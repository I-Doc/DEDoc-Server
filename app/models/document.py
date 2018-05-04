from sqlalchemy import Column, schema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean, Date, Integer, String, LargeBinary


Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    owner = Column(Integer, schema.ForeignKey('users.user_id'))
    template = Column(Integer, schema.ForeignKey('templates.template_id'))
    state = Column(Integer, schema.ForeignKey('document_state.state_id'))
    data = Column(LargeBinary, nullable=False)
    cdate = Column(Date, nullable=False)
    mdate = Column(Date, nullable=False)
