# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#

from nose.tools import *
from time import sleep
from . import app, test_app
from .testcacher import get_random, get_simple, get_alt, Dummy
from ..ratelimit import redis
from ..cacher import cache
from goteoapi.cacher import get_key_list
from nose import SkipTest
import warnings

redis_url = app.config['REDIS_URL']
old_cache_min_timeout = app.config['CACHE_MIN_TIMEOUT']
old_cache_type = app.config['CACHE']['CACHE_TYPE']

def setup():
    app.config['CACHE_MIN_TIMEOUT'] = 1
    app.config['CACHE']['CACHE_TYPE'] = 'redis'
    cache.init_app(app, config=app.config['CACHE'])
    if not redis_url:
        warnings.warn('REDIS is not configured. Some tests will be skipped')

def teardown():
    cache.clear()
    app.config['CACHING'] = False
    app.config['CACHE_MIN_TIMEOUT'] = old_cache_min_timeout
    app.config['CACHE']['CACHE_TYPE'] = old_cache_type


# Test Functions/Classes

# TESTS

# REDIS Test
def test_cacher_redis():
    if not redis_url:
        raise SkipTest()
    app.config['CACHING'] = True
    assert redis
    eq_( get_random() , get_random())
    eq_( get_simple() , get_simple(0))
    eq_( get_simple(num=1) , get_simple(1))
    get_alt(0)
    eq_( get_alt() , 0)
    eq_( get_alt() , 0)
    sleep(1.1)
    eq_( get_alt() , 1)
    assert len(get_key_list()) > 0


def test_class_cacher_redis():
    if not redis_url:
        raise SkipTest()
    eq_( 1 == Dummy.get_simple(1), True)
    eq_( Dummy.get_random() , Dummy.get_random())


# Rate limit tests
#
def test_limit_headers():
    if not redis_url:
        raise SkipTest()
    rv = test_app.get('/projects/')
    eq_(rv.headers['Content-Type'], 'application/json')
    assert 'X-RateLimit-Remaining' in rv.headers
    assert 'X-RateLimit-Limit' in rv.headers
    assert 'X-RateLimit-Reset' in rv.headers
    eq_(len(rv.headers.getlist('X-RateLimit-Remaining')), 1)
    eq_(len(rv.headers.getlist('X-RateLimit-Limit')), 1)
    eq_(len(rv.headers.getlist('X-RateLimit-Reset')), 1)

def test_limit_behaviour():
    if not redis_url:
        raise SkipTest()
    rv = test_app.get('/projects/')
    remaining = int(rv.headers.get('X-RateLimit-Remaining'))
    limit = int(rv.headers.get('X-RateLimit-Limit'))
    reset = int(rv.headers.get('X-RateLimit-Reset'))
    assert remaining > 0
    assert limit > 0
    assert reset > 0
    rv = test_app.get('/projects/')
    eq_(int(rv.headers.get('X-RateLimit-Remaining')), remaining - 1)

