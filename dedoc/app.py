"""This module initialize application."""
import configparser
import os

from flask import Flask
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy


conf_parser = configparser.ConfigParser()
conf_parser.read('db.conf')

if conf_parser.has_section('database'):
    db_keys = ('username', 'password', 'db_type', 'db_name', 'host')
    db_data = {key: conf_parser.get('database', key) for key in db_keys}
    database_uri = ('%(db_type)s://'
                    '%(username)s:%(password)s@'
                    '%(host)s/%(db_name)s?charset=utf8') % db_data
else:
    database_uri = os.environ['DATABASE_URI']

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Token')


from dedoc import urls, models, controller
