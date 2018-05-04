from sqlalchemy import Column, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean, Date, Integer, String, LargeBinary


Base = declarative_base()


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    data = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=True)
    mdate = Column(Date, nullable=False)
    cdate = Column(Date, nullable=False)
