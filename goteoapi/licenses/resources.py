# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from ..decorators import *

from ..base_resources import BaseList, Response

from .models import License

@swagger.model
class LicenseResponse(Response):
    """LicenseResponse"""

    resource_fields = {
        "id"             : fields.String,
        "name"           : fields.String,
        "description"    : fields.String,
        "url"            : fields.String,
        "svg-url"        : fields.String,
        "total-rewards"  : fields.Integer,
        "total-projects" : fields.Integer,
    }

    required = resource_fields.keys()


@swagger.model
@swagger.nested(**{
                'items' : LicenseResponse.__name__,
                }
            )
class LicensesListResponse(Response):
    """LicensesListResponse"""

    resource_fields = {
        "items"         : fields.List(fields.Nested(LicenseResponse.resource_fields)),
    }

    required = resource_fields.keys()


class LicensesListAPI(BaseList):
    """Get License list"""


    @swagger.operation(
        notes='Licenses list',
        nickname='licenses',
        responseClass=LicensesListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the licenses list
        <a href="http://developers.goteo.org/doc/licenses">developers.goteo.org/doc/licenses</a>
        """
        res = self._get()

        if res.ret['items'] == []:
            return bad_request('No licenses to list', 404)

        return res.response()

    def _get(self):
        """Dirty work for the get() method"""

        from ..models.reward import Reward
        from ..models.project import Project

        time_start = time.time()
        #removing not-needed standard filters
        args = self.parse_args(remove=('page','limit'))

        items = []
        for u in License.list(**args):
            item = marshal(u, LicenseResponse.resource_fields)
            item['svg-url'] = svg_image_url(item['id'] + '.svg')
            reward_filter = args.copy()
            reward_filter['license_type'] = 'social'
            # print item
            reward_filter['license'] = [item['id']]
            item['total-rewards'] = Reward.total(**reward_filter)
            item['total-projects'] = Project.total(**reward_filter)
            items.append( item )

        res = LicensesListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = License.total(**args)
        )

        return res
