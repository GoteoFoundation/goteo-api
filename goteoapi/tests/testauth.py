# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *

from . import test_app, app, get_json
from base64 import b64encode
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def setup():
    app.config['AUTH_ENABLED'] = True
    app.config['USERS'] = {
        'bob' : {
            'password': 'marley'
        },
        'peter' : {
            'password': 'tosh',
            'remotes': ['127.0.0.0/16']
        },
        'bunny' : {
            'password': 'wailer',
            'remotes': ['127.0.0.0/16'],
            'cors': ['https://stats.goteo.org']
        }
    }

def teardown():
    app.config['AUTH_ENABLED'] = False


def test_reject_auth():
    rv = test_app.get('/login',
                      headers={
                        'Authorization': 'Basic %s' % b64encode(b"jimmy:cliff").decode("ascii")
                    })
    assert 'WWW-Authenticate' in rv.headers
    assert 'Basic' in rv.headers['WWW-Authenticate']
    eq_(rv.status_code, 401)

token = False
def test_accept_auth():
    global token
    rv = test_app.get('/login',
                      headers={
                        'Authorization': 'Basic %s' % b64encode(b"bob:marley").decode("ascii")
                    })
    eq_(rv.status_code, 200)
    content = get_json(rv)
    # Test access token
    assert 'access_token' in content
    token = content['access_token']

def test_valid_token():
    s = Serializer(app.secret_key)
    data = s.loads(token)
    assert 'id' in data
    # Test

def test_reject_auth_by_token():
    rv = test_app.get('/projects/',
                      headers={
                        'Authorization': 'Bearer non-existing-token'
                    })
    eq_(rv.status_code, 401)
    # Login not allowed by bearer
    rv = test_app.get('/login',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 401)
    # Bearer without user not allowed in private scopes
    rv = test_app.get('/me',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 401)

def test_accept_auth_by_token():
    rv = test_app.get('/projects/',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 200)
    rv = test_app.get('/licenses/',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 200)
    rv = test_app.get('/users/',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 200)
    rv = test_app.get('/categories/',
                      headers={
                        'Authorization': 'Bearer %s' % token
                    })
    eq_(rv.status_code, 200)

# TODO: test by SQL users
#
def test_reject_auth_by_remote():
    rv = test_app.get('/login',
                      environ_base={
                        'HTTP_X_REAL_IP': '172.0.0.2'
                        },
                      headers={
                        'Authorization': 'Basic %s' % b64encode(b"peter:tosh").decode("ascii")
                    })
    eq_(rv.status_code, 401)


def test_accept_auth_by_remote():
    rv = test_app.get('/login',
                      environ_base={
                        'HTTP_X_REAL_IP': '127.0.0.1'
                      },
                      headers={
                        'Authorization': 'Basic %s' % b64encode(b"peter:tosh").decode("ascii")
                    })
    eq_(rv.status_code, 200)


def test_reject_auth_by_cors():
    rv = test_app.get('/login',
                      environ_base={
                        'HTTP_X_REAL_IP': '127.0.0.2'
                      },headers={
                        'Authorization': 'Basic %s' % b64encode(b"bunny:wailer").decode("ascii"),
                        'Origin' : 'http://stats.goteo.org'
                     })
    eq_(rv.status_code, 401)

def test_accept_auth_by_cors():
    rv = test_app.get('/login', environ_base={
                        'HTTP_X_REAL_IP': '127.0.0.1'
                      },headers={
                        'Authorization': 'Basic %s' % b64encode(b"bunny:wailer").decode("ascii"),
                        'Origin' : 'https://stats.goteo.org'
                    })
    eq_(rv.status_code, 200)


def test_oauth_user_login():
    rv = test_app.get('/login',
                      headers={
                        'Authorization': 'Basic %s' % b64encode(b"bob:marley").decode("ascii")
                    })
    eq_(rv.status_code, 200)

