"""add number of mates for user

Revision ID: f3b2901584ca
Revises: 3ce8db4bc7cd
Create Date: 2019-01-26 19:48:33.886423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b2901584ca'
down_revision = '3ce8db4bc7cd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column('home_mates', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column('user', 'home_mates')
