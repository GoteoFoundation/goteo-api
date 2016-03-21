# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *

from . import test_app, app
from base64 import b64encode

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
    rv = test_app.get('/projects/', headers={
                                        'Authorization': 'Basic %s' % b64encode(b"jimmy:cliff").decode("ascii")
                                    })
    assert 'WWW-Authenticate' in rv.headers
    assert 'Basic' in rv.headers['WWW-Authenticate']
    eq_(rv.status_code, 401)

def test_accept_auth():
    rv = test_app.get('/projects/', headers={
                                        'Authorization': 'Basic %s' % b64encode(b"bob:marley").decode("ascii")
                                    })
    eq_(rv.status_code, 200)

def test_reject_auth_by_remote():
    rv = test_app.get('/projects/', environ_base={
                                        'HTTP_X_REAL_IP': '172.0.0.2'
                                    }, headers={
                                        'Authorization': 'Basic %s' % b64encode(b"peter:tosh").decode("ascii")
                                    })
    eq_(rv.status_code, 401)


def test_accept_auth_by_remote():
    rv = test_app.get('/projects/', environ_base={
                                        'HTTP_X_REAL_IP': '127.0.0.1'
                                    }, headers={
                                        'Authorization': 'Basic %s' % b64encode(b"peter:tosh").decode("ascii")
                                    })
    eq_(rv.status_code, 200)


def test_reject_auth_by_cors():
    rv = test_app.get('/projects/', environ_base={
                                        'HTTP_X_REAL_IP': '127.0.0.2'
                                    },headers={
                                        'Authorization': 'Basic %s' % b64encode(b"bunny:wailer").decode("ascii"),
                                        'Origin' : 'http://stats.goteo.org'
                                    })
    eq_(rv.status_code, 401)

def test_accept_auth_by_cors():
    rv = test_app.get('/projects/', environ_base={
                                        'HTTP_X_REAL_IP': '127.0.0.1'
                                    },headers={
                                        'Authorization': 'Basic %s' % b64encode(b"bunny:wailer").decode("ascii"),
                                        'Origin' : 'https://stats.goteo.org'
                                    })
    eq_(rv.status_code, 200)



