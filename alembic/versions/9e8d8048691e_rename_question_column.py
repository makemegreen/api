"""rename question column

Revision ID: 9e8d8048691e
Revises: 8e13b10a7067
Create Date: 2019-01-24 12:58:17.330594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e8d8048691e'
down_revision = '8e13b10a7067'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('question', 'property_name', new_column_name='question_name')


def downgrade():
    op.alter_column('payment', 'question_name', new_column_name='property_name')
