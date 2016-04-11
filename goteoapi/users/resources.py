# -*- coding: utf-8 -*-

import time
from flask import g
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import marshal, bad_request
from ..base_resources import BaseItem, BaseList, Response
from ..location.models import UserLocation
from .models import User

user_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "node"              : fields.String,
    "date_created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
    "profile_url"       : fields.String,
    "profile_image_url" : fields.String,
    # privacy concerns here
    # "latitude" : fields.Float,
    # "longitude" : fields.Float
}

user_full_resource_fields = user_resource_fields.copy()
# user_full_resource_fields["date_updated"] = fields.DateTime(dt_format='rfc822')

class UsersListAPI(BaseList):
    """User list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/user_list.yml')
    def get(self):
        res = self._get()

        if res.ret['items'] == []:
            return bad_request('No users to list', 404)

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

            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = User.total(**args)
        )

        return res



class UserOwnerAPI(BaseItem):
    """Authenticated User Details"""
    @requires_auth(scope='private')
    @ratelimit()
    # @swag_from('swagger_specs/user_item.yml')
    def get(self):
        res = UserAPI()._get(g.user.id)

        if res.ret['id'] == None:
            return bad_request('User not found', 404)

        return res.response()


class UserAPI(BaseItem):
    """User Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/user_item.yml')
    def get(self, user_id):
        res = self._get(user_id)

        if res.ret['id'] == None:
            return bad_request('User not found', 404)

        return res.response()

    def _get(self, user_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        u = User.get(user_id)

        item = marshal(u, user_full_resource_fields)
        if u != None and 'latitude' in user_full_resource_fields:
            location = UserLocation.get(u.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude

        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res

