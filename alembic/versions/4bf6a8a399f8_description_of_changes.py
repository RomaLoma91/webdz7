"""Description of changes

Revision ID: 4bf6a8a399f8
Revises: 42522fb4852f
Create Date: 2023-08-08 09:56:59.484768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bf6a8a399f8'
down_revision: Union[str, None] = '42522fb4852f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
