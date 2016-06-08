# -*- coding: utf-8 -*-
#
# User resources

from .. import api
from .resources import LicensesListAPI

api.add_resource(LicensesListAPI,
                 '/licenses/',
                 endpoint='api_licenses.licenses')
