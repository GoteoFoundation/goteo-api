# -*- coding: utf-8 -*-
#

import time
from flask import jsonify
from flask.ext.restful import Resource, reqparse


class Response():
    """Base response for Reports Endpoints"""
    resource_fields = {}

    def __init__(self, attributes = {}, filters = {}, starttime = 0):
        self.ret = {}
        for var in self.resource_fields.keys():
            self.ret[var] = None
        for var, value in attributes.iteritems():
            if var in self.resource_fields:
                self.ret[var] = value

        self.ret['filters'] = {}
        for k, v in filters:
            if v is not None:
                self.ret['filters'][k] = v

        self.time_start = starttime


    def set(self, var, value):
        self.ret[var] = value;

    def response(self):
        if self.time_start != 0:
            self.ret['time-elapsed'] = time.time() - self.time_start
        return jsonify(self.ret)


class Base(Resource):
    """Base class for enpoint reports"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        self.reqparse.add_argument('category', type=str)
        self.reqparse.add_argument('location', type=str)
        super(Base, self).__init__()

    # Swagger specification
    RESPONSE_MESSAGES = [
        {
            "code": 400,
            "message": "Invalid parameters"
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
            "description": 'Filter by project location (Lat,lon,Radius in Km)',
            "required": False,
            "dataType": "string"
        }

    ]