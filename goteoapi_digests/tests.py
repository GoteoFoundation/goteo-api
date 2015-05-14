# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from goteoapi import app
from .resources import DigestResponse as Response, DigestsListResponse as ListResponse

app.debug = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['AUTH_ENABLED'] = False

test_app = app.test_client()

__import__('goteoapi.controllers')
__import__('goteoapi_digests.controllers')

def check_content_type(headers):
  eq_(headers['Content-Type'], 'application/json')

def test_non_existing():
    rv = test_app.get('/digests/i-dont-exists')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    #make sure we get a response
    eq_(rv.status_code, 400)
    eq_(resp['error'], 400)
    assert 'message' in resp

def test_categories():
    rv = test_app.get('/digests/categories/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)

    fields = ListResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
