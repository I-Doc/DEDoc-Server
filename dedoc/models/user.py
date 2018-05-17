from dedoc.app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date)

    ser_fields = (
        'id', 'username', 'is_admin', 'name', 'birthdate',
    )
