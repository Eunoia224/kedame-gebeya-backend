"""added users table

Revision ID: fa09acfa8fb8
Revises: d9afe11ee3c2
Create Date: 2023-01-19 15:05:39.634542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa09acfa8fb8'
down_revision = 'd9afe11ee3c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.String(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("phone_number", sa.Integer()),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"),
                    sa.UniqueConstraint("phone_number"),
                    )
    pass

def downgrade() -> None:
    op.delete_table("products")
    pass
