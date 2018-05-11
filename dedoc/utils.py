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
    return jsonify({'error': 'Cannot parse JSON.'})