# -*- coding: utf-8 -*-
#
# User resources


from .. import api
from .resources import UsersListAPI, UserAPI, UserOwnerAPI

api.add_resource(UsersListAPI, '/users/', endpoint='api_users.users_list')
api.add_resource(UserOwnerAPI, '/me', endpoint='api_users.users_owner')
api.add_resource(UserAPI, '/users/<string:user_id>', endpoint='api_users.user')
