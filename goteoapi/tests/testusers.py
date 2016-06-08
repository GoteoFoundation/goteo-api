# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from datetime import date, timedelta
from . import app, test_app, get_json, get_swagger
from ..users.resources import user_resource_fields
from ..cacher import cache

old_redis_url = app.config['REDIS_URL']
old_cache_min_timeout = app.config['CACHE_MIN_TIMEOUT']
old_cache_type = app.config['CACHE']['CACHE_TYPE']


def setup():
    cache.clear()
    app.config['CACHING'] = True
    app.config['REDIS_URL'] = None
    app.config['CACHE_MIN_TIMEOUT'] = 2
    app.config['CACHE']['CACHE_TYPE'] = 'simple'
    cache.init_app(app, config=app.config['CACHE'])


def teardown():
    cache.clear()
    app.config['CACHING'] = False
    app.config['REDIS_URL'] = old_redis_url
    app.config['CACHE_MIN_TIMEOUT'] = old_cache_min_timeout
    app.config['CACHE']['CACHE_TYPE'] = old_cache_type

DIR = os.path.dirname(__file__) + '/../users/'

from_date = (date.today() - timedelta(days=60)).isoformat()
to_date = (date.today() - timedelta(days=20)).isoformat()

FILTERS = [
    'page=0',
    'limit=1',
    'page=1&limit=1',
    'lang=ca&lang=fr',
    'category=2',
    'node=goteo&lang=en&lang=ca',
    'from_date=' + from_date,
    'to_date=' + to_date,
    'from_date=' + from_date + '&to_date=' + to_date
]


def test_users():
    fields_swagger = get_swagger(DIR + 'swagger_specs/user_list.yml', 'User')
    for f in FILTERS:
        print(f)
        rv = test_app.get('/users/', query_string=f)
        eq_(rv.headers['Content-Type'], 'application/json')
        resp = get_json(rv)
        fields = user_resource_fields
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys()))
                - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)
        # Swagger test
        eq_(set(resp['items'][0].keys()), set(fields_swagger.keys()))


def test_users_cached():
    test_users()


def test_user_no_users():
    rv = test_app.get('/users/', query_string='category=0')
    resp = get_json(rv)
    eq_(rv.status_code, 200)
    assert 'items' in resp
    eq_(resp['items'], [])
    rv = test_app.get('/users/--i-dont-exits--')
    eq_(rv.status_code, 404)


def test_user_trailing_slash():
    rv = test_app.get('/users')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/users/' in rv.headers['Location'], "%r not in %r" % (
        '/users/', rv.headers['Location'])
    rv = test_app.get('/users/owner-project-passing/')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert ('/users/owner-project-passing' in rv.headers['Location'],
            "%r not in %r" % ('/users/owner-project-passing',
                              rv.headers['Location']))


def test_user():
    # TODO: generic user
    rv = test_app.get('/users/owner-project-passing')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    fields = user_resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys()))
            - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
    # Swagger test
    fields = get_swagger(DIR + 'swagger_specs/user_item.yml', 'UserFull')
    eq_(set(resp.keys()), set(fields.keys()))


def test_user_cached():
    test_user()
