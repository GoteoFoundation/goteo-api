# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *
import os

from goteoapi.tests import test_app, get_json, get_swagger

__import__('goteoapi_reports.controllers')

DIR = os.path.dirname(__file__) + '/'


def test_money():
    rv = test_app.get('/reports/money/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    # make sure we get a response
    eq_(rv.status_code, 200)
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    fields = get_swagger(DIR + 'swagger_specs/money.yml', 'Money')
    eq_(set(resp.keys()), set(fields.keys()))
    eq_(rv.status_code, 200)


def test_projects():
    rv = test_app.get('/reports/projects/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    fields = get_swagger(DIR + 'swagger_specs/projects.yml', 'Project')
    eq_(set(resp.keys()), set(fields.keys()))
    eq_(rv.status_code, 200)


def test_community():
    rv = test_app.get('/reports/community/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    fields = get_swagger(DIR + 'swagger_specs/community.yml', 'Community')
    eq_(set(resp.keys()), set(fields.keys()))
    eq_(rv.status_code, 200)


def test_rewards():
    rv = test_app.get('/reports/rewards/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)

    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    fields = get_swagger(DIR + 'swagger_specs/rewards.yml', 'Reward')
    eq_(set(resp.keys()), set(fields.keys()))
    eq_(rv.status_code, 200)


def test_summary():
    rv = test_app.get('/reports/summary/')
    eq_(rv.headers['Content-Type'], 'application/json')
    resp = get_json(rv)

    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    fields = get_swagger(DIR + 'swagger_specs/summary.yml', 'Summary')
    eq_(set(resp.keys()), set(fields.keys()))
    eq_(rv.status_code, 200)
