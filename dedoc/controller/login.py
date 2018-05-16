from uuid import uuid4

from flask import g, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from dedoc.app import auth, db
from dedoc.constants import SQL_DUPLICATE_ERROR
from dedoc.models.session import Session
from dedoc.models.user import User


@auth.verify_token
def verify_token(token):
    """Check if token belong to any session, and return owner of session.

    Don't use this function directly!

    :params:
        - `token`: str token parsed by flask_httpauth.

    :return:
        True, if token is valid, otherwise False and set g.auth_error
         with error message.
    """
    session = Session.query.filter(Session.token == token).first()
    if session:
        user = User.query.filter(User.id == Session.user).first()
        if user:
            if not user.is_active:
                g.auth_error = 'User is not active. Contact administrator.'
                return False
            g.current_user = user
        else:
            g.auth_error = 'User not found.'
            return False
    else:
        g.auth_error = 'Wrong token.'
        return False
    g.auth_error = None
    return True


@auth.error_handler
def auth_error():
    """Auth error handler."""
    return jsonify({'error': g.auth_error or 'access denied'})


def get_session(user, ip):
    """Return token and session for user.

    If there is already session for this IP and ID - it will be returned.
    Otherwise new will be created.

    :params:
        - `user_id`: user object to create session.
        - `ip`: current login request IP address.

    :return:
        tuple with session object and bool indication if session is new.
    """
    sessions = Session.query.filter(
        Session.user == user.id,
        Session.ip == ip).order_by(Session.ctime.desc())
    session = sessions.first()
    new_session = False
    if not session:
        new_session = True
        print("new session will be created for user: %s and ip: %s" % (user, ip))
        session = Session(user=user.id, ip=ip, token=str(uuid4()))
        db.session.add(session)
        db.session.commit()
    return session, new_session


def _get_password_hash(password):
    """Return bcrypt hash of given password st."""
    return generate_password_hash(password).decode('utf-8')


def check_password(username, password):
    """Check password.

    :params:
        - `username`:
        - `password`:

    :return:
        Return user object if password is correct, None otherwise.
    """
    user = User.query.filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def register_new_user(user_data):
    """Register new user.

    :return:
        tuple with new user object and None if register successful or
         None and error message if something gone wrong.
    """
    try:
        new_user = User(
            username=user_data['username'],
            password=_get_password_hash(user_data['password']),
            name=user_data['name'],
            surname=user_data['surname'],
            fathername=user_data['fathername'],
            birthdate=user_data['birthdate'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, None
    except IntegrityError as error:
        str_error = str(error)
        if SQL_DUPLICATE_ERROR in str_error:
            return None, 'User already exists!'
        return None, str(error)
