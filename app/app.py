import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth


app = Flask(__name__)

db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Token')


@app.route('/login')
@auth.login_required
def h():
    return 'gg'


if __name__ == '__main__':
    try:
        command = sys.argv[0]
    except Exception:
        command = 'run'

    if command == 'run':
        app.run(host='0.0.0.0')
    elif command == 'migrate':
        db.create_all()
