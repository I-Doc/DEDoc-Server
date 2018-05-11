from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, Date, Integer, LargeBinary, String

from dedoc.app import db


class DocumentState(db.Model):
    __tablename__ = 'document_state'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(30), unique=True)
    description = Column(db.String(255))
