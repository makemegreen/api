"""generate category

Revision ID: ad42659a324b
Revises: f3b2901584ca
Create Date: 2019-01-31 21:28:07.197666

"""
from datetime import datetime

from sqlalchemy import ForeignKey, Table, MetaData, table
from sqlalchemy.dialects.postgresql import ENUM

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from models import FootprintType, Question
from models.data import app_data

revision = 'ad42659a324b'
down_revision = 'f3b2901584ca'
branch_labels = None
depends_on = None


def upgrade():
    footprint_type = ENUM(FootprintType, create_type=False, name='footprinttype')
    footprint_type.create(op.get_bind(), checkfirst=True)

    category = op.create_table(
        'category',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('label', sa.String(80), nullable=False),
        sa.Column('type', footprint_type, nullable=False),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.utcnow),
    )

    op.create_table(
        'footprint_category',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('category_id', sa.Integer, ForeignKey('category.id'), nullable=False),
        sa.Column('footprint_id', sa.Integer, ForeignKey('footprint.id'), nullable=False),
    )

    question_category = op.create_table(
        'question_category',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('category_id', sa.Integer, ForeignKey('category.id'), nullable=False),
        sa.Column('question_id', sa.Integer, ForeignKey('question.id'), nullable=False),
    )

    op.create_table(
        'recommendation_category',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('category_id', sa.Integer, ForeignKey('category.id'), nullable=False),
        sa.Column('recommendation_id', sa.Integer, ForeignKey('recommendation.id'), nullable=False),
    )

    question = table(
        'question',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column('question_name', sa.String(80), nullable=False),
        sa.Column('display_text', footprint_type, nullable=False),
        sa.Column('date_created', sa.DateTime, nullable=False, default=datetime.utcnow),
     )

    # op.bulk_insert(category, app_data.category_data, multiinsert=False)
    # op.bulk_insert(question, app_data.final_question_data, multiinsert=False)
    # op.bulk_insert(question_category, app_data., multiinsert=False)


def downgrade():
    op.drop_table('question_category')
    op.drop_table('footprint_category')
    op.drop_table('recommendation_category')
    op.drop_table('category')
