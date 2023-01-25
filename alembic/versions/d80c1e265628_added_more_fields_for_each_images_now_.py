"""added more fields for each images now can accept 8 total images 1 main and 7 additional

Revision ID: d80c1e265628
Revises: 82b0d12cb7d1
Create Date: 2023-01-25 11:50:32.813961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd80c1e265628'
down_revision = '82b0d12cb7d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('products', sa.Column(
    #     'image_address', sa.String(), nullable=False))
    op.add_column('products', sa.Column('main_img', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_1', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_2', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_3', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_4', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_5', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_6', sa.String(), nullable=False))
    op.add_column('products', sa.Column('img_7', sa.String(), nullable=False))
    op.drop_column('products', 'image_address')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('products', sa.Column('image_address', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('products', 'img_7')
    op.drop_column('products', 'img_6')
    op.drop_column('products', 'img_5')
    op.drop_column('products', 'img_4')
    op.drop_column('products', 'img_3')
    op.drop_column('products', 'img_2')
    op.drop_column('products', 'img_1')
    op.drop_column('products', 'main_img')
    # ### end Alembic commands ###