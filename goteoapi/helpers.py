# -*- coding: utf-8 -*-
import datetime
import pytz
from calendar import timegm
from email.utils import formatdate
from flask import jsonify
from flask.ext.restful import marshal as s_marshal
from flask.ext.restful.fields import Raw, MarshallingException

from . import app

# ##################
# Model helpers
# ################


# Helper class to convert a dict to a generic object
class objectview(object):
    def __init__(self, d):
        self.__dict__ = d


def get_lang(obj, field, langs=[], root_lang=app.config['DEFAULT_DB_LANG']):
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
            prop = field + '_' + l
            if l == root_lang:
                prop = field
            if type(obj) == dict:
                val = obj[prop]
            else:
                val = getattr(obj, prop)
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
    """Translates a date according the timezone in settings"""
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

# Field processing helpers

# ##################
# Resource helpers
# ##################


def bad_request(message, code=400):
    """Error handling json response"""
    resp = jsonify(message=str(message), error=code)
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


def marshal(data, fields, envelope=None, remove_null=False):
    """
    Processes a dictionary with values as described in
    http://flask-restful-cn.readthedocs.org/en/latest/api.html#flask_restful.marshal

    and changes all underscore symbol (_) to hyphen symbol (-)
    """
    if isinstance(data, (list, tuple)):
        return [marshal(d, fields, envelope, remove_null) for d in data]
    m = s_marshal(data, fields, envelope)
    if isinstance(m, dict):
        return {k.replace("_", "-"): v for k, v in m.items() if not remove_null or v is not None}
    return m


# Customized filelds for the API

class Date(Raw):
    """
    Plain date format as YYYY-MM-DD (ISO 8601 or RFC822) only the date part
    """
    def __init__(self, dt_format='rfc822', **kwargs):
        super(Date, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        try:
            if self.dt_format == 'rfc822':
                date = datetime.datetime(*(value.timetuple()[:3]))
                return date.strftime("%a, %d %b %Y")
            elif self.dt_format == 'iso8601':
                date = datetime.datetime(*(value.timetuple()[:3]))
                return datetime.date.isoformat(date)
        except ValueError as ve:
            raise MarshallingException(ve)


class DateTime(Raw):
    """
    Customized version of DateTime described in
    http://flask-restful-cn.readthedocs.org/en/0.3.5/api.html#module-fields

    Added: localtime as default for rfc822 format
    Return a formatted datetime string in UTC. Supported formats are RFC 822
    and ISO 8601.

    See :func:`email.utils.formatdate` for more info on the RFC 822 format.

    See :meth:`datetime.datetime.isoformat` for more info on the ISO 8601
    format.

    :param dt_format: ``'rfc822'`` or ``'iso8601'``
    :type dt_format: str
    """
    def __init__(self, dt_format='rfc822', localtime=True, **kwargs):
        super(DateTime, self).__init__(**kwargs)
        self.dt_format = dt_format
        self.localtime = localtime

    def format(self, value):
        try:
            if self.dt_format == 'rfc822':
                return formatdate(timegm(value.utctimetuple()), localtime=self.localtime)
            elif self.dt_format == 'iso8601':
                return value.isoformat()
            else:
                raise MarshallingException(
                    'Unsupported date format %s' % self.dt_format
                )
        except AttributeError as ae:
            raise MarshallingException(ae)
