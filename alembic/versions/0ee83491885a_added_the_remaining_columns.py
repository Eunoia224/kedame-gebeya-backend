"""added the remaining columns

Revision ID: 0ee83491885a
Revises: a7b92b2f21d7
Create Date: 2023-01-19 15:17:21.924776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ee83491885a'
down_revision = 'a7b92b2f21d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 
    op.add_column("products", sa.Column("updated_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("products", "updated_at")
    pass
