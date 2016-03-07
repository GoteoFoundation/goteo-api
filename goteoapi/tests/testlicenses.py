# -*- coding: utf-8 -*-
#
# Minimal tests for main routes
#
from nose.tools import *

from . import test_app, check_content_type, get_json
from ..licenses.resources import license_resource_fields

def test_licenses():
    rv = test_app.get('/licenses/')
    check_content_type(rv.headers)
    resp = get_json(rv)

    fields = license_resource_fields
    if 'time-elapsed' in fields:
        del fields['time-elapsed']
    if 'time-elapsed' in resp:
        del resp['time-elapsed']

    eq_(len(set(map(lambda x: str(x), resp.keys())) - set(fields.keys())) >= 0, True)
    eq_(rv.status_code, 200)


