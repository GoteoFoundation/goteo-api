# -*- coding: utf-8 -*-
#
# Call resources


from .. import api, app
from flask import url_for, redirect
from .resources import CallsListAPI, CallAPI, CallProjectsListAPI

api.add_resource(CallsListAPI,
                 '/calls/',
                 endpoint='api_calls.calls')
api.add_resource(CallAPI,
                 '/calls/<string:call_id>',
                 endpoint='api_calls.call')
api.add_resource(CallProjectsListAPI,
                 '/calls/<string:call_id>/projects/',
                 endpoint='api_calls.call_projects')


# redirect end trailing slash
@app.route('/calls/<string:call_id>/', endpoint='redirect.call')
def call_redirect(call_id):
    return redirect(url_for('api_calls.call', call_id=call_id), code=301)
