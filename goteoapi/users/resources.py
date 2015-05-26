# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from ..decorators import *
from ..base_resources import BaseItem, BaseList, Response
from ..location.models import ProjectLocation, UserLocation

from .models import User

@swagger.model
class UserResponse(Response):
    """UserResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "profile-url"       : fields.String,
        "profile-image-url" : fields.String,
        "latitude" : fields.Float,
        "longitude" : fields.Float,
    }

    required = resource_fields.keys()


@swagger.model
class UserCompleteResponse(Response):
    """UserCompleteResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'),
        # "date-updated"    : fields.DateTime(dt_format='rfc822'),
        "profile-url"       : fields.String,
        "profile-image-url" : fields.String,
        "latitude" : fields.Float,
        "longitude" : fields.Float,
    }

    required = resource_fields.keys()

@swagger.model
@swagger.nested(**{
                'items' : UserResponse.__name__,
                }
            )
class UsersListResponse(Response):
    """UsersListResponse"""

    resource_fields = {
        "items"         : fields.List(fields.Nested(UserResponse.resource_fields)),
    }

    required = resource_fields.keys()


class UsersListAPI(BaseList):
    """Get User list"""


    @swagger.operation(
        notes='Users list',
        nickname='users',
        responseClass=UsersListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the users list
        <a href="http://developers.goteo.org/doc/users">developers.goteo.org/doc/users</a>
        """
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
            item = marshal(u, UserResponse.resource_fields)
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
            location = UserLocation.get(u.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude

            items.append( item )

        res = UsersListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = User.total(**args)
        )

        return res



class UserAPI(BaseItem):
    """Get User Details"""

    @swagger.operation(
        notes='User profile',
        nickname='user',
        responseClass=UserCompleteResponse.__name__,
        responseMessages=BaseItem.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, user_id):
        """Get a user details
        <a href="http://developers.goteo.org/users#user">developers.goteo.org/users#user</a>
        """
        res = self._get(user_id)

        if res.ret['id'] == None:
            return bad_request('User not found', 404)

        return res.response()

    def _get(self, user_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        u = User.get(user_id)
        item = marshal(u, UserCompleteResponse.resource_fields)
        if u != None:
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
            location = UserLocation.get(u.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude

        res = UserCompleteResponse(
            starttime = time_start,
            attributes = item
        )

        return res

