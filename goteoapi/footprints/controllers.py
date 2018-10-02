# -*- coding: utf-8 -*-
#
# User resources


from .. import api
from .resources import FootprintsListAPI

api.add_resource(FootprintsListAPI,
                 '/footprints/',
                 endpoint='api_footprints.footprints')
