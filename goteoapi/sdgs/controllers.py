# -*- coding: utf-8 -*-
#
# User resources


from .. import api
from .resources import SdgsListAPI

api.add_resource(SdgsListAPI,
                 '/sdgs/',
                 endpoint='api_sdgs.sdgs')
