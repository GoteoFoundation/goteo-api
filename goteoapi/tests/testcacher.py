# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import time, random, datetime
from nose.tools import *

from . import app
from goteoapi.cacher import cacher, get_key_functions

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_TIMEOUT'] = 300

@cacher
def get_simple(num="0"):
    return num

@cacher
def get_random():
    return random.random()

class Dummy():
    @classmethod
    @cacher
    def get_simple(self, num="0"):
        return num

    @classmethod
    @cacher
    def get_random(self):
        return random.random()

# TESTS

def test_non_cacher():
    app.config['CACHING'] = False
    assert get_random() != get_random()

def test_cacher():
    app.config['CACHING'] = True
    assert get_random() == get_random()

def test_class_non_cacher():
    app.config['CACHING'] = False
    assert 1 == Dummy.get_simple(1)
    assert Dummy.get_random() != Dummy.get_random()

def test_class_cacher():
    app.config['CACHING'] = True
    assert Dummy.get_random() == Dummy.get_random()

def test_static_methods():
    keys = {"get_simple|1":(50, datetime.datetime.now()),
            "get_simple|<class 'goteoapi.tests.testcacher.Dummy'>|1":(50, datetime.datetime.now()),
            "get_simple|<class 'goteoapi.tests.testcacher.Dummy'>|num=1":(50, datetime.datetime.now())}
    key_list = get_key_functions(keys)
    assert len(key_list) == 3
    for f, args, kargs in key_list:
        if not hasattr(f, '__call__'):
            if f in locals():
                f = locals()[f]
            elif f in globals():
                f = globals()[f]
        assert 1 == int(f(*args, **kargs))

# TODO...
# def test_instance_methods():
#     keys = {"<class 'goteoapi.tests.testcacher.Dummy'>|get_random":(50, datetime.datetime.now())}
#     key_list = get_key_functions(keys)
#     assert len(key_list) == 1
#     for f, args, kargs in key_list:
#         assert "1" == f(*args, **kargs)
