# -*- coding: utf-8 -*-
import flask
from flask import jsonify

from . import app

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers', 'Authorization')
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def page_not_found(e):
     resp = jsonify(error=e.code, message=str(e), links=app.config['LINKS'])
     resp.status_code = e.code
     return resp

#
# Routing
# =======

# HOME
@app.route('/', endpoint='api_home')
# @requires_auth
# @ratelimit()
def index():
    """API Welcome. All the available endpoints of the API"""

    func_list = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.startswith('api_'):
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(version=app.config['VERSION'], message=app.config['DESCRIPTION'] + ' v' + str(app.config['VERSION']), endpoints=func_list, links=app.config['LINKS'])


#
# import sub-packages controllers definitions
#
__import__('goteoapi.users.controllers')
__import__('goteoapi.projects.controllers')
__import__('goteoapi.categories.controllers')
__import__('goteoapi.licenses.controllers')
