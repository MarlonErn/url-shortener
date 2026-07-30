"""set initial urls id sequence

Revision ID: 89d3a02c3da4
Revises: 1e450830b3af
Create Date: 2026-07-30 00:02:31.099621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89d3a02c3da4'
down_revision: Union[str, Sequence[str], None] = '1e450830b3af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DELETE FROM sqlite_sequence WHERE name = 'urls';")
    op.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', 14776335);")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM sqlite_sequence WHERE name = 'urls';")
    op.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', COALESCE((SELECT MAX(id) FROM urls), 0));")
    pass
