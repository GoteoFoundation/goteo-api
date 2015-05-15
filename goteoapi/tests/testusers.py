# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from . import app,test_app, check_content_type
from ..users.resources import UserResponse as Response, UsersListResponse as ListResponse

app.config['AUTH_ENABLED'] = False
FILTERS = [
'page=0',
'limit=1',
'page=1&limit=1',
'lang=ca&lang=fr',
'category=2',
'node=barcelona',
'from_date=2014-01-01',
'to_date=2014-12-31',
'from_date=2014-01-01&to_date=2014-12-31',
'location=41.38879,2.15899,50',
'location=41.38879,2.15899,50&from_date=2014-01-01',
'location=41.38879,2.15899,50&to_date=2014-12-31',
'location=41.38879,2.15899,50&from_date=2014-01-01&to_date=2014-12-31'
]
def test_users():
    for f in FILTERS:
        rv = test_app.get('/users/' , query_string=f)
        check_content_type(rv.headers)
        resp = json.loads(rv.data)
        print resp
        fields = ListResponse.resource_fields
        if 'time-elapsed' in fields:
            del fields['time-elapsed']
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)

# def test_user():
#     rv = test_app.get('/users/goteo/')
#     check_content_type(rv.headers)
#     resp = json.loads(rv.data)
#     print resp
#     fields = Response.resource_fields
#     if 'time-elapsed' in fields:
#         del fields['time-elapsed']
#     if 'time-elapsed' in resp:
#         del resp['time-elapsed']

#     eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
#     eq_(rv.status_code, 200)

