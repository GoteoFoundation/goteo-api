# -*- coding: utf-8 -*-

from flask import Blueprint
from api.controllers.user import UserAPI, UsersListAPI
from api.controllers.license import LicensesListAPI
from api.controllers.category import CategoriesListAPI
from api.controllers.digest import DigestsListAPI

from api import api
from api.decorators import *

api_users = Blueprint('api_users', __name__)

# All resources for users
api.add_resource(UserAPI, '/users/<string:id>', endpoint='api_users.user')
api.add_resource(UsersListAPI, '/users/', endpoint='api_users.users_list')


api_licenses = Blueprint('api_licenses', __name__)

# All resources for licenses
api.add_resource(LicensesListAPI, '/licenses/', endpoint='api_licenses.licenses_list')

api_categories = Blueprint('api_categories', __name__)

# All resources for categories
api.add_resource(CategoriesListAPI, '/categories/', endpoint='api_categories.categories_list')

api_digests = Blueprint('api_digests', __name__)

# All resources for digests
api.add_resource(DigestsListAPI, '/digests/<path:endpoint>', endpoint='api_digests.money')