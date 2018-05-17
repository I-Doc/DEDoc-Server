import datetime

from collections import Iterable
from flask import jsonify


DATE_FORMAT = '%Y-%m-%d'


def date_to_str(date):
    """Convert date to string with format dd/mm/YYYY"""
    return date.strftime(DATE_FORMAT)


def str_to_date(string):
    """Convert string with format dd/mm/YYYY to date object"""
    return datetime.datetime.strptime(string, DATE_FORMAT).date()


def parse_error():
    return jsonify({'error': 'Cannot parse JSON.'}), 400


SER_RULES = {
    int: int,
    str: str,
    bytes: lambda d: bytes_to_string(d),
    datetime.datetime: lambda d: d.isoformat(),
    datetime.date: date_to_str
}


def object_serializer(obj, final=True):
    """Return serialized object.

    object should have ser_fields attr.
    """
    if final:
        return jsonify(_object_serializer(obj))
    else:
        return _object_serializer(obj)


def _object_serializer(obj):
    if obj is None:
        return {}

    if type(obj) in SER_RULES:
        return SER_RULES[type(obj)](obj)

    if hasattr(obj, 'ser_fields'):
        result = {}
        for field_name in obj.ser_fields:
            result[field_name] = _object_serializer(getattr(obj, field_name))
        return result

    if hasattr(obj, 'serialize'):
        return obj.serialize()

    if isinstance(obj, Iterable):
        result = []
        for i in obj:
            result.append(_object_serializer(i))
        return result
    return obj


def string_to_bytes(data):
    return data.encode('utf-8')


def bytes_to_string(data):
    return data.decode('utf-8')
