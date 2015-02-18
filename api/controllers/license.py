# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from api.models.license import License
from api.decorators import *
from api.base_endpoint import BaseItem, BaseList, Response


@swagger.model
class LicenseResponse(Response):
    """LicenseResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
        "description"         : fields.String,
        "svg_url"         : fields.String,
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
        <a href="http://developers.goteo.org/licenses#list">developers.goteo.org/licenses#list</a>
        """
        time_start = time.time()
        args = self.reqparse.parse_args()
        items = []
        for u in License.list(**args):
            items.append( marshal(u, LicenseResponse.resource_fields) )

        res = LicensesListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = License.total(**args)
        )
        if items == []:
            return bad_request('No licenses to list', 404)

        return res.response()
