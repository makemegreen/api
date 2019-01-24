"""User model"""
from sqlalchemy import Column, Integer, DateTime, Text
from datetime import datetime

from models.db import Model
from models.base_object import BaseObject


class Question(BaseObject, Model):

    id = Column(Integer, primary_key=True)

    question_name = Column(Text, unique=True, nullable=False)

    display_text = Column(Text)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow())

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Question, self).errors()
        return errors
