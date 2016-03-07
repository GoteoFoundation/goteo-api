# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *

from . import test_app, check_content_type, get_json
from ..categories.resources import category_resource_fields

FILTERS = [
'',
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
def test_categories():
    for f in FILTERS:
        rv = test_app.get('/categories/' , query_string=f)
        check_content_type(rv.headers)
        resp = get_json(rv)

        fields = category_resource_fields
        if 'time-elapsed' in fields:
            del fields['time-elapsed']
        if 'time-elapsed' in resp:
            del resp['time-elapsed']

        eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
        eq_(rv.status_code, 200)

