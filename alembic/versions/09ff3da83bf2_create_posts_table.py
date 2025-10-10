"""create posts table

Revision ID: 09ff3da83bf2
Revises:
Create Date: 2025-10-10 17:34:15.806408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09ff3da83bf2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('Posts',sa.Column('id',sa.INTEGER(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("Posts")
