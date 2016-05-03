# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os
from . import test_app, get_json, get_swagger
from ..invests.resources import invest_resource_fields

DIR = os.path.dirname(__file__) + '/../invests/'

FILTERS = [
'page=0',
'limit=1',
'page=1&limit=1',
'category=2',
'node=barcelona',
'from_date=2014-01-01',
'to_date=2014-12-31',
'from_date=2014-01-01&to_date=2014-12-31',
# 'location=41.38879,2.15899,50',
]
def test_invests():
    fields_swagger = get_swagger(DIR + 'swagger_specs/invest_list.yml', 'Invest')
    for f in FILTERS:
        rv = test_app.get('/invests/' , query_string=f)
        eq_(rv.headers['Content-Type'], 'application/json')
        resp = get_json(rv)
        fields = invest_resource_fields
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)
        # Swagger test
        eq_(set(resp['items'][0].keys()) , set(fields_swagger.keys()))


def test_invest_no_invests():
    rv = test_app.get('/invests/', query_string='category=0')
    resp = get_json(rv)
    eq_(rv.status_code, 200)
    assert 'items' in resp
    eq_(resp['items'], [])
    rv = test_app.get('/invests/--i-dont-exits--')
    eq_(rv.status_code, 404)

def test_invest_trailing_slash():
    rv = test_app.get('/invests')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/invests/' in rv.headers['Location'], "%r not in %r" % ('/invests/', rv.headers['Location'])
    rv = test_app.get('/invests/10/')
    eq_(rv.status_code, 301)
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/invests/10' in rv.headers['Location'], "%r not in %r" % ('/invests/10', rv.headers['Location'])

def test_invest():
    # TODO: generic invest
    rv = test_app.get('/invests/10')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    fields = invest_resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)
    # Swagger test
    fields = get_swagger(DIR + 'swagger_specs/invest_item.yml', 'InvestFull')
    eq_(set(resp.keys()) , set(fields.keys()))

