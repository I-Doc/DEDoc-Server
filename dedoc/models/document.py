from sqlalchemy.sql import func

from dedoc.app import db


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    owner = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    template = db.Column(
        db.Integer,
        db.ForeignKey('templates.id', ondelete='CASCADE'),
        nullable=False,
    )
    state = db.Column(
        db.Integer,
        db.ForeignKey('document_state.id', ondelete='CASCADE'),
        nullable=False,
    )
    data = db.Column(db.LargeBinary, nullable=False)
    cdate = db.Column(db.DateTime, nullable=False, server_default=func.now())
    mdate = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=func.now(),
        server_default=func.now(),
    )
