# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from

from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import *

from ..base_resources import BaseItem, BaseList, Response
from .models import Invest
from ..users.resources import user_resource_fields
from ..location.models import InvestLocation

invest_resource_fields = {
    "id"             : fields.Integer,
    "owner"        : fields.String,
    "owner_name"        : fields.String,
    "project"        : fields.String,
    "call"        : fields.String,
    "amount"         : fields.Float,
    "status"         : fields.String,
    "method"         : fields.String,
    "currency"         : fields.String,
    "conversion_ratio"         : fields.Float,
    "anonymous"         : fields.Boolean,
    "resign"         : fields.Boolean,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
    "date_invested"  : fields.DateTime(dt_format='rfc822'),
    "date_charged"  : fields.DateTime(dt_format='rfc822'),
    "date_returned"  : fields.DateTime(dt_format='rfc822'),
}

class InvestsListAPI(BaseList):
    """Invest list"""

    @requires_auth()
    @ratelimit()
    # @swag_from('swagger_specs/call_list.yml')
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
            item['method'] = p.method_string
            location = InvestLocation.get(p.id)
            if location and not p.anonymous:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {  'items' : items,
                            'extra' : {
                                'pledged': float(Invest.pledged_total(**args)),
                                'refunded': float(Invest.refunded_total(**args)),
                                'projects': Invest.projects_total(**args)
                            }
                        },
            filters = args.items(),
            total = Invest.total(**args)
        )

        return res



class InvestAPI(BaseItem):
    """Invest Details"""

    @requires_auth()
    @ratelimit()
    # @swag_from('swagger_specs/call_item.yml')
    def get(self, call_id):
        res = self._get(call_id)

        if res.ret['id'] == None:
            return bad_request('Matchfunding not found', 404)

        return res.response()

    def _get(self, call_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Invest.get(call_id)

        item = marshal(p, call_full_resource_fields)
        if p != None:
            item['matchfund-url'] = call_url(p.id)
            item['description-short'] = p.subtitle
            item['status'] = p.status_string
            item['scope'] = p.scope_string
            item['image-url'] = image_url(p.image, 'medium', False)
            item['image-url-big'] = image_url(p.image, 'big', False)
            item['image-background'] = image_url(p.backimage, 'big', False)
            location = InvestLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, call_location_resource_fields)]
            translations = {}

        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res
