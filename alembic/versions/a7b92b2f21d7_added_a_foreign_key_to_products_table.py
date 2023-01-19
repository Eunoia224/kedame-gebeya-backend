"""added a foreign key to products table

Revision ID: a7b92b2f21d7
Revises: fa09acfa8fb8
Create Date: 2023-01-19 15:12:27.323397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b92b2f21d7'
down_revision = 'fa09acfa8fb8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("products", sa.Column(
        "owner_id", sa.String(), nullable=False))
    op.create_foreign_key("product_users_fk", source_table="products", referent_table="users", local_cols=[
                          "owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("product_users_fk", table_name="products")
    op.drop_column("products", "owner_id")
    pass
