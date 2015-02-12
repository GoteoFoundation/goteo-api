# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from api.reports.money import MoneyAPI
from api.reports.projects import ProjectsAPI
from api.reports.community import CommunityAPI
from api.reports.rewards import RewardsAPI

from api import app, api
from api.decorators import *

api_reports = Blueprint('api_reports', __name__)

# Reports home
@api_reports.route('/reports/')
@api_reports.route('/reports', endpoint='main')
@requires_auth
@ratelimit()
def reports():
    """All available endpoints for Statistics"""
    func_list = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.startswith('api_reports.') and not rule.rule.endswith('/'):
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
        # func_list[rule.rule] = rule.endpoint
    return jsonify(message='Collected Statistics of Goteo.org', endpoints=func_list)

# All resources for reports
api.add_resource(MoneyAPI, '/reports/money', '/reports/money/', endpoint='api_reports.money')
api.add_resource(ProjectsAPI, '/reports/projects', '/reports/projects/', endpoint='api_reports.projects')
api.add_resource(CommunityAPI, '/reports/community', '/reports/community/', endpoint='api_reports.community')
api.add_resource(RewardsAPI, '/reports/rewards', '/reports/rewards/', endpoint='api_reports.rewards')