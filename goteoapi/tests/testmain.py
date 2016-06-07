# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *

from . import test_app, app, get_json

app.config['AUTH_ENABLED']


def test_main_routes():
    rv = test_app.get('/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    #make sure we get a response
    eq_(rv.status_code, 200)

    assert 'endpoints' in resp
    assert 'message' in resp
    assert 'version' in resp
    assert 'links' in resp


def test_error_routes():
    rv = test_app.get('/i-dont-exists')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    eq_(rv.status_code, 404)
    assert 'error' in resp
    eq_(resp['error'], 404)
    assert 'message' in resp


def test_trailing_slash():
    rv = test_app.get('/projects')
    eq_(rv.status_code, 301)
    eq_(rv.headers['Location'], 'http://localhost/projects/')


def test_bad_request():
    rv = test_app.get('/projects/?category=string')
    eq_(rv.status_code, 400)


def test_cors_headers():
    rv = test_app.get('/projects/')
    eq_(rv.headers['Content-Type'], 'application/json')
    assert 'Access-Control-Allow-Origin' in rv.headers
    assert 'Access-Control-Allow-Headers' in rv.headers
    assert 'Access-Control-Expose-Headers' in rv.headers
    assert 'Access-Control-Allow-Methods' in rv.headers
    assert 'Access-Control-Allow-Credentials' in rv.headers
    assert 'Access-Control-Max-Age' in rv.headers
    eq_(len(rv.headers.getlist('Access-Control-Allow-Origin')), 1)
    eq_(len(rv.headers.getlist('Access-Control-Allow-Headers')), 1)
    eq_(len(rv.headers.getlist('Access-Control-Expose-Headers')), 1)
    eq_(len(rv.headers.getlist('Access-Control-Allow-Methods')), 1)
    eq_(len(rv.headers.getlist('Access-Control-Allow-Credentials')), 1)
    eq_(len(rv.headers.getlist('Access-Control-Max-Age')), 1)



