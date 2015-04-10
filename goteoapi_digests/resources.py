# -*- coding: utf-8 -*-

import time
from dateutil.parser import parse
import calendar
from datetime import date as dtdate, datetime as dtdatetime

from flask.ext.restful import fields
from flask_restful_swagger import swagger

#import current endpoints
from goteoapi.decorators import *
from goteoapi.base_resources import BaseList, Response
from goteoapi import app

def year_sanitizer(data):
    d = parse(data)
    if d > dtdatetime.now():
        raise Exception("Invalid parameter year")
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
    #TODO: configurable
    AVAILABLE_ENDPOINTS = [
        '/reports/summary/',
        '/reports/money/',
        '/reports/community/',
        '/reports/projects/',
        '/reports/rewards/',
        '/categories/',
        '/licenses/'
        ]

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
        self.reqparse.add_argument('year', type=year_sanitizer, default=None)
        #removing not-needed standard filters
        args = self.parse_args(remove=('from_date', 'to_date', 'limit', 'page'))
        # get the class
        if endpoint[-1] != '/':
            endpoint = endpoint + '/'
        endpoint = '/' + endpoint
        # endpoint = '/'.join(endpoint.split('/')[:2])
        mod = None
        try:
            for rule in app.url_map.iter_rules():
                if rule.rule in self.AVAILABLE_ENDPOINTS and rule.rule == endpoint:
                    # Find the Class
                    pack = app.view_functions[rule.endpoint].__dict__['view_class'].__module__
                    clas = app.view_functions[rule.endpoint].__dict__['view_class'].__name__
                    parts = pack.split('.')
                    parts.append(clas)
                    mod = __import__(parts[0])
                    for att in parts[1:]:
                        mod = getattr(mod, att)

            # global data, construct from_date >> to_date
            instance = mod()
        except Exception as e:
            if app.debug:
                return bad_request('Endpoint error. Try some allowed endpoint to digest. {0}'.format(str(e)), 404)
            return bad_request('Endpoint error. Try some allowed endpoint to digest.', 404)

        buckets = {}
        try:
            #arguments for the global response
            year = args['year']
            if year is not None:
                del args['year']
                # digest by months in the specified year
                # Assign date filters
                [args['from_date'], args['to_date']] = map(lambda d:d.isoformat(),self.max_min(year))
                for month in range(1,13):
                    maxmin = self.max_min(year, month)
                    if maxmin[0] < maxmin[1]:
                        buckets[format(month, '02')] = map(lambda d:d.isoformat(),maxmin)
            else:
                # digest by years
                for year in range(app.config['INITIAL_YEAR'], dtdate.today().year + 1):
                    buckets[year] = map(lambda d:d.isoformat(),self.max_min(year))

            # parse the args in the instance
            instance.parse_args = (lambda **a:self.dummy_parse_args(args, **a))
            # # data for global dates
            global_ = instance._get().response(False)
            # cleaning response
            # del global_['time-elapsed']
            # All months/years in different buckets
            for part in buckets:
                [args['from_date'], args['to_date']] = buckets[part]
                buckets[part] = instance._get().response(False)

            #aditional cleaning
            if 'from_date' in args:
                del args['from_date']
            if 'to_date' in args:
                del args['to_date']

        except Exception as e:
            return bad_request('Unexpected error. [{0}]'.format(e), 400)
            pass

        if global_ == []:
            return bad_request('No digests to list.', 404)

        res = DigestsListResponse(
            starttime = time_start,
            attributes = {'global' : global_, 'buckets' : buckets, 'endpoint' : endpoint },
            filters = args.items()
        )

        return res.response()

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

        d_min = dtdate(int(year), int(start_month), 1)
        d_max = dtdate(int(year), int(month), calendar.monthrange(int(year), int(month))[1])

        d_min = dtdate.today() if d_min > dtdate.today() else d_min
        d_max = dtdate.today() if d_max > dtdate.today() else d_max
        return (d_min, d_max)
