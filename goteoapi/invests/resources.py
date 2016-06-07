# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from

from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import *

from ..base_resources import BaseItem, BaseList, Response
from .models import Invest
# from ..users.resources import user_resource_fields
from ..location.models import InvestLocation, location_resource_fields


def type_sanitizer(type):
    if type not in ('drop', 'payment', 'pool'):
        raise Exception("Invalid parameter type. Only types 'drop', 'payment' or 'pool' are allowed")
    return str(type)

invest_resource_fields = {
    "id": fields.Integer,
    # Privacy concerns here...
    # "owner": fields.String,
    # "owner_name": fields.String,
    # "anonymous": fields.Boolean,
    "type": fields.String,
    "project": fields.String,
    "call": fields.String,
    "amount": fields.Float,
    "status": fields.String,
    "currency": fields.String,
    "conversion_ratio": fields.Float,
    "resign": fields.Boolean,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "region": fields.String,
    "date_created": DateTime,
    "date_charged": DateTime,
    "date_returned": DateTime,
    "date_updated": DateTime,
}

invest_full_resource_fields = invest_resource_fields.copy()
invest_full_resource_fields.pop('latitude')
invest_full_resource_fields.pop('longitude')
invest_full_resource_fields["location"] = fields.List(fields.Nested(location_resource_fields))


class InvestsListAPI(BaseList):
    """Invest list"""

    def __init__(self):

        super().__init__()
        # Additional filters for this endpoint
        self.reqparse.add_argument('call', type=str, action='append')
        self.reqparse.add_argument('type', type=type_sanitizer)

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/invest_list.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()

        items = []
        for p in Invest.list(**args):
            item = marshal(p, invest_resource_fields)
            item['status'] = p.status_string
            item['project'] = p.project_id
            if 'latitude' in invest_resource_fields:
                location = InvestLocation.get(p.id)
                if location and not p.anonymous:
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude
                    item['region'] = location.region if location.region != '' else location.country
            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={
                'items': items,
                'extra': {
                    'pledged': float(Invest.pledged_total(**args)),
                    'refunded': float(Invest.refunded_total(**args)),
                    'projects': Invest.projects_total(**args),
                    'calls': Invest.calls_total(**args)
                }
            },
            filters=args.items(),
            total=Invest.total(**args)
        )

        return res


class InvestAPI(BaseItem):
    """Invest Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/invest_item.yml')
    def get(self, invest_id):
        res = self._get(invest_id)

        if not res.ret['id']:
            return bad_request('Invest not found', 404)

        return res.response()

    def _get(self, invest_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Invest.get(invest_id)

        item = marshal(p, invest_full_resource_fields)
        if p is not None:
            item['status'] = p.status_string
            item['project'] = p.project_id
            if 'user' in invest_full_resource_fields:
                if p.anonymous:
                    item['user'] = None
            if 'location' in invest_full_resource_fields:
                location = InvestLocation.get(p.id)
                if location:
                    item['location'] = [marshal(location, location_resource_fields)]

        res = Response(
            starttime=time_start,
            attributes=item
        )

        return res
