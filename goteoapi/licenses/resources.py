# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..decorators import *
from ..helpers import marshal
from ..base_resources import BaseList, Response
from .models import License

license_resource_fields = {
    "id"             : fields.String,
    "name"           : fields.String,
    "description"    : fields.String,
    "url"            : fields.String,
    "svg-url"        : fields.String,
    "total-rewards"  : fields.Integer,
    "total-projects" : fields.Integer
}

class LicensesListAPI(BaseList):
    """License API"""

    @requires_auth
    @ratelimit()
    @swag_from('swagger_specs.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Dirty work for the get() method"""

        from ..models.reward import Reward
        from ..projects.models import Project

        time_start = time.time()
        #removing not-needed standard filters
        args = self.parse_args(remove=('page','limit'))

        items = []
        for u in License.list(**args):
            item = marshal(u, license_resource_fields)
            item['svg-url'] = svg_image_url(item['id'] + '.svg')
            reward_filter = args.copy()
            reward_filter['license_type'] = 'social'
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
