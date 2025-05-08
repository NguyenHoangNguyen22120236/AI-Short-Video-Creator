"""drop all tables

Revision ID: 2b59616027da
Revises: d3cebec3ea16
Create Date: 2025-05-08 10:01:37.955595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.models import Base


# revision identifiers, used by Alembic.
revision: str = '2b59616027da'
down_revision: Union[str, None] = 'd3cebec3ea16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    pass
