import datetime

from flask import jsonify


DATE_FORMAT = '%d/%m/%Y'


def date_to_str(date):
    """Convert date to string with format dd/mm/YYYY"""
    return date.strftime(DATE_FORMAT)


def str_to_date(string):
    """Convert string with format dd/mm/YYYY to date object"""
    return datetime.datetime.strptime(string, DATE_FORMAT).date()


def parse_error():
    return jsonify({'error': 'Cannot parse JSON.'}), 400


def serialize(obj):
    """Transforms object to dict"""
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}
