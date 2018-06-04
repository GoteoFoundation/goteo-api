# -*- coding: utf-8 -*-
#
# Matcher resources


from .. import api, app
from flask import url_for, redirect
from .resources import MatchersListAPI, MatcherAPI, MatcherProjectsListAPI

api.add_resource(MatchersListAPI,
                 '/matchers/',
                 endpoint='api_matchers.matchers')
api.add_resource(MatcherAPI,
                 '/matchers/<string:matcher_id>',
                 endpoint='api_matchers.matcher')
api.add_resource(MatcherProjectsListAPI,
                 '/matchers/<string:matcher_id>/projects/',
                 endpoint='api_matchers.matcher_projects')


# redirect end trailing slash
@app.route('/matchers/<string:matcher_id>/', endpoint='redirect.matcher')
def matcher_redirect(matcher_id):
    return redirect(url_for('api_matchers.matcher', matcher_id=matcher_id), code=301)
