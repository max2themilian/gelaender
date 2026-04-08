from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.dependencies import db_session
from app.models.order import Order
from app.schemas.order import OrderCreateRequest, OrderResponse
from app.services.order_service import OrderValidationError, create_order_from_items

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
	payload: OrderCreateRequest,
	idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
	db: Session = Depends(db_session),
) -> Order:
	try:
		return create_order_from_items(db, payload, client_request_id=idempotency_key)
	except OrderValidationError as exc:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(db_session)) -> Order:
	order = db.execute(
		select(Order)
		.where(Order.id == order_id)
		.options(selectinload(Order.items))
	).scalar_one_or_none()

	if order is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

	return order
