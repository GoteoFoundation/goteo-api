# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os

from goteoapi.tests import test_app, get_json, get_swagger

__import__('goteoapi_digests.controllers')

DIR = os.path.dirname(__file__) + '/'

def test_non_existing():
    rv = test_app.get('/digests/i-dont-exists')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    #make sure we get a response
    eq_(rv.status_code, 400)
    eq_(resp['error'], 400)
    assert 'message' in resp

def test_categories():
    rv = test_app.get('/digests/categories/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)

    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    fields = get_swagger(DIR + 'swagger_specs.yml', 'Digest')
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)
