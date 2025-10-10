"""add post table last columns

Revision ID: 4d2600b18e67
Revises: 75f2902717be
Create Date: 2025-10-10 18:40:20.505449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d2600b18e67'
down_revision: Union[str, Sequence[str], None] = '75f2902717be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('Posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    


def downgrade():
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    
