# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from ..decorators import *
from ..base_resources import BaseItem, BaseList, Response
from ..location.models import UserLocation
from .models import User

class UsersListAPI(BaseList):
    """User list"""

    @requires_auth
    @ratelimit()
    def get(self):
        """
        User API
        This resource returns user information.
        <a href="http://developers.goteo.org/doc/users">developers.goteo.org/doc/users</a>
        ---
        tags:
            - users
        definitions:
            - schema:
                id: User
                properties:
                    id:
                        type: string
                        description: User unique identifier
                    name:
                        type: string
                        description: Name of the user
                    node:
                        type: string
                        description: Node where the user was created originally
                    profile-image-url:
                        type: string
                        description:  URL with the avatar (image) of the user
                    profile-url:
                        type: string
                        description: URL for the user profile
                    date-created:
                        type: string
                        description: Date when the user was created RFC822 format

        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified. Restricts the list to the users originally created in that node(s)
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified. Restricts the list to the users that have either collaborate or contributed (financially) to that project(s).
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01". Restricts the list to the users created in that range
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01". Restricts the list to the users created in that range
              type: string
              format: date
            - in: query
              name: category
              description: Filter by project category. Multiple users can be specified. Restricts the list to the users that have interests in that category(ies)
              type: integer
            # - in: query
            #   name: location
            #   description: Filter by project location (Latitude,longitude,Radius in Km). Restricts the list to the users used in projects geolocated in that area
            #   type: number
            #   collectionFormat: csv
            - in: query
              name: page
              description: Page number (starting at 1) if the result can be paginated
              type: integer
            - in: query
              name: limit
              description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
              type: integer
        responses:
            200:
                description: List of available users
                schema:
                    type: array
                    id: users
                    items:
                        $ref: '#/definitions/api_users_users_list_get_User'
            400:
                description: Invalid parameters format
            # 404:
            #     description: Resource not found
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

        resource_fields = {
            "id"                : fields.String,
            "name"              : fields.String,
            "node"              : fields.String,
            "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
            "profile-url"       : fields.String,
            "profile-image-url" : fields.String,
            "latitude" : fields.Float,
            "longitude" : fields.Float
        }
        items = []
        for u in User.list(**args):
            item = marshal(u, resource_fields)
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
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



class UserAPI(BaseItem):
    """User Details"""

    @requires_auth
    @ratelimit()
    def get(self, user_id):
        """
        User API
        This resource returns user information.
        <a href="http://developers.goteo.org/users#user">developers.goteo.org/users#user</a>
        ---
        tags:
            - users
        parameters:
            - in: path
              type: string
              name: user_id
              description: Unique ID for the user
              required: true
        responses:
            200:
                description: User data
                schema:
                    $ref: '#/definitions/api_users_users_list_get_User'
            404:
                description: Resource not found
        """

        res = self._get(user_id)

        if res.ret['id'] == None:
            return bad_request('User not found', 404)

        return res.response()

    def _get(self, user_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        u = User.get(user_id)
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
        item = marshal(u, resource_fields)
        if u != None:
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
            location = UserLocation.get(u.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude

        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res

