# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from config import config

from api import db
from api.models import User
from api.decorators import *

from api.base_endpoint import BaseItem, BaseList, Response

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)


@swagger.model
class UserResponse(Response):
    """UserResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
        "date_created"         : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "profile_image_url"         : fields.String,
    }

    required = resource_fields.keys()


@swagger.model
class UserCompleteResponse(Response):
    """UserCompleteResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
        "node"         : fields.String,
        "date_created"         : fields.DateTime(dt_format='rfc822'),
        "date_updated"         : fields.DateTime(dt_format='rfc822'),
        "profile_image_url"         : fields.String,
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
        nickname='money',
        responseClass=UsersListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        time_start = time.time()
        args = self.reqparse.parse_args()
        items = []
        for u in User.list(args['page'], args['limit']):
            items.append( marshal(u, UserResponse.resource_fields) )

        res = UsersListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = User.total()
        )
        if items == []:
            return bad_request('No users to list', 404)

        return res.response()




class UserAPI(BaseItem):
    """Get User Details"""


    @swagger.operation(
        notes='User profile',
        nickname='money',
        responseClass=UserResponse.__name__,
        responseMessages=BaseItem.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, id):
        u = User.get(id)
        time_start = time.time()
        res = UserCompleteResponse(
            starttime = time_start,
            attributes = marshal(u, UserCompleteResponse.resource_fields)
        )
        if u is None:
            return bad_request('User not found', 404)

        return res.response()

