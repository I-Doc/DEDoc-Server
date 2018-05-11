from sqlalchemy import Column, schema
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.sql import func

from dedoc.app import db


class Session(db.Model):
    __tablename__ = 'sessions'

    id = Column(db.Integer, primary_key=True)
    user = Column(db.Integer, schema.ForeignKey('users.id', ondelete="CASCADE"))
    token = Column(db.String(60))
    ip = Column(db.Integer)
    ctime = Column(db.DateTime, server_default=func.now())
    mtime = Column(db.DateTime, onupdate=func.now())