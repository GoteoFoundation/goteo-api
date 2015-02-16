# -*- coding: utf-8 -*-
#

import time
from dateutil.parser import *

from flask import jsonify
from flask.ext.restful import Resource, reqparse
from helpers import *

from api import db
from api.models import Location

def date_sanitizer(data):
    d = parse(data)
    return str(d.date())

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
    resource_fields = {}

    def __init__(self, attributes = {}, filters = {}, total = 0, starttime = 0):
        self.ret = {}
        for var in self.resource_fields.keys():
            self.ret[var] = None
        for var, value in attributes.iteritems():
            if var in self.resource_fields:
                self.ret[var] = value

        meta = {}
        if filters:
            for k, v in filters:
                if v is not None:
                    meta[k] = v
        if total:
            meta['total'] = int(total)

        if meta:
            self.ret['meta'] = meta

        self.time_start = starttime
        # If debug?
        # self.ret['date'] = utc_from_local( datetime.utcnow() )

    def set(self, var, value):
        self.ret[var] = value;

    def response(self):
        if self.time_start != 0:
            self.ret['time-elapsed'] = time.time() - self.time_start
        return jsonify(self.ret)

class BaseItem(Resource):
    """Base class for individual enpoint reports"""

    def __init__(self):
        super(BaseItem, self).__init__()

    # For Swagger specification
    RESPONSE_MESSAGES = [
        {
            "code": 404,
            "message": "Item not found"
        }
    ]

    INPUT_FILTERS = []

class BaseList(Resource):
    """Base class for list enpoint reports"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=date_sanitizer)
        self.reqparse.add_argument('to_date', type=date_sanitizer)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        self.reqparse.add_argument('category', type=str)
        self.reqparse.add_argument('location', type=location_sanitizer)
        self.reqparse.add_argument('page', type=int, default=0)
        self.reqparse.add_argument('limit', type=limit_sanitizer, default=10)

        super(BaseList, self).__init__()

    #Get location ids
    ## TODO:
    #  Do a first "cut" before getting results from the mysql table
    #  as described here:
    #  http://www.movable-type.co.uk/scripts/latlong-db.html
    #
    def location_ids(self, latitude, longitude, radius):
        from geopy.distance import VincentyDistance

        locations = db.session.query(Location.id, Location.latitude, Location.longitude).all()
        locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= radius, locations)
        location_ids = map(lambda l: int(l[0]), locations)

        return location_ids

    # For Swagger specification
    RESPONSE_MESSAGES = [
        {
            "code": 400,
            "message": "Invalid parameters"
        },
        {
            "code": 404,
            "message": "Item not found"
        }
    ]

    INPUT_FILTERS = [
        {
            "paramType": "query",
            "name": "project",
            "description": "Filter by individual project(s) separated by commas",
            "required": False,
            "dataType": "string",
            "allowMultiple": True
        },
        {
            "paramType": "query",
            "name": "from_date",
            "description": 'Filter from date. Ex. "2013-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "to_date",
            "description": 'Filter until date.. Ex. "2014-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "node",
            "description": 'Filter by individual node(s) separated by commas',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "category",
            "description": 'Filter by project category',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "location",
            "description": 'Filter by project location (Latitude,longitude,Radius in Km)',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "page",
            "description": 'Page number (starting at 1) if the result can be paginated',
            "required": False,
            "dataType": "integer"
        },
        {
            "paramType": "query",
            "name": "limit",
            "description": 'Page limit (maximum 50 results, defaults to 10) if the result can be paginated',
            "required": False,
            "dataType": "integer"
        },

    ]