# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
from . import app, test_app
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


def test_spec():
    rv = test_app.get('/spec')
    eq_(rv.status_code, 200)
