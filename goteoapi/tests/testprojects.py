# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
import json
from nose.tools import *

from . import app,test_app, check_content_type
from ..projects.resources import ProjectResponse as Response, ProjectsListResponse as ListResponse

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
def test_projects():
    for f in FILTERS:
        rv = test_app.get('/projects/' , query_string=f)
        check_content_type(rv.headers)
        resp = json.loads(rv.data)
        fields = ListResponse.resource_fields
        if 'time-elapsed' in fields:
            del fields['time-elapsed']
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)

def test_project_no_slash():
    rv = test_app.get('/projects/goteo')
    assert 'text/html' in rv.headers['Content-Type']
    assert 'location' in rv.headers, "%r not in %r" % ('location', rv.headers)
    assert '/projects/goteo/' in rv.headers['Location'], "%r not in %r" % ('/projects/goteo/', rv.headers['Location'])

def test_project():
    rv = test_app.get('/projects/160metros/')
    check_content_type(rv.headers)
    resp = json.loads(rv.data)
    fields = Response.resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)

