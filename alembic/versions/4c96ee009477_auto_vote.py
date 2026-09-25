"""auto-vote

Revision ID: 4c96ee009477
Revises: f46c10d8b649
Create Date: 2026-09-24 15:51:15.633719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c96ee009477'
down_revision: Union[str, Sequence[str], None] = 'f46c10d8b649'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column("user_id", sa.Integer(), nullable=False),
                    sa.Column("post_id", sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ["posts.id"], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint("user_id", "post_id"))
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
