# -*- coding: utf-8 -*-
#
# Auth resources


from .. import api
from .resources import TokenAPI

api.add_resource(TokenAPI, '/login', endpoint='api_auth.token')
