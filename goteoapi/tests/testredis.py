# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#

from nose.tools import *
from time import sleep
from . import app, redis_url
from .testcacher import get_random, get_simple, get_alt, Dummy
from ..ratelimit import redis
from ..cacher import cache
from goteoapi.cacher import get_key_list

app.config['REDIS_URL'] = redis_url
app.config['CACHE_MIN_TIMEOUT'] = 1
app.config['CACHE']['CACHE_TYPE'] = 'redis'

cache.init_app(app, config=app.config['CACHE'])

def teardown():
    cache.clear()
    app.config['CACHING'] = False


# Test Functions/Classes

# TESTS

# REDIS Test
def test_cacher_redis():
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
    eq_( 1 == Dummy.get_simple(1), True)
    eq_( Dummy.get_random() , Dummy.get_random())

