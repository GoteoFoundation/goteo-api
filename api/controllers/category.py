# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from api.models.category import Category
from api.models.project import Project
from api.models.user import User
from api.decorators import *
from api.base_endpoint import BaseList, Response
from api.helpers import parse_args

@swagger.model
class CategoryResponse(Response):
    """CategoryResponse"""

    resource_fields = {
        "id"             : fields.String,
        "name"           : fields.String,
        "description"    : fields.String,
        "total-projects" : fields.Integer,
        "total-users"    : fields.Integer,
    }

    required = resource_fields.keys()


@swagger.model
@swagger.nested(**{
                'items' : CategoryResponse.__name__,
                }
            )
class CategoriesListResponse(Response):
    """CategoriesListResponse"""

    resource_fields = {
        "items"         : fields.List(fields.Nested(CategoryResponse.resource_fields)),
    }

    required = resource_fields.keys()


class CategoriesListAPI(BaseList):
    """Get Category list"""


    @swagger.operation(
        notes='Categorys list',
        nickname='categories',
        responseClass=CategoriesListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the categories list
        <a href="http://developers.goteo.org/doc/categories">developers.goteo.org/doc/categories</a>
        """
        time_start = time.time()
        #removing not-needed standard filters
        self.reqparse.remove_argument('page')
        self.reqparse.remove_argument('limit')
        args = parse_args(self.reqparse)

        items = []
        for u in Category.list(**args):
            item = marshal(u, CategoryResponse.resource_fields)
            project_filter = args.copy()
            project_filter['category'] = [item['id']]
            item['total-projects'] = Project.total(**project_filter)
            item['total-users'] = User.total(**project_filter)
            items.append( item )

        res = CategoriesListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Category.total(**args)
        )
        if items == []:
            return bad_request('No categories to list', 404)

        return res.response(self.json)
