# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from datetime import date,timedelta
from . import app,test_app, get_json, get_swagger
from ..categories.resources import category_resource_fields
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


DIR = os.path.dirname(__file__) + '/../categories/'

from_date = (date.today() - timedelta(days=40)).isoformat()
to_date = (date.today() - timedelta(days=20)).isoformat()

FILTERS = [
'',
'lang=ca&lang=fr',
'category=2',
'node=goteo',
'from_date=' + from_date ,
'to_date=' + to_date,
'from_date=' + from_date + '&to_date=' + to_date,
'location=41.38879,2.15899,50',
'location=41.38879,2.15899,50&from_date=' + from_date ,
'location=41.38879,2.15899,50&to_date=' + to_date,
'location=41.38879,2.15899,50&from_date=' + from_date + '&to_date=' + to_date
]
def test_categories():
    fields_swagger = get_swagger(DIR + 'swagger_specs.yml', 'Category')
    for f in FILTERS:
        rv = test_app.get('/categories/' , query_string=f)
        eq_(rv.headers['Content-Type'], 'application/json')
        resp = get_json(rv)

        fields = category_resource_fields
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)

        # Swagger test
        eq_(set(resp['items'][0].keys()) , set(fields_swagger.keys()))

def test_categories_cached():
    test_categories()
