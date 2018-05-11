import json
import datetime
from ipaddress import IPv4Address

from flask import request, jsonify, g

from dedoc.app import app, auth
from dedoc.controller import login as login_controller
from dedoc.controller import validators
from dedoc.utils import date_to_str, str_to_date, parse_error


REGISTRATION_REQUIRED_FIELDS = ()


@app.route('/login', methods=['POST'])
def login():
    """Create new session and return token of this session.

    :params:
        - `username`: str
        - `password`: str
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return parse_error()

    username = data.get('username')
    password = data.get('password')

    error = None

    if not username:
        error = 'No `username` field.'

    if not password:
        error = 'No `password` field.'

    print('username: %s password: %s' % (username, password, ))

    if error:
        return jsonify({'error': error})

    login_user = login_controller.check_password(username, password)
    if login_user:
        ip = int(IPv4Address(request.remote_addr))
        session, new = login_controller.get_session(login_user, ip)
        return jsonify({'new': new, 'token': session.token})
    else:
        return jsonify({'error': 'Wrong username or password'})


@app.route('/register', methods=['POST'])
def register():
    """Register new user with given data."""
    data = request.get_json(force=True, silent=True)
    if not data:
        return parse_error()

    errors = []

    username = data.get('username')
    password = data.get('password')

    name = data.get('name')
    surname = data.get('surname')
    fathername = data.get('fathername')

    birthdate = data.get('birthdate')
    if not birthdate:
        errors.append('No `birthdate` field.')
    else:
        try:
            birthdate = str_to_date(birthdate)
            if not validators.validate_birthdate(birthdate):
                errors.append('Wrong `birthdate`.')
        except ValueError:
            errors.append('Wrong date format. Need dd/mm/YYYY.')

    if not username:
        errors.append('No `username` field.')
    else:
        if not validators.validate_username(username):
            errors.append('`username` field is not valid.')

    if not password:
        errors.append('No `password` field.')
    else:
        password_errors = validators.validate_password(password)
        if password_errors:
            errors.extend(password_errors)

    if not name:
        errors.append('No `name` field.')
    else:
        if not validators.validate_name(name):
            errors.append('`name` field is not valid.')

    if not surname:
        errors.append('No `surname` field.')
    else:
        if not validators.validate_surname(surname):
            errors.append('`surname` field is not valid.')

    if not fathername:
        errors.append('No `fathername` field.')
    else:
        if not validators.validate_fathername(fathername):
            errors.append('`fathername` field is not valid.')

    if errors:
        return jsonify({'errors': errors, 'success': False})
    else:
        registration_data = {
            'username': username,
            'password': password,
            'name': name,
            'surname': surname,
            'fathername': fathername,
            'birthdate': birthdate,
        }

    new_user, error = login_controller.register_new_user(registration_data)
    if new_user:
        ip = int(IPv4Address(request.remote_addr))
        new_user_session, _ = login_controller.get_session(new_user, ip)
        print("new user session: %s" % (new_user_session, ))
        return jsonify({'token': new_user_session.token})
    else:
        return jsonify({'error': error})


@app.route('/check', methods=['GET'])
@auth.login_required
def check():
    return jsonify({
        'username': g.current_user.username,
        'name': g.current_user.name,
        'surname': g.current_user.surname,
        'fathername': g.current_user.fathername,
        'birthdate': date_to_str(g.current_user.birthdate),
        })