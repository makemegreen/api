from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.base_object import BaseObject
from models.db import Model


class UserSession(BaseObject, Model):
    userId = Column(BigInteger, ForeignKey('user.id'), nullable=False)

    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
