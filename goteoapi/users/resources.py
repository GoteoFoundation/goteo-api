# -*- coding: utf-8 -*-

import time
from flask import g
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..ratelimit import ratelimit
from ..helpers import *
from ..auth.decorators import requires_auth
from ..helpers import marshal, bad_request
from ..base_resources import BaseItem, BaseList, Response
from ..location.models import UserLocation
from .models import User, UserLang

user_resource_fields = {
    "id": fields.String,
    "name": fields.String,
    "node": fields.String,
    "date_created": DateTime,
    "profile_url": fields.String,
    "profile_image_url": fields.String,
    # privacy concerns here
    # "latitude": fields.Float,
    # "longitude": fields.Float
    # "region": fields.String
}

user_full_resource_fields = user_resource_fields.copy()
user_full_resource_fields['about'] = fields.String
user_full_resource_fields['lang'] = fields.String
user_full_resource_fields['amount_public_invested'] = fields.Float
user_full_resource_fields['projects_public_invested'] = fields.Integer
user_full_resource_fields['projects_published'] = fields.Integer
user_full_resource_fields['projects_collaborated'] = fields.Integer
# TODO: extra field for Oauth Auth only with enough privileges
# user_full_resource_fields['amount_private_invested'] = fields.Float
# user_full_resource_fields['projects_private_invested'] = fields.Integer


class UsersListAPI(BaseList):
    """User list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/user_list.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        # For privacy, removing location filter ?
        args = self.parse_args(remove=('location'))

        items = []
        for u in User.list(**args):
            item = marshal(u, user_resource_fields)
            if 'latitude' in user_resource_fields:
                location = UserLocation.get(u.id)
                if location:
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude
                    if location.region:
                        item['region'] = location.region
                    else:
                        item['region'] = location.country

            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={'items': items},
            filters=args.items(),
            total=User.total(**args)
        )

        return res


class UserOwnerAPI(BaseItem):
    """Authenticated User Details"""
    @requires_auth(scope='private')
    @ratelimit()
    # @swag_from('swagger_specs/user_item.yml')
    def get(self):
        res = UserAPI()._get(g.user.id)

        if res.ret['id'] is None:
            return bad_request('User not found', 404)

        return res.response()


class UserAPI(BaseItem):
    """User Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/user_item.yml')
    def get(self, user_id):
        res = self._get(user_id)

        if res.ret['id'] is None:
            return bad_request('User not found', 404)

        return res.response()

    def _get(self, user_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        u = User.get(user_id)

        item = marshal(u, user_full_resource_fields)
        if u is not None:
            if 'latitude' in user_full_resource_fields:
                location = UserLocation.get(u.id)
                if location:
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude
                    if location.region:
                        item['region'] = location.region
                    else:
                        item['region'] = location.country

            translations = {}
            translate_keys = {
                k: v for k, v in user_full_resource_fields.items()
                if k in UserLang.get_translate_keys()
            }
            for k in u.Translations:
                translations[k.lang] = marshal(k, translate_keys)
            item['translations'] = translations

        res = Response(
            starttime=time_start,
            attributes=item
        )

        return res
