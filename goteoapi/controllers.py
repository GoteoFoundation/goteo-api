# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import app
from .ratelimit import get_view_rate_limit


@app.after_request
def inject_addtional_headers(resp):
    """
    Ensure all responses have the CORS headers.
    This ensures any failures are also accessible by the client.
    """
    # Default global opened CORS
    origin = request.headers.get('Origin', '*')
    # Check system user bind to CORS response
    auth = request.authorization
    if (auth and app.config['USERS']
       and auth.username in app.config['USERS']
       and 'password' in app.config['USERS'][auth.username]):
        user = app.config['USERS'][auth.username]
        if user['password'] == auth.password:
            if 'cors' in user and origin not in user['cors']:
                origin = ''
    resp.headers['Access-Control-Allow-Origin'] = origin
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Expose-Headers'] = 'Authorization'
    # 'GET, POST, HEAD, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get(
        'Access-Control-Request-Headers', 'Authorization')
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = 1
    else:
        resp.headers['Access-Control-Max-Age'] = 60 * 60 * 24 * 20

    # Limit headers
    limit = get_view_rate_limit()
    if limit:
        h = resp.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))

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
# @requires_auth()
# @ratelimit()
def index():
    """API Welcome. All the available endpoints of the API"""

    func_list = {}
    for rule in app.url_map.iter_rules():
        # Filter out rules non Goteo-api rules
        if "GET" in rule.methods and rule.endpoint.startswith('api_'):
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(version=app.config['VERSION'],
                   message=app.config['DESCRIPTION']
                   + ' v' + str(app.config['VERSION']),
                   endpoints=func_list,
                   links=app.config['LINKS'])


#
# import sub-packages controllers definitions
#
__import__('goteoapi.users.controllers')
__import__('goteoapi.auth.controllers')
__import__('goteoapi.projects.controllers')
__import__('goteoapi.invests.controllers')
__import__('goteoapi.categories.controllers')
__import__('goteoapi.licenses.controllers')
__import__('goteoapi.calls.controllers')
