# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from
from ..ratelimit import ratelimit
from ..base_resources import BaseItem, Response
from ..users.models import User

user_resource_fields = {
    "id"                : fields.String
}


class LoginAPI(BaseItem):
    """Auth & login"""

    @ratelimit()
    def get(self):
        time_start = time.time()
        item = User.generate_auth_token()
        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res.response()


