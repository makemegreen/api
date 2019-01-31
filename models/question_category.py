from sqlalchemy import Column, ForeignKey, BigInteger

from models import BaseObject
from models.db import Model


class QuestionCategory(BaseObject, Model):
    question_id = Column(BigInteger, ForeignKey('question.id'), nullable=False)

    category_id = Column(BigInteger, ForeignKey('category.id'), nullable=False)

    def get_id(self):
        return str(self.id)
