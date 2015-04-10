# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from goteoapi import app
app.debug = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['AUTH_ENABLED'] = False

test_app = app.test_client()

__import__('goteoapi_reports.controllers')

def check_content_type(headers):
  eq_(headers['Content-Type'], 'application/json')


def test_money():
    from .money import MoneyResponse
    rv = test_app.get('/reports/money/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    #make sure we get a response
    eq_(rv.status_code, 200)

    resp = json.loads(rv.data)
    fields = MoneyResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())), 0)
    eq_(rv.status_code, 200)

def test_projects():
    from .projects import ProjectsResponse
    rv = test_app.get('/reports/projects/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    fields = ProjectsResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())), 0)
    eq_(rv.status_code, 200)

def test_community():
    from .community import CommunityResponse
    rv = test_app.get('/reports/community/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    fields = CommunityResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)

def test_rewards():
    from .rewards import RewardsResponse
    rv = test_app.get('/reports/rewards/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)

    fields = RewardsResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)

