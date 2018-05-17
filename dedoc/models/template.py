from sqlalchemy.sql import func

from dedoc.app import db


class Template(db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    data = db.Column(db.LargeBinary, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    cdate = db.Column(db.DateTime, nullable=False, server_default=func.now())
    mdate = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=func.now(),
        server_default=func.now(),
    )

    ser_fields = (
        'id', 'name', 'data', 'is_active', 'cdate', 'mdate'
    )
