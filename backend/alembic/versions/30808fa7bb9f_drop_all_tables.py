"""drop all tables

Revision ID: 30808fa7bb9f
Revises: 3fa12aa1f1fe
Create Date: 2025-05-08 10:09:52.712754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30808fa7bb9f'
down_revision: Union[str, None] = '3fa12aa1f1fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from app.models import Base


def upgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())


def downgrade() -> None:
    """Downgrade schema."""
    pass
