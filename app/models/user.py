from sqlalchemy import Column, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean, Date, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column('user_id', Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    email = Column(String(50))

    name = Column(String(50), nullable=False)
    surname = Column(String(50))
    fathername = Column(String(50))
    birthdate = Column(Date())