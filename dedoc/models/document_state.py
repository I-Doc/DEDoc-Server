from dedoc.app import db


class DocumentState(db.Model):
    __tablename__ = 'document_state'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(255))
