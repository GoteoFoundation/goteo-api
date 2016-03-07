# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import random, datetime
from nose.tools import *

from . import app
from goteoapi.cacher import cacher, cache, get_key_functions

cache.clear()

def teardown():
    cache.clear()
    app.config['CACHING'] = False


# Test Functions/Classes


alt = 1
@cacher
def get_alt():
    global alt
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
    eq_( get_alt() , 0)
    eq_( get_alt() , 1)

def test_cacher():
    app.config['CACHING'] = True
    eq_( get_random() , get_random())
    eq_( get_simple() , get_simple(0))
    eq_( get_simple(num=1) , get_simple(1))
    eq_( get_alt() , 0)
    eq_( get_alt() , 0)

def test_class_non_cacher():
    app.config['CACHING'] = False
    eq_( 0 == Dummy.get_simple(0), True)
    eq_( Dummy.get_random() == Dummy.get_random(), False)

def test_class_cacher():
    app.config['CACHING'] = True
    eq_( 1 == Dummy.get_simple(1), True)
    eq_( Dummy.get_random() , Dummy.get_random())

def test_static_methods():
    Dummy.get_simple(num=0)
    keys = {
            b'\x80\x04\x95\x13\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94)}\x94\x87\x94.': (50, datetime.datetime.now()),
            b'\x80\x04\x95\x16\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94K\x00\x85\x94}\x94\x87\x94.': (50, datetime.datetime.now()),
            b'\x80\x04\x95C\x00\x00\x00\x00\x00\x00\x00\x8c\nget_simple\x94\x8c\x19goteoapi.tests.testcacher\x94\x8c\x05Dummy\x94\x93\x94\x85\x94}\x94\x8c\x03num\x94K\x00s\x87\x94.': (50, datetime.datetime.now())
            }
    key_list = get_key_functions(keys)
    eq_(len(key_list) , len(keys))
    for key, clas, f, args, kargs in key_list:
        if not hasattr(f, '__call__'):
            if f in locals():
                f = locals()[f]
            elif f in globals():
                f = globals()[f]
        eq_( 0, int(f(*args, **kargs)))

def test_invalid_keys():
    keys = {
        "get_simple|1==2":(50, datetime.datetime.now()),
        "Cacher/total|<class 'goteoapi.users.models.User'>|node=None|category=[u'16']|lang=None|project=None|from_date=2013-01-01|location=None|year=None|to_date=2013-12-31":(50, datetime.datetime.now()),
    }
    key_list = get_key_functions(keys)
    eq_( len(key_list) , 0)

# TODO...
# def test_instance_methods():
#     keys = {"<class 'goteoapi.tests.testcacher.Dummy'>|get_random":(50, datetime.datetime.now())}
#     key_list = get_key_functions(keys)
#     assert len(key_list) == 1
#     for f, args, kargs in key_list:
#         eq_( "1" == f(*args, **kargs), True)


