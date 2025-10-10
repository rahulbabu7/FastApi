"""add rest of post table

Revision ID: bde1071c09bf
Revises: 09ff3da83bf2
Create Date: 2025-10-10 18:16:28.440979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bde1071c09bf'
down_revision: Union[str, Sequence[str], None] = '09ff3da83bf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts',sa.Column('content',sa.String(),nullable=False))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Posts','content')
