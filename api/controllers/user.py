# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from api.models.user import User
from api.decorators import *
from api.base_endpoint import BaseItem, BaseList, Response


@swagger.model
class UserResponse(Response):
    """UserResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
        "node"         : fields.String,
        "date-created"         : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "profile-image-url"         : fields.String,
    }

    required = resource_fields.keys()


@swagger.model
class UserCompleteResponse(Response):
    """UserCompleteResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
        "node"         : fields.String,
        "date-created"         : fields.DateTime(dt_format='rfc822'),
        # "date_updated"         : fields.DateTime(dt_format='rfc822'),
        "profile-image-url"         : fields.String,
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
        <a href="http://developers.goteo.org/users#list">developers.goteo.org/users#list</a>
        """
        time_start = time.time()
        args = self.reqparse.parse_args()
        items = []
        for u in User.list(**args):
            item = marshal(u, UserResponse.resource_fields)
            item['date-created'] = u.date_created
            item['profile-image-url'] = u.profile_image_url
            items.append( item )

        res = UsersListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = User.total(**args)
        )
        if items == []:
            return bad_request('No users to list', 404)

        return res.response()




class UserAPI(BaseItem):
    """Get User Details"""

    @swagger.operation(
        notes='User profile',
        nickname='user',
        responseClass=UserResponse.__name__,
        responseMessages=BaseItem.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, id):
        """Get a user details
        <a href="http://developers.goteo.org/users#user">developers.goteo.org/users#user</a>
        """
        u = User.get(id)
        item = marshal(u, UserCompleteResponse.resource_fields)
        item['date-created'] = u.date_created
        item['profile-image-url'] = u.profile_image_url
        time_start = time.time()
        res = UserCompleteResponse(
            starttime = time_start,
            attributes = item
        )
        if u is None:
            return bad_request('User not found', 404)

        return res.response()

