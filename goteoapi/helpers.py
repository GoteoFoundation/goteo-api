# -*- coding: utf-8 -*-
import datetime
import pytz
from flask import jsonify
from flask.ext.restful import marshal as s_marshal

from . import app

def marshal(data, fields, envelope=None):
    """
    Processes a dictionary with values as described in
    http://flask-restful-cn.readthedocs.org/en/latest/api.html#flask_restful.marshal

    and changes all underscore symbol (_) to hyphen symbol (-)
    """
    if isinstance(data, (list, tuple)):
        return [marshal(d, fields, envelope) for d in data]
    m = s_marshal(data, fields, envelope)
    if isinstance(m, dict):
        return { k.replace("_", "-"): v for k, v in m.items() }
    return m

def get_lang(obj, field, langs=[]):
    """
    Searches alternatives langs on a object in the form of:
    {
        field:'original',
        field_en:'english translation',
        field_eu:'basque translation',
        ...
    }
    """
    if langs:
        for l in langs:
            if type(obj) == dict:
                val = obj[field + '_' + l]
            else:
                val = getattr(obj, field + '_' + l)
            if val:
                return val

    if type(obj) == dict:
        return obj[field]
    else:
        return getattr(obj, field)

def image_url(img, size='medium', cut=False, default='la_gota.png'):
    """
    Goteo image urls
    @size 'thumb', 'medium', 'large'
    """
    sizes = ('icon', 'thumb', 'medium', 'large', 'big')

    s = size if size in sizes else 'medium'
    if cut:
        s += 'c'
    i = img if img is not None else default

    return 'https://goteo.org/img/' + s + '/' + i

def image_resource_url(url):
    """Links for images"""
    if url:
        if url.startswith('http') and '://' in url:
            return url
        if url.startswith('goteo.org'):
            return 'http://' + url
        if not url.startswith('/'):
            url = '/' + url
        return 'http://goteo.org' + url
    return None

def project_url(project_id):
    return 'https://goteo.org/project/' + project_id

def call_url(call_id):
    return 'https://goteo.org/call/' + call_id

def project_widget_url(project_id):
    return 'https://goteo.org/widget/project/' + project_id

def user_url(user_id):
    return 'https://goteo.org/user/profile/' + user_id

def svg_image_url(img, type='licenses'):
    return 'https://goteoassets.org/api/svg/' + type + '/' + img


def utc_from_local(date_time, local_tz=None):
    local_time = None
    if date_time.__class__.__name__ == 'date':
        date_time = datetime.datetime(*(date_time.timetuple()[:6]))

    # assert date_time.__class__.__name__ == 'datetime'

    if date_time.__class__.__name__ != 'datetime':
        return date_time
    if local_tz is None:
        local_tz = pytz.timezone(app.config['TIMEZONE']) # eg, "Europe/London"
    local_time = local_tz.localize(date_time)

    return local_time

#Error handling
def bad_request(message, code = 400):
    """Error handling json response"""
    resp = jsonify(message=str(message), error = code)
    resp.status_code = code
    return resp

# Generic percentage
def percent(number, base=None):
    """Fload percent number"""
    if base is None:
        return 0
    if base == 0:
        return 0
    perc = float(number) / base * 100
    return round(perc, 2)

