from flask import request
from app import app
from app.models import Session


@auth.verify_token
def verify_token(token):
    Session.o
    g.current_user = object()
    return True


@auth.error_handler
def auth_error():
    return 'Access Denied'