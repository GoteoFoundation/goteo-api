# -*- coding: utf-8 -*-
from datetime import datetime as dtdatetime

from functools import wraps
from flask import request, jsonify
from netaddr import IPSet, AddrFormatError
from sqlalchemy.orm.exc import NoResultFound

from ..helpers import *

from .. import app, db

#
# BASIC AUTH DECORATOR
# ====================
# Based on http://flask.pocoo.org/snippets/8/

def check_auth(username, password):
    """Checks username & password authentication"""

    # #try some built-in auth first
    # if app.config['USERS'] and username in app.config['USERS'] and 'password' in app.config['USERS'][username]:
    #     user = app.config['USERS'][username]
    #     if user['password'] == password:
    #         if 'remotes' in user:
    #             try:
    #                 remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #                 if remote_ip in IPSet(user['remotes']):
    #                     return True
    #             except AddrFormatError:
    #                 pass

    #         else:
    #             return True

    #Try the key-password values in sql
    try:
        from ..users.models import UserApi
        user = UserApi.query.filter(UserApi.user == username).one()
        print (user)
        if user.expiration_date is not None and user.expiration_date <= dtdatetime.today():
            # print (user.expiration_date, '<=', dtdatetime.today())
            return 'API Key expired. Please get new valid key! '
        return True
    except NoResultFound:
        return 'Acces denied: Invalid username or password!'

    return False


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not app.config['AUTH_ENABLED']:
            return f(*args, **kwargs)

        auth = request.authorization
        msg = 'You need a key in order to use this API. Get one on www.goteo.org!'
        if auth:
            ok = check_auth(auth.username, auth.password)
            if(ok is True):
                return f(*args, **kwargs)
            elif(ok is not False):
                msg = str(ok)

        resp = jsonify(error=401, message=msg)
        resp.status_code = 401
        resp.headers.add('WWW-Authenticate', 'Basic realm="Goteo.org API"')
        return resp

    return decorated
