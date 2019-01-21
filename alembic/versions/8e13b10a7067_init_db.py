"""Init db

Revision ID: 8e13b10a7067
Revises: 
Create Date: 2019-01-21 13:27:29.456754

"""
from pathlib import Path
import os
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e13b10a7067'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    sql_file = Path(os.path.dirname(os.path.realpath(__file__))) / 'sql' / 'init_db.sql'
    with open(sql_file, 'r') as file:
        data = file.read()
    op.execute(data)


def downgrade():
    pass
