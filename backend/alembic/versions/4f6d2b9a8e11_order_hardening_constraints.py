"""order hardening constraints

Revision ID: 4f6d2b9a8e11
Revises: 9a6f9d2d1c41
Create Date: 2026-04-08 12:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f6d2b9a8e11"
down_revision: Union[str, None] = "9a6f9d2d1c41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("orders", sa.Column("client_request_id", sa.String(length=128), nullable=True))
    op.create_index(op.f("ix_orders_client_request_id"), "orders", ["client_request_id"], unique=True)

    op.create_check_constraint(
        "ck_orders_total_cents_non_negative",
        "orders",
        "total_cents >= 0",
    )
    op.create_check_constraint(
        "ck_orders_status_valid",
        "orders",
        "status IN ('pending','confirmed','cancelled')",
    )

    op.create_check_constraint(
        "ck_order_items_quantity_positive",
        "order_items",
        "quantity >= 1",
    )
    op.create_check_constraint(
        "ck_order_items_unit_price_non_negative",
        "order_items",
        "unit_price_cents >= 0",
    )
    op.create_check_constraint(
        "ck_order_items_line_total_non_negative",
        "order_items",
        "line_total_cents >= 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_order_items_line_total_non_negative", "order_items", type_="check")
    op.drop_constraint("ck_order_items_unit_price_non_negative", "order_items", type_="check")
    op.drop_constraint("ck_order_items_quantity_positive", "order_items", type_="check")

    op.drop_constraint("ck_orders_status_valid", "orders", type_="check")
    op.drop_constraint("ck_orders_total_cents_non_negative", "orders", type_="check")

    op.drop_index(op.f("ix_orders_client_request_id"), table_name="orders")
    op.drop_column("orders", "client_request_id")
