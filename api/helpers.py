# -*- coding: utf-8 -*-
import time
import datetime
import pytz

from flask import jsonify

from config import config
from api import app

def parse_args(parser):
    """Standard args parser santizizer"""
    args = parser.parse_args()
    # limit lang length
    if 'lang' in args and args['lang'] is not None:
        langs = []
        for l in args['lang']:
            if config.default_db_lang != l:
                langs.append(l)

        args['lang'] = langs
        if langs is []:
            del args['lang']
        else:
            # 2 elements allowed only
            args['lang'] = args['lang'][:2]

    return args

def get_lang(object, field, langs=[]):
    """Searchs langs alternatives on a object in the form of:
    {
        field:'original',
        field_en:'english translation',
        field_eu:'basque translation',
        ...
    }
    """
    if langs:
        for l in langs:
            if object[field + '_' + l]:
                return object[field + '_' + l]
    return object[field]

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

    return 'http://goteo.org/img/' + s + '/' + i

def project_url(project_id):
    return 'http://goteo.org/project/' + project_id

def svg_image_url(img, type='licenses'):
    return 'http://goteoassets.org/api/svg/' + type + '/' + img

def utc_from_local(date_time, local_tz=None):
    local_time = None
    if date_time.__class__.__name__ == 'date':
        date_time = datetime.datetime(*(date_time.timetuple()[:6]))

    if date_time.__class__.__name__ != 'datetime':
        return date_time
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
