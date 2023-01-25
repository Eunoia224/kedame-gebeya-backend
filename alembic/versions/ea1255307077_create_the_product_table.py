"""create the product table

Revision ID: ea1255307077
Revises: 
Create Date: 2023-01-23 14:17:47.243906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1255307077'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('products', sa.Column('id', sa.String(), nullable=False,
                                          primary_key=True),
                    sa.Column('product_name', sa.String(), nullable=False),
                    # sa.Column('image_address', sa.String(), nullable=False),
                    sa.Column('category', sa.String(), nullable=False),
                    sa.Column('manufacturer', sa.String(), nullable=False),
                    sa.Column('weight', sa.Float(), nullable=False),
                    sa.Column('items_included', sa.String()),
                    sa.Column('type_of_item', sa.String(), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('detail', sa.String(), nullable=False),
                    sa.Column('stock_quantity', sa.Integer(), nullable=False),
                    sa.Column('sale', sa.Boolean()),
                    sa.Column('sale_price', sa.Float()),
                    sa.Column('reviews', sa.Float()),
                    sa.Column('review_stars', sa.Float()),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True)),
                    sa.Column('owner_id', sa.String(), nullable=False)
                    )
    
    
    pass


def downgrade() -> None:
    op.drop_table("products")
    pass
