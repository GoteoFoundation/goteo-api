# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os

from goteoapi.tests import test_app, check_content_type, get_json, get_swagger

__import__('goteoapi_reports.controllers')

DIR = os.path.dirname(__file__) + '/'

def test_money():
    rv = test_app.get('/reports/money/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    #make sure we get a response
    eq_(rv.status_code, 200)
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    docs = get_swagger(DIR + 'swagger_specs/money.yml')
    fields = docs['definitions'][-1]['schema']['properties']
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)

def test_projects():
    rv = test_app.get('/reports/projects/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    docs = get_swagger(DIR + 'swagger_specs/projects.yml')
    fields = docs['definitions'][-1]['schema']['properties']
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)

def test_community():
    rv = test_app.get('/reports/community/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    docs = get_swagger(DIR + 'swagger_specs/community.yml')
    fields = docs['definitions'][-1]['schema']['properties']
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)

def test_rewards():
    rv = test_app.get('/reports/rewards/')
    check_content_type(rv.headers)
    resp = get_json(rv)

    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    docs = get_swagger(DIR + 'swagger_specs/rewards.yml')
    fields = docs['definitions'][-1]['schema']['properties']
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)

def test_summary():
    rv = test_app.get('/reports/summary/')
    check_content_type(rv.headers)
    resp = get_json(rv)

    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    docs = get_swagger(DIR + 'swagger_specs/summary.yml')
    fields = docs['definitions'][-1]['schema']['properties']
    print('JSON:')
    print(set(resp.keys()))
    print('YML:')
    print(set(fields.keys()))
    print('DIFF:')
    print(set(resp.keys()) - set(fields.keys()))
    eq_(set(resp.keys()) , set(fields.keys()))
    eq_(rv.status_code, 200)

