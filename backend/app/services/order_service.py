from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreateRequest, OrderItemInput


class OrderValidationError(ValueError):
    """Raised when order input cannot be processed safely."""


def validate_item_quantities(items: list[OrderItemInput]) -> None:
    for item in items:
        if item.quantity < 1:
            raise OrderValidationError("Quantity must be at least 1.")


def calculate_totals_cents(
    items: list[OrderItemInput],
    products_by_id: dict[int, Product],
) -> tuple[int, list[dict[str, int]]]:
    total_cents = 0
    prepared_items: list[dict[str, int]] = []

    for item in items:
        product = products_by_id.get(item.product_id)
        # Keep this helper safe if it is reused without pre-validation.
        if product is None:
            raise OrderValidationError(f"Product {item.product_id} not found.")

        unit_price_cents = product.price_cents
        line_total_cents = unit_price_cents * item.quantity
        total_cents += line_total_cents

        prepared_items.append(
            {
                "product_id": product.id,
                "quantity": item.quantity,
                "unit_price_cents": unit_price_cents,
                "line_total_cents": line_total_cents,
            }
        )

    return total_cents, prepared_items


def create_order_from_items(
    db: Session,
    payload: OrderCreateRequest,
    client_request_id: str | None = None,
) -> Order:
    if client_request_id:
        existing_order = db.execute(
            select(Order)
            .where(Order.client_request_id == client_request_id)
            .options(selectinload(Order.items))
        ).scalar_one_or_none()
        if existing_order is not None:
            return existing_order

    validate_item_quantities(payload.items)

    product_ids = sorted({item.product_id for item in payload.items})
    products = db.execute(select(Product).where(Product.id.in_(product_ids))).scalars().all()
    products_by_id = {product.id: product for product in products}

    missing_product_ids = [str(product_id) for product_id in product_ids if product_id not in products_by_id]
    if missing_product_ids:
        joined_ids = ", ".join(missing_product_ids)
        raise OrderValidationError(f"Unknown product ids: {joined_ids}")

    total_cents, prepared_items = calculate_totals_cents(payload.items, products_by_id)

    order = Order(
        status="pending",
        total_cents=total_cents,
        currency="eur",
        client_request_id=client_request_id,
        customer_name=payload.customer_name,
        customer_email=str(payload.customer_email),
    )

    order.items = [
        OrderItem(
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price_cents=item["unit_price_cents"],
            line_total_cents=item["line_total_cents"],
        )
        for item in prepared_items
    ]

    db.add(order)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if client_request_id:
            existing_order = db.execute(
                select(Order)
                .where(Order.client_request_id == client_request_id)
                .options(selectinload(Order.items))
            ).scalar_one_or_none()
            if existing_order is not None:
                return existing_order
        raise OrderValidationError("Unable to create order due to a conflicting request.") from exc

    db.refresh(order)
    return order
