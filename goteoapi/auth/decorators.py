# -*- coding: utf-8 -*-
#
# Currently this module only handles an implicit oauth authentication.
#
# ----------------------------------------
# Access token authorization
# ----------------------------------------
#
# With Basic HTTP Auth:
#
#              HTTP AUTH
# User owner | ---user/password--> | /login
#            | <--access_token---- |
#
# Or with API key (which is valid also for public requests)
#
#              HTTP AUTH
# User owner | ---user/api_key---> | /login
#            | <--access_token---- |
#
# ----------------------------------------
# Access to public protected resources
# ----------------------------------------
#
#              HEADER Authorize: Bearer
# User owner | ---access_token---> | /projects/
#            | <-------JSON------- |
#
# or with API key (legacy):
#
#              HTTP AUTH
# User owner | ---user/api_key---> | /projects/
#            | <-------JSON------- |
#
# ----------------------------------------
# Access to private/user-only protected resources:
# ----------------------------------------
#
#              HEADER Authorize: Bearer
# User owner | ---access_token---> | /projects/
#            | <-------JSON------- |
#
from datetime import datetime as dtdatetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from functools import update_wrapper
from flask import g, request, jsonify
from netaddr import IPSet, AddrFormatError, IPAddress
from sqlalchemy.orm.exc import NoResultFound

from ..helpers import *

from .. import app
from ..users.models import User, UserApi

def generate_auth_token(authid, expiration = app.config['ACCESS_TOKEN_DURATION']):
    s = Serializer(app.secret_key, expires_in = expiration)
    return s.dumps({ 'id': authid })

def verify_auth_token(token):
    s = Serializer(app.secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return 'Expired token' # valid token, but expired
    except BadSignature:
        return 'Invalid token' # invalid token

    g.loginId = data['id']
    return True

def check_builtin_auth(username, password):
    """Checks username & password authentication"""

    # Personal token workflow
    # try some built-in auth first
    origin = request.headers.get('Origin','*')
    remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if app.config['USERS'] and username in app.config['USERS'] and 'password' in app.config['USERS'][username]:
        user = app.config['USERS'][username]
        if user['password'] == password:
            if 'remotes' in user:
                try:
                    if IPAddress(remote_ip) not in IPSet(user['remotes']):
                        return 'Not valid user for this IP'
                except AddrFormatError as e:
                    if(app.debug):
                        return e
                    return 'Malformed remote IP'
            if 'cors' in user:
                if origin not in user['cors']:
                    return 'Origin header not valid'
            g.loginId = '#' + username
            return True
    return False

def check_apikey_auth(username, password):
    """Checks username & API-key authentication"""

    # Try the user-id-key values in sql
    try:
        userapi = UserApi.query.filter(UserApi.user_id == username, UserApi.key == password).one()

        if userapi.expiration_date is not None and userapi.expiration_date <= dtdatetime.today():
            return 'API Key expired'
        user = User.query.filter(User.id == userapi.user_id).one()
    except NoResultFound:
        return 'Invalid API Key or secret'
    g.loginId = user.id
    return True

def check_user_auth(username, password):
    """Checks username & password authentication"""

    # Try the user-id-key values in sql
    user = User.get(username)
    if user and user.verify_password(password):
        g.loginId = user.id
        return True
    return 'Invalid username or password'

def requires_auth(scope='public'):
    """
    scope:
        - public: Either "Bearer" token or a pair key/secret can be used to gain access to the resource
        - access_token: Either user/password or key/secret can be used to gain access
                        The endpoint using this kind of auth should return the "Bearer" token
        - private: Only "Bearer" token will be accepted as authorization
    """
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if not app.config['AUTH_ENABLED'] and scope == 'public':
                return f(*args, **kwargs)

            # Bearer Auth
            ok = None
            auth = request.headers.get('Authorization')
            if auth and 'Bearer' in auth:
                # Check bearer
                ok = verify_auth_token(auth[7:])
                if ok is True:
                    user = User.query.get(g.loginId)
                    if isinstance(user, User):
                        g.user = user
                    if scope == 'access_token':
                        ok = 'Access token cannot be used to refresh tokens'
            else:
                # Basic Auth
                auth = request.authorization
                msg = 'This resource requires authorization. More info in http://developers.goteo.org/'
                if auth:
                    msg = 'Invalid access method or wrong credentials'
                    # normal user/password can only be used to obtain access_tokens
                    if scope == 'access_token':
                        ok = check_user_auth(auth.username, auth.password)
                    if ok is not True:
                        ok = check_apikey_auth(auth.username, auth.password)
                    if ok is not True:
                        ok = check_builtin_auth(auth.username, auth.password)

            # Check scope for non public resources
            if ok is True and scope not in ('public', 'access_token') and not hasattr(g, 'user'):
                ok = 'Use a proper access token to access this resource'
            if ok is True:
                return f(*args, **kwargs)
            if ok is not False and ok is not None:
                msg = 'Access denied: ' + str(ok)
            resp = jsonify(error=401, message=msg)
            resp.status_code = 401
            resp.headers.add('WWW-Authenticate', 'Basic realm="Goteo API"')
            return resp
        return update_wrapper(wrapped_function, f)
    return decorator

