# -*- coding: utf-8 -*-
import time
import pytz

from flask import jsonify

from config import config
from api import app


def get_lang(object, field, langs=[]):
    """Searchs langs alternatives on a object in the form of:
    {
        field:'original',
        field_en:'english translation',
        field_eu:'basque translation',
        ...
    }
    """
    for l in langs:
        if object[field + '_' + l]:
            return object[field + '_' + l]
    return object[field]

def image_url(img, size='large'):
    """
    Goteo image urls
    @size 'thumb', 'medium', 'large'
    """
    sizes = {'thumb' : '56x56c', 'medium' : '192x192c', 'large' : '512x512c'}

    s = sizes[size] if size in sizes else sizes['thumb']

    i = img if img is not None else 'la_gota.png'

    return 'http://goteo.org/img/' + s + '/' + i

def svg_image_url(img, type='licenses'):
    return 'http://goteoassets.org/api/svg/' + type + '/' + img

def utc_from_local(date_time, local_tz=None):
    assert date_time.__class__.__name__ == 'datetime'
    if local_tz is None:
        local_tz = pytz.timezone(config.timezone) # eg, "Europe/London"
    local_time = local_tz.localize(date_time)
    return local_time

#Error handling
def bad_request(message, code = 400):
    """Error handling json response"""
    resp = jsonify(message=str(message))
    resp.status_code = code
    return resp

# Generic percentage
def percent(number, base=None):
    """Porcentaje en base a un total"""
    if base is None:
        return 0
    if base == 0:
        return 0
    perc = float(number) / base * 100
    return round(perc, 2)


############################ debug ############################
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
