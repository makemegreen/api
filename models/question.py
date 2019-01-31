"""User model"""
from sqlalchemy import Column, DateTime, Text
from datetime import datetime

from sqlalchemy.orm import relationship

from models.db import Model
from models.base_object import BaseObject


class Question(BaseObject, Model):

    question_name = Column(Text, unique=True, nullable=False)

    display_text = Column(Text)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow())

    categories = relationship('Category', secondary='question_category')

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Question, self).errors()
        return errors

    def get_categories(self):
        result = []
        for category in self.categories:
            result.append(category.label)

        return result