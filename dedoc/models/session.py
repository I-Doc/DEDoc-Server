from sqlalchemy.sql import func

from dedoc.app import db


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    token = db.Column(db.String(60))
    ip = db.Column(db.Integer)
    ctime = db.Column(db.DateTime, server_default=func.now())
    mtime = db.Column(db.DateTime, onupdate=func.now())