# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from . import app,test_app, get_json, get_swagger
from ..calls.resources import call_resource_fields, call_full_resource_fields
from ..projects.resources import project_resource_fields
from ..cacher import cache

old_redis_url = app.config['REDIS_URL']
old_cache_min_timeout = app.config['CACHE_MIN_TIMEOUT']
old_cache_type = app.config['CACHE']['CACHE_TYPE']

def setup():
    cache.clear()
    app.config['CACHING'] = True
    app.config['REDIS_URL'] = None
    app.config['CACHE_MIN_TIMEOUT'] = 5
    app.config['CACHE']['CACHE_TYPE'] = 'simple'
    cache.init_app(app, config=app.config['CACHE'])

def teardown():
    cache.clear()
    app.config['CACHING'] = False
    app.config['REDIS_URL'] = old_redis_url
    app.config['CACHE_MIN_TIMEOUT'] = old_cache_min_timeout
    app.config['CACHE']['CACHE_TYPE'] = old_cache_type

DIR = os.path.dirname(__file__) + '/../calls/'

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
'location=42.9,-2.6,50',
'location=42.9,-2.6,50&from_date=2014-01-01',
'location=42.9,-2.6,50&to_date=2014-12-31',
'location=42.9,-2.6,50&from_date=2014-01-01&to_date=2014-12-31'
]
def test_calls():
    fields_swagger = get_swagger(DIR + 'swagger_specs/call_list.yml', 'Call')
    for f in FILTERS:
        rv = test_app.get('/calls/' , query_string=f)
        eq_(rv.headers['Content-Type'], 'application/json')
        resp = get_json(rv)
        fields = call_resource_fields
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)
        # Swagger test
        eq_(set(resp['items'][0].keys()) , set(fields_swagger.keys()))

def test_calls_cached():
    test_calls()

def test_call_no_calls():
    rv = test_app.get('/calls/--i-dont-exits--')
    eq_(rv.status_code, 404)
    rv = test_app.get('/calls/', query_string='category=0')
    resp = get_json(rv)
    eq_(rv.status_code, 200)
    assert 'items' in resp
    eq_(resp['items'], [])

def test_call_trailing_slash():
    rv = test_app.get('/calls')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/calls/' in rv.headers['Location'], "%r not in %r" % ('/calls/', rv.headers['Location'])
    rv = test_app.get('/calls/test-call/')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/calls/test-call' in rv.headers['Location'], "%r not in %r" % ('/calls/test-call', rv.headers['Location'])

def test_call():
    # TODO: generic call here
    rv = test_app.get('/calls/crowdsasuna/')
    eq_(rv.status_code, 301)
    rv = test_app.get('/calls/crowdsasuna')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    fields = call_full_resource_fields
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
    # Swagger test
    fields = get_swagger(DIR + 'swagger_specs/call_item.yml', 'CallFull')
    eq_(set(resp.keys()) , set(fields.keys()))

def test_call_cached():
    test_call()

def test_call_projects():
    fields_swagger = get_swagger(DIR + 'swagger_specs/call_projects.yml', 'ProjectCall')
    rv = test_app.get('/calls/crowdsasuna/projects')
    eq_(rv.status_code, 301)
    rv = test_app.get('/calls/crowdsasuna/projects/')
    eq_(rv.status_code, 200)
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    fields = project_resource_fields
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)

    # Swagger test
    eq_(set(resp['items'][0].keys()) , set(fields_swagger.keys()))
