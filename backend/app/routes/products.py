from fastapi import APIRouter

from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products() -> list[ProductOut]:
	return [
		ProductOut(
			id=1,
			name="Gelaender Shirt - Black",
			description="First-run release shirt.",
			price_cents=3200,
		),
		ProductOut(
			id=2,
			name="Gelaender Cap - Steel Blue",
			description="Limited cap release.",
			price_cents=2600,
		),
	]
