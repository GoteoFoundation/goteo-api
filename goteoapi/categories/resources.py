# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from ..decorators import *
from ..base_resources import BaseList, Response
from .models import Category

class CategoriesListAPI(BaseList):
    """Category list"""

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Category API
        This resource returns categories information.
        <a href="http://developers.goteo.org/doc/categories">developers.goteo.org/doc/categories</a>
        ---
        tags:
            - categories
        definitions:
            - schema:
                id: Category
                properties:
                    id:
                        type: string
                        description: Category unique identifier
                    name:
                        type: string
                        description: Category name
                    description:
                        type: string
                        description: Category short description
                    total-users:
                        type: integer
                        description: Number of users using this license
                    total-projects:
                        type: integer
                        description: Number of projects using this license
        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified. Restricts the list to the categories used in projects assigned in that nodes
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified. Restricts the list to the categories used in that projects
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01". Restricts the list to the categories used in projects created between that dates
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01". Restricts the list to the categories used in projects created between that dates
              type: string
              format: date
            # - in: query
            #   name: category
            #   description: Filter by project category. Multiple categories can be specified. Restricts the list to the categories used in projects in that categories
            #   type: integer
            - in: query
              name: lang
              description: Get results by specified lang. Multiple langs can be specified
              type: string
              collectionFormat: multi
            - in: query
              name: location
              description: Filter by project location (Latitude,longitude,Radius in Km). Restricts the list to the categories used in projects geolocated in that area
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
                description: List of available categories
                schema:
                    type: array
                    id: categories
                    items:
                        $ref: '#/definitions/api_categories_categories_list_get_Category'
            400:
                description: Invalid parameters format
            # 404:
            #     description: Resource not found
        """
        res = self._get()

        return res.response()

    def _get(self):
        """Dirty work for the get() method"""

        from ..users.models import User
        from ..projects.models import Project

        time_start = time.time()
        #removing not-needed standard filters
        args = self.parse_args(remove=('page','limit'))

        items = []
        resource_fields = {
            "id"             : fields.String,
            "name"           : fields.String,
            "description"    : fields.String,
            "total-projects" : fields.Integer,
            "total-users"    : fields.Integer
        }
        for u in Category.list(**args):
            item = marshal(u, resource_fields)
            project_filter = args.copy()
            project_filter['category'] = [item['id']]
            item['total-projects'] = Project.total(**project_filter)
            item['total-users'] = User.total(**project_filter)
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Category.total(**args)
        )

        return res
