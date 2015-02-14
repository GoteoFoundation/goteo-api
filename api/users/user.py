# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound

from config import config

from api import db
from api.models import User
from api.decorators import *

from api.base_endpoint import Base, Response

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

func = sqlalchemy.func


@swagger.model
class UserResponse(Response):
    """UserResponse"""

    resource_fields = {
        "id"         : fields.String,
        "name"         : fields.String,
    }

    required = resource_fields.keys()


class UserAPI(Base):
    """Get User Details"""


    @swagger.operation(
        notes='Money report',
        nickname='money',
        responseClass=User.__name__,
        parameters=Base.INPUT_FILTERS,
        responseMessages=Base.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, id):
        try:
            time_start = time.time()
            res = UserResponse(
                starttime = time_start,
                attributes = marshal(User.query.filter(User.id == id, User.hide == 0).one(), UserResponse.resource_fields)
            )
            return res.response()
        except NoResultFound:
            return bad_request('User not found', 404)
