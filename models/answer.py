"""User model"""
from sqlalchemy import Column, DateTime, Text, BigInteger, ForeignKey, Float
from datetime import datetime

from models.db import Model
from models.base_object import BaseObject


class Answer(BaseObject, Model):

    answer_name = Column(Text, unique=True, nullable=False)

    value = Column(Float, nullable=True)

    display_text = Column(Text)

    date_created = Column(DateTime, nullable=False, default=datetime.utcnow())

    question_id = Column(BigInteger, ForeignKey('question.id'), nullable=False)

    def get_id(self):
        return str(self.id)

    def errors(self):
        errors = super(Answer, self).errors()
        return errors
