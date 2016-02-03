# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from ..decorators import *
from ..base_resources import BaseList, Response
from .models import License

class LicensesListAPI(BaseList):
    """License API"""

    @requires_auth
    @ratelimit()
    def get(self):
        """
        License API
        This resource returns license information.
        <a href="http://developers.goteo.org/doc/licenses">developers.goteo.org/doc/licenses</a>
        ---
        tags:
            - licenses
        definitions:
            - schema:
                id: License
                properties:
                    id:
                        type: string
                        description: License unique identifier
                    name:
                        type: string
                        description: License name
                    description:
                        type: string
                        description: License short description
                    svg-url:
                        type: string
                        description: Icon URL for the license
                    total-rewards:
                        type: integer
                        description: Number of rewards using this license
                    total-projects:
                        type: integer
                        description: Number of projects using this license
        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified. Restricts the list to the licenses used in projects assigned in that nodes
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified. Restricts the list to the licenses used in that projects
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01". Restricts the list to the licenses used in projects created between that dates
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01". Restricts the list to the licenses used in projects created between that dates
              type: string
              format: date
            # - in: query
            #   name: category
            #   description: Filter by project category. Multiple licenses can be specified. Restricts the list to the licenses used in projects in that licenses
            #   type: integer
            - in: query
              name: lang
              description: Get results by specified lang. Multiple langs can be specified
              type: string
              collectionFormat: multi
            - in: query
              name: location
              description: Filter by project location (Latitude,longitude,Radius in Km). Restricts the list to the licenses used in projects geolocated in that area
              type: number
              collectionFormat: csv
            # - in: query
            #   name: page
            #   description: Page number (starting at 1) if the result can be paginated
            #   type: integer
            # - in: query
            #   name: limit
            #   description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
            #   type: integer
        responses:
            200:
                description: List of available licenses
                schema:
                    type: array
                    id: licenses
                    items:
                        $ref: '#/definitions/api_licenses_licenses_list_get_License'
            400:
                description: Invalid parameters format
            # 404:
            #     description: Resource not found

        """
        res = self._get()

        return res.response()

    def _get(self):
        """Dirty work for the get() method"""

        from ..models.reward import Reward
        from ..projects.models import Project

        time_start = time.time()
        #removing not-needed standard filters
        args = self.parse_args(remove=('page','limit'))

        resource_fields = {
            "id"             : fields.String,
            "name"           : fields.String,
            "description"    : fields.String,
            "url"            : fields.String,
            "svg-url"        : fields.String,
            "total-rewards"  : fields.Integer,
            "total-projects" : fields.Integer
        }
        items = []
        for u in License.list(**args):
            item = marshal(u, resource_fields)
            item['svg-url'] = svg_image_url(item['id'] + '.svg')
            reward_filter = args.copy()
            reward_filter['license_type'] = 'social'
            # print item
            reward_filter['license'] = [item['id']]
            item['total-rewards'] = Reward.total(**reward_filter)
            item['total-projects'] = Project.total(**reward_filter)
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = License.total(**args)
        )

        return res
