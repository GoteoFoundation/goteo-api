# -*- coding: utf-8 -*-
#
# User resources

from .. import api

from .resources import DigestsListAPI

api.add_resource(DigestsListAPI, '/digests/<path:endpoint>', endpoint='api_digests')
