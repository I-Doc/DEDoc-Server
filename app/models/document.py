from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, Date, Integer, String, LargeBinary

from app.app import db


class Document(db.Model):
    __tablename__ = "documents"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50))
    owner = Column(db.Integer, schema.ForeignKey('users.id'))
    template = Column(db.Integer, schema.ForeignKey('templates.id'))
    state = Column(db.Integer, schema.ForeignKey('document_state.id'))
    data = Column(db.LargeBinary, nullable=False)
    cdate = Column(db.Date, nullable=False)
    mdate = Column(db.Date, nullable=False)
