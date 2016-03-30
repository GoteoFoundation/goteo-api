# -*- coding: utf-8 -*-
#
# User resources


from .. import api, app
from flask import redirect, url_for
from .resources import UsersListAPI, UserAPI, UserOwnerAPI

api.add_resource(UsersListAPI, '/users/', endpoint='api_users.users_list')
api.add_resource(UserOwnerAPI, '/me', endpoint='api_users.users_owner')
api.add_resource(UserAPI, '/users/<string:user_id>', endpoint='api_users.user')

# redirect end trailing slash
@app.route('/users/<string:user_id>/', endpoint='redirect.user')
def user_redirect(user_id):
    return redirect(url_for('api_users.user', user_id=user_id), code=301)
