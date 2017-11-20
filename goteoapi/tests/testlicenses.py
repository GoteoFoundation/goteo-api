# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from . import app, test_app, get_json, get_swagger
from ..licenses.resources import license_resource_fields
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

DIR = os.path.dirname(__file__) + '/../licenses/'

FILTERS = [
    '',
    'lang=ca'
]


def test_licenses():
    rv = test_app.get('/licenses/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)

    fields = license_resource_fields
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys()))
            - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
    # Swagger test
    fields_swagger = get_swagger(DIR + 'swagger_specs.yml', 'License')
    eq_(set(resp['items'][0].keys()), set(fields_swagger.keys()))


def test_licenses_cached():
    test_licenses()
