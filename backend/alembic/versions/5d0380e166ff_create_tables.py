"""Create Tables

Revision ID: 5d0380e166ff
Revises: 2b59616027da
Create Date: 2025-05-08 10:03:45.006790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d0380e166ff'
down_revision: Union[str, None] = '2b59616027da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
