import time
from functools import update_wrapper
from flask import request, g, session, jsonify
from model import app
from sqlalchemy.orm.exc import NoResultFound
from flask_redis import Redis

from config import config

#Error handling
def bad_request(message):
     resp = jsonify(error=400, message=str(message))
     resp.status_code = 400
     return resp

#
# REDIS RATE LIMITER
# ==================

if app.config['REDIS_URL'] is not False:
    redis = Redis(app)
else:
    redis = False

class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        p = redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)

def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)

def on_over_limit(limit):
    resp = jsonify(code=400, message='Too many requests')
    resp.status_code = 400
    return resp

def ratelimit(limit=config.requests_limit, per=config.requests_time, over_limit=on_over_limit):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            if not config.requests_limit:
                return f(*args, **kwargs)

            if config.auth_enabled:
                key = 'rate-limit/%s/' % request.authorization.username
            else:
                remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                key = 'rate-limit/%s' % remote_ip

            rlimit = RateLimit(key, limit, per)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator

@app.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response


#
# BASIC AUTH DECORATOR
# ====================
# Based on http://flask.pocoo.org/snippets/8/

from functools import wraps
from model import db, UserApi
from netaddr import IPSet, AddrFormatError
from datetime import datetime

def check_auth(username, password):
    """Checks username & password authentication"""

    #try some built-in auth first
    if config.users and username in config.users and 'password' in config.users[username]:
        user = config.users[username]
        if user['password'] == password:
            if 'remotes' in user:
                try:
                    remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    if remote_ip in IPSet(user['remotes']):
                        return True
                except AddrFormatError:
                    "continue"

            else:
                return True

    #Try the key-password values in sql
    try:
        user = db.session.query(UserApi).filter(UserApi.user == username, UserApi.key == password).one()
        if user.expiration_date is not None and user.expiration_date <= datetime.today():
            # print user.expiration_date, '<=', datetime.today()
            return 'API Key expired. Please get new valid key! '
        return True
    except NoResultFound:
        return 'Acces denied: Invalid username or password!'

    return False


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.auth_enabled:
            return f(*args, **kwargs)

        auth = request.authorization
        msg = 'You need a key in order to use our API. Please contact us and we will provide you one!'
        if auth:
            ok = check_auth(auth.username, auth.password)
            if(ok is True):
                return f(*args, **kwargs)
            elif(ok is not False):
                msg = str(ok)

        resp = jsonify(code=401, message=msg)
        resp.status_code = 401
        resp.headers.add('WWW-Authenticate', 'Basic realm="Goteo.org API"')
        return resp

    return decorated


############################ debug ############################
def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f
