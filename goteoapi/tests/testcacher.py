# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import random
import datetime
from nose.tools import *
from time import sleep
from . import app
from goteoapi.cacher import cache, cacher, get_key_functions, get_key_list

old_redis_url = app.config['REDIS_URL']
old_cache_min_timeout = app.config['CACHE_MIN_TIMEOUT'] = 1
old_cache_type = app.config['CACHE']['CACHE_TYPE'] = 'redis'


def setup():
    app.config['REDIS_URL'] = None
    app.config['CACHE_MIN_TIMEOUT'] = 1
    app.config['CACHE']['CACHE_TYPE'] = 'simple'
    cache.init_app(app, config=app.config['CACHE'])


def teardown():
    cache.clear()
    app.config['CACHING'] = False
    app.config['REDIS_URL'] = old_redis_url
    app.config['CACHE_MIN_TIMEOUT'] = old_cache_min_timeout
    app.config['CACHE']['CACHE_TYPE'] = old_cache_type


# Test Functions/Classes
alt = 1


@cacher
def get_alt(a=None):
    global alt
    if a is not None:
        alt = a
    alt = 1 - alt
    return alt


@cacher
def get_simple(num=0):
    return num


@cacher
def get_random():
    return random.random()


class Dummy():
    @classmethod
    @cacher
    def get_simple(self, num=0):
        return num

    @classmethod
    @cacher
    def get_random(self):
        return random.random()

# TESTS


def test_non_cacher():
    app.config['CACHING'] = False
    eq_(get_random() == get_random(), False)
    eq_(get_alt(), 0)
    eq_(get_alt(), 1)


def test_cacher():
    app.config['CACHING'] = True
    eq_(get_random(), get_random())
    eq_(get_simple(), get_simple(0))
    eq_(get_simple(num=1), get_simple(1))
    get_alt(0)
    eq_(get_alt(), 0)
    eq_(get_alt(), 0)
    sleep(1.1)
    eq_(get_alt(), 1)
    assert len(get_key_list()) > 0


def test_class_non_cacher():
    app.config['CACHING'] = False
    eq_(0 == Dummy.get_simple(0), True)
    eq_(Dummy.get_random() == Dummy.get_random(), False)


def test_class_cacher():
    app.config['CACHING'] = True
    eq_(1 == Dummy.get_simple(1), True)
    eq_(Dummy.get_random(), Dummy.get_random())


def test_renew_cacher():
    key_list = get_key_list()
    assert len(key_list) > 0
    func_list = get_key_functions(get_key_list(), True)
    assert len(func_list) > 0


def test_static_methods():
    Dummy.get_simple(num=0)
    keys = {
            b'\x80\x04\x95\x13\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94)}\x94\x87\x94.': (50, datetime.datetime.now()),
            b'\x80\x04\x95\x16\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94K\x00\x85\x94}\x94\x87\x94.': (50, datetime.datetime.now()),
            b'\x80\x04\x95C\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94\x8c\x19goteoapi.tests.testcacher\x94\x8c\x05Dummy\x94\x93\x94\x85\x94}\x94\x8c\x03num\x94K\x00s\x87\x94.': (50, datetime.datetime.now())
            }
    key_list = get_key_functions(keys)
    eq_(len(key_list), len(keys))
    for key, clas, f, args, kargs in key_list:
        if not hasattr(f, '__call__'):
            if f in locals():
                f = locals()[f]
            elif f in globals():
                f = globals()[f]
        eq_(0, int(f(*args, **kargs)))


def test_invalid_keys():
    keys = {
        "get_simple|1==2": (50, datetime.datetime.now()),
        "Cacher/total|<class 'goteoapi.users.models.User'>|node=None|category=[u'16']|lang=None|project=None|from_date=2013-01-01|location=None|year=None|to_date=2013-12-31": (50, datetime.datetime.now()),
    }
    key_list = get_key_functions(keys)
    eq_(len(key_list), 0)

# TODO...
# def test_instance_methods():
#     keys = {"<class 'goteoapi.tests.testcacher.Dummy'>|get_random":(50, datetime.datetime.now())}
#     key_list = get_key_functions(keys)
#     assert len(key_list) == 1
#     for f, args, kargs in key_list:
#         eq_("1" == f(*args, **kargs), True)
