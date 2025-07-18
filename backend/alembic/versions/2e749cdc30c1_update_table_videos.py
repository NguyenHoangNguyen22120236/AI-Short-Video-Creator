"""Update Table Videos

Revision ID: 2e749cdc30c1
Revises: 3021bd052001
Create Date: 2025-06-02 18:32:51.302670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e749cdc30c1'
down_revision: Union[str, None] = '3021bd052001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('image_urls', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('videos', sa.Column('audio_urls', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('videos', sa.Column('subtitles', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'subtitles')
    op.drop_column('videos', 'audio_urls')
    op.drop_column('videos', 'image_urls')
    # ### end Alembic commands ###
