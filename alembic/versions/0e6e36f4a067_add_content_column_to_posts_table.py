"""add content column to posts table

Revision ID: 0e6e36f4a067
Revises: 0098b518f554
Create Date: 2026-09-24 11:16:04.491944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e6e36f4a067'
down_revision: Union[str, Sequence[str], None] = '0098b518f554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
