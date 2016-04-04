# -*- coding: utf-8 -*-
#
# Call resources


from .. import api, app
from flask import url_for, redirect
from .resources import CallsListAPI, CallAPI

api.add_resource(CallsListAPI, '/matchfunding/', endpoint='api_calls.calls_list')
# api.add_resource(CallAPI, '/matchfunding/<string:call_id>', endpoint='api_calls.call')

# redirect end trailing slash
# @app.route('/matchfunding/<string:call_id>/', endpoint='redirect.call')
# def call_redirect(call_id):
#     return redirect(url_for('api_calls.call', call_id=call_id), code=301)
