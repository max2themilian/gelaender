from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
	pending = "pending"
	confirmed = "confirmed"
	cancelled = "cancelled"


class OrderItemInput(BaseModel):
	product_id: int = Field(gt=0)
	quantity: int = Field(ge=1, le=100)


class OrderCreateRequest(BaseModel):
	customer_name: str = Field(min_length=1, max_length=255)
	customer_email: str = Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
	items: list[OrderItemInput] = Field(min_length=1, max_length=100)


class OrderItemOut(BaseModel):
	id: int
	product_id: int
	quantity: int
	unit_price_cents: int
	line_total_cents: int

	model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
	id: int
	status: OrderStatus
	total_cents: int
	currency: str
	client_request_id: str | None = None
	customer_name: str
	customer_email: str
	stripe_checkout_session_id: str | None = None
	stripe_payment_intent_id: str | None = None
	items: list[OrderItemOut]

	model_config = ConfigDict(from_attributes=True)
