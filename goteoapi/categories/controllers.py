# -*- coding: utf-8 -*-
#
# User resources


from .. import api
from .resources import CategoriesListAPI

api.add_resource(CategoriesListAPI,
                 '/categories/',
                 endpoint='api_categories.categories')
