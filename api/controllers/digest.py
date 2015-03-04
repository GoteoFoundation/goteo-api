# -*- coding: utf-8 -*-

import time

from flask import jsonify
from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from dateutil.parser import parse
import calendar
from datetime import date
from api.decorators import *
from api.base_endpoint import BaseList, Response
from api.helpers import parse_args
#import current endpoints
from api.reports.money import *
from api import app

def year_sanitizer(data):
    d = parse(data)
    return str(d.year)

@swagger.model
class DigestResponse(Response):
    """DigestResponse, here just for swagger documentation
    final Responses will be the related endpoints"""

    resource_fields = {
    }

    required = resource_fields.keys()


@swagger.model
@swagger.nested(**{
                'response' : DigestResponse.__name__,
                }
            )
class DigestsListResponse(Response):
    """DigestsListResponse"""

    resource_fields = {
        "global"    : fields.Nested(DigestResponse.resource_fields),
        "buckets"    : fields.List(fields.Nested(DigestResponse.resource_fields)),
        'endpoint' : fields.String
    }

    required = resource_fields.keys()


class DigestsListAPI(BaseList):
    """Get Digest list"""
    AVAILABLE_ENDPOINTS = {
        'reports/money' : 'reports.money.MoneyAPI',
        'categories' : 'controllers.category.CategoriesListAPI'
        }

    @swagger.operation(
        notes='Digests list',
        nickname='digests',
        responseClass=DigestsListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, endpoint):
        """Get the digests list
        <a href="http://developers.goteo.org/doc/digests">developers.goteo.org/doc/digests</a>
        """
        time_start = time.time()
        self.reqparse.add_argument('year', type=year_sanitizer, default=datetime.today().year)
        #removing not-needed standard filters
        args = self.parse_args(('from_date', 'to_date'))

        # get the class
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
        endpoint = '/'.join(endpoint.split('/')[:2])

        if endpoint in self.AVAILABLE_ENDPOINTS:
            mod = __import__('api')
            parts =  self.AVAILABLE_ENDPOINTS[endpoint].split('.')
            for att in parts:
                mod = getattr(mod, att)
        try:
            # global data, construct from_date >> to_date
            instance = mod()
            instance.json = False # we don't want jsonify the response
        except Exception:
            return bad_request('Endpoint error. Try some allowed endpoint to digest.', 404)

        try:
            #arguments for the global response
            year = args['year']
            [args['from_date'], args['to_date']] = self.max_min(year)
            del args['year']
            instance.parse_args = (lambda **a:self.dummy_parse_args(args, **a))
            # get year

            global_ = instance.get()
            # cleaning response
            # del global_['time-elapsed']
            buckets = {}
            # All months in different buckets
            for month in range(1,13):
                [args['from_date'], args['to_date']] = self.max_min(year, month)
                buckets[format(month, '02')] = instance.get()

        except Exception as e:
            return bad_request('Unexpected error. [{0}]'.format(e), 400)

        if global_ == []:
            return bad_request('No digests to list.', 404)

        res = DigestsListResponse(
            starttime = time_start,
            attributes = {'global' : global_, 'buckets' : buckets, 'endpoint' : endpoint },
            filters = args.items()
        )

        return res.response(self.json)

    def dummy_parse_args(self, old_args, remove=()):
        new_args = {}
        for k in old_args:
            if remove:
                if k in remove:
                    continue
            new_args[k] = old_args[k]
        return new_args

    def max_min(self, year, month=None):
        """Returns a lower date and a upper date from year or month"""
        start_month=month
        if month is None:
            start_month=1
            month=12
        month = int(month)
        start_month = int(start_month)
        year = int(year)
        max_ = calendar.monthrange(year, month)[1]
        return (
                date(year,start_month,1).isoformat(),
                date(year,month,max_).isoformat()
                )