# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..decorators import *
from ..helpers import marshal
from ..base_resources import BaseList, Response
from .models import Category

category_resource_fields = {
    "id"             : fields.Integer,
    "name"           : fields.String,
    "description"    : fields.String,
    "total-projects" : fields.Integer,
    "total-users"    : fields.Integer
}

class CategoriesListAPI(BaseList):
    """Category list"""

    @requires_auth
    @ratelimit()
    @swag_from('swagger_specs.yml')
    def get(self):
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
        for u in Category.list(**args):
            item = marshal(u, category_resource_fields)
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
