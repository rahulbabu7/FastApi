"""add foreign key to post table 

Revision ID: 75f2902717be
Revises: bec267107d39
Create Date: 2025-10-10 18:31:32.840534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75f2902717be'
down_revision: Union[str, Sequence[str], None] = 'bec267107d39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Posts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('user_id_fkey',source_table="Posts",referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('user_id_fkey',table_name="Posts")
    op.drop_column('Posts',"user_id")
