from sqlalchemy import Column, schema
from sqlalchemy.types import Integer, String, DateTime

from app.app import db


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer, schema.ForeignKey('users.id'))
    session_token = Column(db.String(60))
    session_ip = Column(db.Integer)
    session_create_time = Column(db.DateTime)
    session_last_use = Column(db.DateTime)