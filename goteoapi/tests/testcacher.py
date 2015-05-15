# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import random, datetime
from nose.tools import *

from . import app
from goteoapi.cacher import cacher, cache, get_key_functions, get_key_list

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_TIMEOUT'] = 300

cache.clear()

def teardown():
    cache.clear()
    app.config['CACHING'] = False


# Test Functions/Classes

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

def test_cacher():
    app.config['CACHING'] = True
    eq_( get_random() , get_random())
    eq_( get_simple(num=1) , get_simple(1))

def test_class_non_cacher():
    app.config['CACHING'] = False
    eq_( 1 == Dummy.get_simple(1), True)
    eq_( Dummy.get_random() == Dummy.get_random(), False)

def test_class_cacher():
    app.config['CACHING'] = True
    eq_( Dummy.get_random() , Dummy.get_random())

def test_static_methods():
    keys = {
            "(S'get_simple'\np0\n(I1\ntp1\n(dp2\ntp3\n.": (50, datetime.datetime.now()),
            "(S'get_simple'\np0\n(cgoteoapi.tests.testcacher\nDummy\np1\nI1\ntp2\n(dp3\ntp4\n.": (50, datetime.datetime.now()),
            "(S'get_simple'\np0\n(t(dp1\nS'num'\np2\nI1\nstp3\n.": (50, datetime.datetime.now())
            }
    key_list = get_key_functions(keys)

    eq_(len(key_list) , len(keys))
    for key, clas, f, args, kargs in key_list:
        if not hasattr(f, '__call__'):
            if f in locals():
                f = locals()[f]
            elif f in globals():
                f = globals()[f]
        eq_( 1, int(f(*args, **kargs)))

def test_invalid_keys():
    keys = {"get_simple|1==2":(50, datetime.datetime.now()),}
    key_list = get_key_functions(keys)
    eq_( len(key_list) , 0)

# TODO...
# def test_instance_methods():
#     keys = {"<class 'goteoapi.tests.testcacher.Dummy'>|get_random":(50, datetime.datetime.now())}
#     key_list = get_key_functions(keys)
#     assert len(key_list) == 1
#     for f, args, kargs in key_list:
#         eq_( "1" == f(*args, **kargs), True)


