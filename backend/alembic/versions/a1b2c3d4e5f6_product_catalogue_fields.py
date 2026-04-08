"""product catalogue fields

Revision ID: a1b2c3d4e5f6
Revises: 4f6d2b9a8e11
Create Date: 2026-04-08 12:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "4f6d2b9a8e11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("sku", sa.String(length=64), nullable=False))
    op.add_column("products", sa.Column("variant", sa.String(length=128), nullable=True))
    op.add_column("products", sa.Column("category", sa.String(length=64), nullable=True))
    op.add_column("products", sa.Column("stock", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("products", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"))
    op.add_column("products", sa.Column("image_path", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("weight_grams", sa.Integer(), nullable=True))

    op.create_index("ix_products_sku", "products", ["sku"], unique=True)

    op.create_check_constraint(
        "ck_products_stock_non_negative",
        "products",
        "stock >= 0",
    )
    op.create_check_constraint(
        "ck_products_price_cents_positive",
        "products",
        "price_cents > 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_products_price_cents_positive", "products", type_="check")
    op.drop_constraint("ck_products_stock_non_negative", "products", type_="check")

    op.drop_index("ix_products_sku", table_name="products")

    op.drop_column("products", "weight_grams")
    op.drop_column("products", "image_path")
    op.drop_column("products", "is_active")
    op.drop_column("products", "stock")
    op.drop_column("products", "category")
    op.drop_column("products", "variant")
    op.drop_column("products", "sku")
