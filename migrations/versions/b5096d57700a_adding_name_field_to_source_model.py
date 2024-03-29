"""Adding name field to Source model

Revision ID: b5096d57700a
Revises: 22b92cd2b1ed
Create Date: 2024-01-29 03:08:45.930321

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b5096d57700a'
down_revision: str | None = '22b92cd2b1ed'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sources', sa.Column('name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sources', 'name')
    # ### end Alembic commands ###
