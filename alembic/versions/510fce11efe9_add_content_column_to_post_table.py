"""Add content column to post table

Revision ID: 510fce11efe9
Revises: adb32e66ec76
Create Date: 2022-06-17 01:08:37.098817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510fce11efe9'
down_revision = 'adb32e66ec76'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
