"""Add user table

Revision ID: 660daecd200b
Revises: 510fce11efe9
Create Date: 2022-06-17 01:00:38.293805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '660daecd200b'
down_revision = '510fce11efe9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass