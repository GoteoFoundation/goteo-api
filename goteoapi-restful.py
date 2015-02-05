#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import config
from model import app
from decorators import *

from flask import request, jsonify, url_for

from api.reports.money import MoneyAPI
from api.reports.rewards import RewardsAPI
from api.reports.community import CommunityAPI
from api.reports.projects import ProjectsAPI
#from api.misc import ProjectListAPI, ProjectAPI

from flask_restful_swagger import swagger
from flask.ext.restful import Api


api = swagger.docs(Api(app), apiVersion='1.0', description='Goteo.org API')
#api = Api(app)

@app.errorhandler(404)
def page_not_found_404(e):
     return jsonify(status='ERROR', error=404, message=str(e), links=config.links),

@app.errorhandler(403)
def page_not_found_403(e):
     return jsonify(status='ERROR', error=403, message=str(e), links=config.links),

@app.errorhandler(410)
def page_not_found_410(e):
     return jsonify(status='ERROR', error=410, message=str(e), links=config.links),

@app.errorhandler(500)
def page_not_found_500(e):
     return jsonify(status='ERROR', error=500, message=str(e), links=config.links),

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route('/')
@requires_auth
def index():
    routes = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            routes.append((url, rule.endpoint))
    return jsonify(status='OK', message='Goteo API v' + str(config.version), routes=routes, links=config.links)


@app.route('/reports/')
@requires_auth
def reports():
    return """
<h1>API de Goteo.org</h1>
This API is compatible with <a href="http://swagger.io/">Swagger</a> specification. See: <a href="http://{host}/api/spec.html">html</a> and <a href="http://{host}/api/spec.json">json</a>.
<h3>Endpoints:</h3>
<a href="/reports/money">/reports/money</a></br>
<a href="/reports/projects">/reports/projects</a></br>
<a href="/reports/community">/reports/community</a></br>
<a href="/reports/rewards">/reports/rewards</a></br>
<h3>URL examples:</h3>
<a href="http://{host}/reports/money?from_date=2014-01-01">http://{host}/reports/money?from_date=2014-01-01</a><br>
<a href="http://{host}/reports/money?project=diagonal">http://{host}/reports/money?project=diagonal</a><br>
<a href="http://{host}/reports/projects?location=36.716667,-4.416667,100">http://{host}/reports/projects?location=36.716667,-4.416667,100</a><br>
<h3>curl examples:</h3>
<span style="font-family: monospace;">
curl -i http://{host}/reports/money</br>
curl -i -X GET -d from_date="2014-01-01" http://{host}/reports/money<br>
curl -i -X GET -d project="diagonal" http://{host}/reports/money<br>
curl -i -X GET -d location="36.716667,-4.416667,100" http://{host}/reports/projects<br>
<br>
curl -i --basic --user "user:key" http://{host}/reports/
</span>
""".format(host=request.host)

#api.add_resource(ProjectListAPI, '/projects/', endpoint='projects1')
#api.add_resource(ProjectAPI, '/projects/<string:project_id>', endpoint='project')
api.add_resource(MoneyAPI, '/reports/money', endpoint='money')
api.add_resource(ProjectsAPI, '/reports/projects', endpoint='projects')
api.add_resource(CommunityAPI, '/reports/community', endpoint='community')
api.add_resource(RewardsAPI, '/reports/rewards', endpoint='rewards')


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
