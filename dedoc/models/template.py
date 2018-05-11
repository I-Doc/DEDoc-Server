import datetime

from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, DateTime, Integer, String, LargeBinary
from sqlalchemy.sql import func

from dedoc.app import db


class Template(db.Model):
    __tablename__ = "templates"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True)
    data = Column(db.LargeBinary, nullable=False)
    is_active = Column(db.Boolean, default=True)
    mdate = Column(db.DateTime, nullable=False, server_default=func.now())
    cdate = Column(db.DateTime, nullable=False, onupdate=func.now())
