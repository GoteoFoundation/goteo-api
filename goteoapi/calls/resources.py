# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from

from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import *

from ..base_resources import BaseItem, BaseList, Response
from .models import Call, CallLang
from ..users.resources import user_resource_fields
from ..projects.resources import project_resource_fields
from ..projects.models import Project
from ..invests.models import Invest
from ..location.models import CallLocation, ProjectLocation, location_resource_fields

call_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description_short" : fields.String,
    "date_opened"      : DateTime,
    "date_published"    : DateTime,
    "date_succeeded"    : DateTime,
    "call_url"       : fields.String,
    "logo_url" : fields.String,
    "image_url" : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
    "region" : fields.String,
    "call_location" : fields.String,
    "owner" : fields.String,
    "owner_name" : fields.String,
    "amount_available" : fields.Float,
    "amount_peers" : fields.Float,
    "amount_committed" : fields.Float,
    "amount_remaining" : fields.Float,
    "projects_total" : fields.Integer,
    "projects_applied" : fields.Integer,
    "projects_active" : fields.Integer,
    "projects_succeeded" : fields.Integer,
    "status" : fields.String,
}

call_full_resource_fields = call_resource_fields.copy()
call_full_resource_fields.pop('latitude')
call_full_resource_fields.pop('region')
call_full_resource_fields.pop('longitude')
call_full_resource_fields["description"]      = fields.String
call_full_resource_fields["legal"]            = fields.String
call_full_resource_fields["whom"]             = fields.String
call_full_resource_fields["applies"]          = fields.String
call_full_resource_fields["dossier"]          = fields.String
call_full_resource_fields["tweet"]            = fields.String
call_full_resource_fields["resources"]        = fields.String
call_full_resource_fields["date_closed"]      = DateTime
call_full_resource_fields["image_url_big"]    = fields.String
call_full_resource_fields["image_background_url"] = fields.String
call_full_resource_fields["facebook_url"]     = fields.String
call_full_resource_fields["user"]             = fields.Nested(user_resource_fields)
call_full_resource_fields["location"]         = fields.List(fields.Nested(location_resource_fields))


call_project_resource_fields = project_resource_fields.copy()
call_project_resource_fields['amount_call'] = fields.Float

class CallsListAPI(BaseList):
    """Call list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/call_list.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()

        items = []
        for p in Call.list(**args):
            item = marshal(p, call_resource_fields)
            item['status'] = p.status_string
            location = CallLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                item['region'] = location.region if location.region != '' else location.country
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Call.total(**args)
        )

        return res



class CallAPI(BaseItem):
    """Call Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/call_item.yml')
    def get(self, call_id):
        res = self._get(call_id)

        if res.ret['id'] == None:
            return bad_request('Matchfunding call not found', 404)

        return res.response()

    def _get(self, call_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Call.get(call_id)

        item = marshal(p, call_full_resource_fields)
        if p != None:
            item['status'] = p.status_string
            item['scope'] = p.scope_string
            location = CallLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, location_resource_fields)]
            translations = {}
            translate_keys = {k: v for k, v in call_full_resource_fields.items() if k in CallLang.get_translate_keys()}
            for k in p.translations:
                translations[k.lang] = marshal(k, translate_keys)
                translations[k.lang]['description-short'] = k.subtitle
            item['translations'] = translations

        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res

class CallProjectsListAPI(BaseList):
    """Projects list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/call_projects.yml')
    def get(self, call_id):
        res = self._get(call_id)

        if res.ret['id'] == None:
            return bad_request('Call not found', 404)

        return res.response()

    def _get(self, call_id):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()
        args['call'] = call_id

        items = []
        if Call.get(call_id) == None:
            return Response(attributes = {'id': None})

        for p in Project.list(**args):
            item = marshal(p, call_project_resource_fields)
            item['status'] = p.status_string
            item['amount-call'] = float(Invest.pledged_total(project=p.id, call=call_id))
            item['image-url'] = image_url(p.image, 'medium', False)
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                item['region'] = location.region if location.region != '' else location.country
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'id':call_id, 'items' : items},
            filters = args.items(),
            total = Project.total(**args)
        )

        return res
