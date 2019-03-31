"""User model"""
from sqlalchemy import Column, DateTime, Text, String, Float, Boolean
from datetime import datetime

from models.category_mixin import CategoryMixin
from models.db import Model
from models.base_object import BaseObject


class Recommendation(BaseObject, CategoryMixin, Model):
    title = Column(String(120), nullable=False)

    content = Column(Text, nullable=False)

    benefit = Column(Float, nullable=False)

    benefit_description = Column(Text, nullable=True)

    did_you_know = Column(Text, nullable=True)

    how_to = Column(Text, nullable=True)

    is_shared = Column(Boolean, nullable=False, default=False)

    date_created = Column(DateTime, nullable=True, default=datetime.utcnow)

    def errors(self):
        errors = super(Recommendation, self).errors()
        return errors
