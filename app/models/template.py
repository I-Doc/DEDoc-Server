from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, Date, Integer, String, LargeBinary

from app.app import db


class Template(db.Model):
    __tablename__ = "templates"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50))
    data = Column(db.LargeBinary, nullable=False)
    is_active = Column(db.Boolean, default=True)
    mdate = Column(db.Date, nullable=False)
    cdate = Column(db.Date, nullable=False)
