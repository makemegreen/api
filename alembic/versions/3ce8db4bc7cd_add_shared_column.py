"""add shared column

Revision ID: 3ce8db4bc7cd
Revises: 9e8d8048691e
Create Date: 2019-01-26 16:52:18.669714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce8db4bc7cd'
down_revision = '9e8d8048691e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'recommendation',
        sa.Column('is_shared', sa.Boolean(), nullable=True, default=False)
    )
    new_column = sa.table('recommendation', sa.column('is_shared'))
    op.execute(new_column.update().values(**{'is_shared': False}))
    op.alter_column('recommendation', 'is_shared', nullable=False)


def downgrade():
    op.drop_column('recommendation', 'is_shared')
