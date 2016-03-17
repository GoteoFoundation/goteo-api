# -*- coding: utf-8 -*-
#
# Auth resources


from .. import api
from .resources import LoginAPI

api.add_resource(LoginAPI, '/login/', endpoint='api_login.login')
