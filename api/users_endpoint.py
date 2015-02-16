# -*- coding: utf-8 -*-

from flask import Blueprint
from api.users.user import UserAPI, UsersListAPI

from api import api
from api.decorators import *

api_users = Blueprint('api_users', __name__)

# All resources for users
api.add_resource(UserAPI, '/users/<string:id>', endpoint='api_users.user')
api.add_resource(UsersListAPI, '/users/', endpoint='api_users.users_list')