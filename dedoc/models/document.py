import datetime

from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, DateTime, Integer, LargeBinary, String
from sqlalchemy.sql import func

from dedoc.app import db


class Document(db.Model):
    __tablename__ = "documents"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), nullable=False, unique=True)
    owner = Column(db.Integer, schema.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    template = Column(db.Integer, schema.ForeignKey('templates.id', ondelete='CASCADE'), nullable=False)
    state = Column(db.Integer, schema.ForeignKey('document_state.id', ondelete='CASCADE'), nullable=False)
    data = Column(db.LargeBinary, nullable=False)
    cdate = Column(db.DateTime, nullable=False, server_default=func.now())
    mdate = Column(db.DateTime, nullable=False, onupdate=func.now())
