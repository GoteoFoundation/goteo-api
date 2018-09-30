# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import marshal
from ..base_resources import BaseList, Response
from .models import SocialCommitment

category_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String
}
social_commitment_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "icon_url": fields.String,
    "Categories": fields.List(fields.Nested(category_resource_fields)),
    "total_projects": fields.Integer,
    "total_users": fields.Integer
}


class SocialCommitmentsListAPI(BaseList):
    """SocialCommitment list"""

    @requires_auth()
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
        # removing not-needed standard filters
        args = self.parse_args(remove=('page', 'limit'))

        items = []
        for u in SocialCommitment.list(**args):
            item = marshal(u, social_commitment_resource_fields)
            project_filter = args.copy()
            project_filter['social_commitment'] = item['id']
            item['total-projects'] = Project.total(**project_filter)
            item['total-users'] = User.total(**project_filter)
            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={'items': items},
            filters=args.items(),
            total=SocialCommitment.total(**args)
        )

        return res
