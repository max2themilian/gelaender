from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Order(Base):
	__tablename__ = "orders"
	__table_args__ = (
		CheckConstraint("total_cents >= 0", name="ck_orders_total_cents_non_negative"),
		CheckConstraint("status IN ('pending','confirmed','cancelled')", name="ck_orders_status_valid"),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)
	total_cents: Mapped[int] = mapped_column(Integer, nullable=False)
	currency: Mapped[str] = mapped_column(String(3), nullable=False, default="eur")
	client_request_id: Mapped[str | None] = mapped_column(String(128), nullable=True, unique=True, index=True)
	customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
	customer_email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
	stripe_checkout_session_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
	stripe_payment_intent_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	items: Mapped[list["OrderItem"]] = relationship(
		back_populates="order",
		cascade="all, delete-orphan",
		passive_deletes=True,
	)


class OrderItem(Base):
	__tablename__ = "order_items"
	__table_args__ = (
		CheckConstraint("quantity >= 1", name="ck_order_items_quantity_positive"),
		CheckConstraint("unit_price_cents >= 0", name="ck_order_items_unit_price_non_negative"),
		CheckConstraint("line_total_cents >= 0", name="ck_order_items_line_total_non_negative"),
	)

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
	product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"), nullable=False, index=True)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False)
	unit_price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
	line_total_cents: Mapped[int] = mapped_column(Integer, nullable=False)

	order: Mapped[Order] = relationship(back_populates="items")
