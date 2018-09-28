# -*- coding: utf-8 -*-
#
# User resources


from .. import api
from .resources import SocialCommitmentsListAPI

api.add_resource(SocialCommitmentsListAPI,
                 '/socialcommitments/',
                 endpoint='api_socialcommitments.socialcommitments')
