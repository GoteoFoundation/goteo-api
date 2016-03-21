# -*- coding: utf-8 -*-

from flask import jsonify

from goteoapi import app, api
from goteoapi.ratelimit import ratelimit
from goteoapi.auth.decorators import requires_auth

from .money import MoneyAPI
from .projects import ProjectsAPI
from .community import CommunityAPI
from .rewards import RewardsAPI
from .summary import SummaryAPI


# Reports home
@app.route('/reports/', endpoint='api_reports')
# @requires_auth
@ratelimit()
def reports():
    """All available endpoints for Statistics"""
    func_list = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.startswith('api_reports.'):
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(message='Collected Statistics of Goteo.org', endpoints=func_list)

# All resources for reports
api.add_resource(MoneyAPI, '/reports/money/', endpoint='api_reports.money')
api.add_resource(ProjectsAPI, '/reports/projects/', endpoint='api_reports.projects')
api.add_resource(CommunityAPI, '/reports/community/', endpoint='api_reports.community')
api.add_resource(RewardsAPI, '/reports/rewards/', endpoint='api_reports.rewards')
api.add_resource(SummaryAPI, '/reports/summary/', endpoint='api_reports.summary')
