# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from . import test_app, check_content_type, get_json, get_swagger
from ..users.resources import user_resource_fields

DIR = os.path.dirname(__file__) + '/../users/'

FILTERS = [
'page=0',
'limit=1',
'page=1&limit=1',
'lang=ca&lang=fr',
'category=2',
'node=barcelona&lang=en&lang=ca',
'from_date=2014-01-01',
'to_date=2014-12-31',
'from_date=2014-01-01&to_date=2014-12-31',
'location=41.38879,2.15899,50',
'location=41.38879,2.15899,50&from_date=2014-01-01',
'location=41.38879,2.15899,50&to_date=2014-12-31',
'location=41.38879,2.15899,50&from_date=2014-01-01&to_date=2014-12-31'
]
def test_users():
    fields_swagger = get_swagger(DIR + 'swagger_specs/user_list.yml', 'User')
    for f in FILTERS:
        rv = test_app.get('/users/' , query_string=f)
        check_content_type(rv.headers)
        resp = get_json(rv)
        fields = user_resource_fields
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)
        # Swagger test
        eq_(set(resp['items'][0].keys()) , set(fields_swagger.keys()))


def test_user_no_users():
    rv = test_app.get('/users/', query_string='category=0')
    eq_(rv.status_code, 404)
    rv = test_app.get('/users/--i-dont-exits--/')
    eq_(rv.status_code, 404)

def test_user_no_slash():
    rv = test_app.get('/users/goteo')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/users/goteo/' in rv.headers['Location'], "%r not in %r" % ('/users/goteo/', rv.headers['Location'])

def test_user():
    # TODO: generic user
    rv = test_app.get('/users/goteo/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    fields = user_resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
    # Swagger test
    fields = get_swagger(DIR + 'swagger_specs/user_list.yml', 'User')
    eq_(set(resp.keys()) , set(fields.keys()))

