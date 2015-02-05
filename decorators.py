import time
from functools import update_wrapper
from flask import request, g, session
from model import app
from sqlalchemy.orm.exc import NoResultFound
from flask_redis import Redis

from config import config

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
    return 'You hit the rate limit', 400

def ratelimit(limit=config.requests_limit, per=config.requests_time, over_limit=on_over_limit):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            if not config.requests_limit:
                return f(*args, **kwargs)
            if config.auth_enabled:
                key = 'rate-limit/%s/' % request.authorization.username
            else:
                key = 'rate-limit/%s/'

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


######################### auth #########################
# Based on http://flask.pocoo.org/snippets/8/

from functools import wraps
from flask import request, Response
from model import db, UserApi

from datetime import datetime

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.auth_enabled:
            return f(*args, **kwargs)
        auth = request.authorization
        if auth:
            try:
                user = db.session.query(UserApi).filter(UserApi.user == auth.username, UserApi.key == auth.password).one()
                if user.expiration_date is not None and user.expiration_date <= datetime.today():
                    print user.expiration_date, '<=', datetime.today()
                    return Response('You API key has expired!\n')
                return f(*args, **kwargs)
            except NoResultFound:
                """Sends a 401 response that enables basic auth"""
                return Response(
                'You need a key in order to use our API. Please contact us and we will provide you one!\n', 401,
                {'WWW-Authenticate': 'Basic realm="Goteo.org API"'})
        else:
            return Response(
            'You need a key in order to use our API. Please contact us and we will provide you one!\n', 401,
            {'WWW-Authenticate': 'Basic realm="Goteo.org API"'})
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
