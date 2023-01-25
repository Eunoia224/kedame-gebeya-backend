"""create the users table

Revision ID: 869ca81c3cd8
Revises: ea1255307077
Create Date: 2023-01-23 14:18:29.235285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '869ca81c3cd8'
down_revision = 'ea1255307077'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.String(), nullable=False,
                                          primary_key=True),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('delivery_address', sa.String()),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('phone_number', sa.Integer(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(
                        timezone=True)),

                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass