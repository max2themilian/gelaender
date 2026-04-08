from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
	name: str
	description: str | None = None
	price_cents: int


class ProductOut(ProductBase):
	id: int

	model_config = ConfigDict(from_attributes=True)
