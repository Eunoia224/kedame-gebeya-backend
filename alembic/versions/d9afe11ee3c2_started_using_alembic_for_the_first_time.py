"""Started using alembic for the first time

Revision ID: d9afe11ee3c2
Revises:
Create Date: 2023-01-19 14:42:47.933681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9afe11ee3c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
    # primary_key=True), sa.Column('Title', sa.String(), nullable=False))

    op.create_table("products", sa.Column("id", sa.String(), nullable=False, primary_key=True)
                    , sa.Column("product_name", sa.String(), nullable=False),
                    sa.Column("image_address", sa.String(), nullable=False),
                    sa.Column("category", sa.String(), nullable=False),
                    sa.Column("type_of_item", sa.String(), nullable=False),
                    sa.Column("price", sa.Integer(), nullable=False),
                    sa.Column("detail", sa.String(), nullable=False),
                    sa.Column("sale", sa.Boolean()),
                    sa.Column("sale_price", sa.Integer()),
                    sa.Column("review_stars", sa.Integer()),
                    sa.Column("reviews", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
                    
                    )
    
    pass


def downgrade() -> None:
    op.delete_table("products")
    pass
