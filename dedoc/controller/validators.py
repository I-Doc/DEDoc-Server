"""This module contains field validators."""
import re
import datetime

LC_PAT = re.compile(r'[a-z]')
UC_PAT = re.compile(r'[A-Z]')
NUM_PAT = re.compile(r'[0-9]')


def validate_username(username):
    """Return True is username is valid, False otherwise"""
    return username is not None and username != ''


def validate_password(password):
    """Return list of errors. If there is not error - then password is valid."""
    error = []
    if len(password) < 6:
        error.append('Password length should be greater than 5.')
    elif len(password) > 15:
        error.append("Password length shouldn't be greater than 15.")

    if not LC_PAT.search(password):
        error.append('Password should contain lowercase letters.')
    if not UC_PAT.search(password):
        error.append('Password should contain uppercase letter')
    if not NUM_PAT.search(password):
        error.append('Password should contain at least on number.')

    return error


def validate_name(name):
    """Return True is name is valid, False otherwise"""
    return validate_username(name)


def validate_surname(surname):
    """Return True is surname is valid, False otherwise"""
    return validate_name(surname)


def validate_fathername(fathername):
    """Return True is fathername is valid, False otherwise"""
    return validate_name(fathername)


def validate_birthdate(birthdate):
    """Return True if birthdate is valid, False otherwise"""
    return datetime.date(1940, 1, 1) < birthdate < datetime.date.today()
