# -*- coding: utf-8 -*-
#

import time
from datetime import datetime as dtdatetime
from dateutil.parser import parse
from flask import jsonify
from flask.ext.restful import Resource, reqparse

from .helpers import *
from . import app

def date_sanitizer(data):
    d = parse(data)
    if d > dtdatetime.now():
        d = dtdatetime.now()
    return str(d.date())

def lang_sanitizer(data):
    d = str(data)
    if len(data) != 2:
        raise Exception("Invalid parameter lang. 2 chars length required: (en, es, fr, pt, etc)")
    return d

def location_sanitizer(data):
    location = data.split(",")
    if len(location) != 3:
        raise Exception("Invalid parameter location. 3 parameters required: latitude,longitude,radius(km)")

    radius = int(location[2])
    if radius > 500 or radius < 0:
        raise Exception("Radius must be a value between 0 and 500 Km")
    return {'latitude':location[0], 'longitude':location[1], 'radius':radius}

def limit_sanitizer(limit):
    l = int(limit)
    if(l > 50):
        l = 50
    return l

class Response():
    """Base response for Reports Endpoints"""

    def __init__(self, attributes = {}, filters = {}, total = None, starttime = 0):
        self.ret = {}
        for var, value in attributes.items():
            self.ret[var] = value

        meta = {}
        if filters:
            for k, v in filters:
                if v is not None:
                    meta[k] = v
        if total is not None:
            meta['total'] = int(total)

        if meta:
            self.ret['meta'] = meta

        self.time_start = starttime
        # If debug?
        # self.ret['date'] = utc_from_local( dtdatetime.utcnow() )

    def set(self, var, value):
        self.ret[var] = value;

    def response(self, as_json = True):
        if self.time_start != 0:
            self.ret['time-elapsed'] = time.time() - self.time_start
        if as_json:
            return jsonify(self.ret)
        return self.ret

class BaseItem(Resource):
    """Base class for individual enpoint reports"""

    def __init__(self):
        super().__init__()

    def option(self):
        pass

class BaseList(Resource):
    """Base class for list enpoint reports"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=date_sanitizer)
        self.reqparse.add_argument('to_date', type=date_sanitizer)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        # TODO: buscar por nombre de categoria dependiendo de idioma
        self.reqparse.add_argument('category', type=int, action='append')
        self.reqparse.add_argument('location', type=location_sanitizer)
        self.reqparse.add_argument('page', type=int, default=0)
        self.reqparse.add_argument('limit', type=limit_sanitizer, default=10)
        self.reqparse.add_argument('lang', type=lang_sanitizer, action='append')

        super().__init__()

    def parse_args(self, remove=()):
        """Standard args parser santizizer
           returns a dict of arguments and values
        """
        if remove:
            for r in remove:
                self.reqparse.remove_argument(r)

        args = self.reqparse.parse_args()
        # limit lang length
        if 'lang' in args and args['lang'] is not None:
            langs = []
            for l in args['lang']:
                if app.config['DEFAULT_DB_LANG'] != l:
                    langs.append(l)

            args['lang'] = langs
            if langs is []:
                del args['lang']
            else:
                # 2 elements allowed only
                args['lang'] = args['lang'][:2]

        return args
