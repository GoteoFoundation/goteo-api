#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import config
from model import app
from decorators import *

from flask import jsonify

from api.reports.money import MoneyAPI
from api.reports.rewards import RewardsAPI
from api.reports.community import CommunityAPI
from api.reports.projects import ProjectsAPI
#from api.misc import ProjectListAPI, ProjectAPI

from flask_restful_swagger import swagger
from flask.ext.restful import Api


api = swagger.docs(Api(app), apiVersion=config.version, description=config.description)
#api = Api(app)

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
def page_not_found(e):
     resp = jsonify(code=e.code, message=str(e), links=config.links)
     resp.status_code = e.code
     return resp


#
# Routing
# =======

# HOME
@app.route('/', endpoint='api_home')
@requires_auth
@ratelimit()
def index():
    """API Welcome. All the available endpoints of the API"""

    func_list = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.find('api_') == 0:
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(code=200, version=config.version, message=config.description + ' v' + str(config.version), endpoints=func_list, links=config.links)

# Reports home
@app.route('/reports/')
@app.route('/reports', endpoint='api_reports')
@requires_auth
@ratelimit()
def reports():
    """All available endpoints for Statistics"""

    routes = []
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.find('api_reports_') == 0:
            routes.append(rule.rule)
    return jsonify(code=200, message='Collected Statistics of Goteo.org', endpoints=routes)

# ROUTE CLASSES
#api.add_resource(ProjectListAPI, '/projects/', endpoint='projects1')
#api.add_resource(ProjectAPI, '/projects/<string:project_id>', endpoint='project')
api.add_resource(MoneyAPI, '/reports/money', '/reports/money/', endpoint='api_reports_money')
api.add_resource(ProjectsAPI, '/reports/projects', '/reports/projects/', endpoint='api_reports_projects')
api.add_resource(CommunityAPI, '/reports/community', '/reports/community/', endpoint='api_reports_community')
api.add_resource(RewardsAPI, '/reports/rewards', '/reports/rewards/', endpoint='api_reports_rewards')


#This part will not be executed under uWSGI module (nginx)
if __name__ == '__main__':
    app.debug = True

    if app.debug:
        import os
        module_path = os.path.dirname(swagger.__file__)
        module_path = os.path.join(module_path, 'static')
        extra_dirs = [module_path, ]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
    else:
        extra_files = []

    app.run(host='0.0.0.0', extra_files=extra_files)
