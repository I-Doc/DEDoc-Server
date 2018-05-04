from sqlalchemy import Column, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean, Date, Integer, String, LargeBinary


Base = declarative_base()


class DocumentState(Base):
    __tablename__ = 'document_state'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    description = Column(String(255))