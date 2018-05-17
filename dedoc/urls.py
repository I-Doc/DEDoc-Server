from ipaddress import IPv4Address

from flask import request, jsonify, g

from dedoc.app import app, auth
from dedoc.controller import login as login_controller
from dedoc.controller import document as document_controller
from dedoc.controller import template as template_controller
from dedoc.controller import validators
from dedoc.models.document import Document
from dedoc.models.template import Template
from dedoc.models.document_state import DocumentState
from dedoc.utils import str_to_date, parse_error, object_serializer, \
    string_to_bytes

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

    print('username: %s password: %s' % (username, password,))

    if error:
        return jsonify({'error': error}), 400

    login_user = login_controller.check_password(username, password)
    if login_user:
        ip = int(IPv4Address(request.remote_addr))
        session, new = login_controller.get_session(login_user, ip)
        return jsonify({'new': new, 'token': session.token})
    else:
        return jsonify({'error': 'Wrong username or password'}), 401


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

    birthdate = data.get('birthdate')
    if not birthdate:
        errors.append('No `birthdate` field.')
    else:
        try:
            birthdate = str_to_date(birthdate)
            if not validators.validate_birthdate(birthdate):
                errors.append('Wrong `birthdate`.')
        except ValueError:
            errors.append('Wrong date format. Need YYYY-mm-dd.')

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

    if errors:
        return jsonify({'errors': errors, 'success': False}), 400
    else:
        registration_data = {
            'username': username,
            'password': password,
            'name': name,
            'birthdate': birthdate,
        }

    new_user, error = login_controller.register_new_user(registration_data)
    if new_user:
        ip = int(IPv4Address(request.remote_addr))
        new_user_session, _ = login_controller.get_session(new_user, ip)
        print('new user session: %s' % (new_user_session,))
        return jsonify({'token': new_user_session.token})
    else:
        return jsonify({'error': error}), 400


@app.route('/profile', methods=['GET'])
@auth.login_required
def profile():
    return object_serializer(g.current_user)


@app.route('/documents', methods=['GET'])
@auth.login_required
def documents():
    if g.current_user.is_admin:
        documents = Document.query.all()
    else:
        documents = Document.query.filter_by(owner=g.current_user.id)
    return object_serializer(documents)


@app.route('/documents/<id>', methods=['GET'])
@auth.login_required
def document(id):
    document = Document.query \
        .filter_by(owner=g.current_user.id) \
        .filter_by(id=id) \
        .first()

    return object_serializer(document)


@app.route('/documents/<id>/state', methods=['POST'])
@auth.login_required
def change_document_state(id):
    data = request.get_json(force=True, silent=True)
    if not data:
        return parse_error()

    if g.current_user.is_admin:
        new_state = data.get('state')
        if not new_state:
            return jsonify({'error': '`state` not found.'})

        error = document_controller.change_document_state(id, new_state)
        if error:
            return jsonify({'error': error})
        return jsonify({'success': True})
    return jsonify({'error': 'Permissions denied.'})


@app.route('/documents', methods=['POST'])
@auth.login_required
def create_document():
    data = request.get_json(force=True, silent=True)

    if not data:
        return parse_error()

    name = data.get('name')
    owner = g.current_user.id
    template = data.get('template')
    state = 1
    data = string_to_bytes(data.get('data'))

    document = {
        'name': name,
        'owner': owner,
        'template': template,
        'state': state,
        'data': data,
    }

    new_document, error = document_controller.create_document(document)

    if new_document:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': error}), 400


@app.route('/templates', methods=['GET'])
@auth.login_required
def templates():
    templates = Template.query.all()
    return object_serializer(templates)


@app.route('/templates/<id>', methods=['GET'])
@auth.login_required
def template(id):
    return object_serializer(Template.query.get(id), False)


@app.route('/templates', methods=['POST'])
@auth.login_required
def create_template():
    data = request.get_json(force=True, silent=True)

    if not data:
        return parse_error()

    name = data.get('name')
    data = string_to_bytes(data.get('data'))

    template = {
        'name': name,
        'data': data,
    }

    new_template, error = template_controller.create_template(template)

    if new_template:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': error}), 400


@app.route('/states', methods=['GET'])
def doc_states():
    return object_serializer(DocumentState.query.all())