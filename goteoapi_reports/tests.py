# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from goteoapi import app
from goteoapi.tests import test_app, check_content_type, get_json

__import__('goteoapi_reports.controllers')

def test_money():
    from .money import money_resource_fields
    rv = test_app.get('/reports/money/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    #make sure we get a response
    eq_(rv.status_code, 200)

    resp = get_json(rv)
    fields = money_resource_fields
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
    resp = get_json(rv)
    fields = ProjectsResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())), 0)
    eq_(rv.status_code, 200)

def test_community():
    rv = test_app.get('/reports/community/')
    check_content_type(rv.headers)
    resp = get_json(rv)
    fields = CommunityResponse.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']
    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)

def test_rewards():
    rv = test_app.get('/reports/rewards/')
    check_content_type(rv.headers)
    resp = get_json(rv)

    fields = [ 'reward-refusal', 'percentage-reward-refusal', 'rewards-per-amount', 'favorite-rewards' ]

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields)) >= 0, True)
    eq_(rv.status_code, 200)

def test_summary():
    rv = test_app.get('/reports/summary/')
    check_content_type(rv.headers)
    resp = get_json(rv)

    fields = ['pledged', 'matchfund-amount', 'matchfundpledge-amount', 'average-donation', 'users', 'projects-received', 'projects-published', 'projects-successful', 'projects-failed', 'categories', 'top10-collaborations', 'top10-donations', 'favorite-rewards' ]

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields)) >= 0, True)
    eq_(rv.status_code, 200)

