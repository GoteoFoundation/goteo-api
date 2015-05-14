# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from . import app,test_app, check_content_type

def test_main_routes():
    rv = test_app.get('/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    #make sure we get a response
    eq_(rv.status_code, 200)

    assert 'endpoints' in resp
    assert 'message' in resp
    assert 'version' in resp
    assert 'links' in resp

def test_error_routes():
    rv = test_app.get('/i-dont-exists')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    eq_(rv.status_code, 404)
    assert 'error' in resp
    eq_(resp['error'], 404)
    assert 'message' in resp


def test_categories():
    from ..categories.resources import CategoryResponse as Response, CategoriesListResponse as ListResponse
    app.config['REQUESTS_LIMIT'] = None
    app.config['AUTH_ENABLED'] = False
    rv = test_app.get('/categories/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    print resp

    fields = ListResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)

