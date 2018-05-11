from sqlalchemy import Column, schema
from sqlalchemy.types import Boolean, Date, Integer, String

from dedoc.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(50), nullable=False, unique=True)
    password = Column(db.String(60), nullable=False)
    is_admin = Column(db.Boolean, default=False)
    is_active = Column(db.Boolean, default=True)
    email = Column(db.String(50))

    name = Column(db.String(50), nullable=False)
    surname = Column(db.String(50))
    fathername = Column(db.String(50))
    birthdate = Column(db.Date)
