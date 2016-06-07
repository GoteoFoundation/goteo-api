#
# CONFIG DEFAULTS
# DO NO TOUCH THIS FILE
#
# Configuration must be overriden in the
# ../config.py file
#

# Goteo Database (mandatory)
# ================================
# DB URI
DB_URI = 'mysql://user:pass@mysqlhost/dbname'

# A unique secret key for this application
SECRET_KEY = 'a-super-secret-and-random-key'

# Optional config:
# ================

# Number of seconds to auto-expire access tokens
ACCESS_TOKEN_DURATION = 600

# api requests rate limit (Needs REDIS_URL configured)
# Users are allowed 300 requests in 15 minutes
REQUESTS_LIMIT = 300
# Users are allowed 'requests_limit' requests in 'request_time' seconds:
REQUESTS_TIME = 60 * 15

# redis (mandatory if requests_limit activated)
# REDIS_URL = "redis://redisserver:6379/0"
REDIS_URL = False

# Use cache type (null by default)
# View http://pythonhosted.org/Flask-Cache/#configuring-flask-cache
# for types and configuration options
CACHE = {'CACHE_TYPE' : 'null'}
# Minimun timeout for function caching
CACHE_MIN_TIMEOUT = 0

# Use Http Authentication for public scopes
AUTH_ENABLED = False

# Extend the API functionality by enabling additional modules/plugins
MODULES = {
    # reports endpoints
    # 'goteoapi_reports.controllers',
    # digests endpoints
    # 'goteoapi_digests.controllers'
}

# debug (False by default)
DEBUG = False

#Year when goteo started
INITIAL_YEAR = 2011

#Api description
DESCRIPTION = 'Goteo.org Api'
#Api base path (useful for swagger-ui) in case is prefixed
BASE_PATH = ''

#Timezone used in Goteo database
# timezone = 'US/Eastern'
TIMEZONE = 'Europe/Madrid'

# Default language used in Goteo
DEFAULT_LANG = 'es'

# Default db language used in Goteo
DEFAULT_DB_LANG = 'es'

# Some usefull links
LINKS = {
    'Swagger Interface' : '/spec',
    'Swagger Documentation' : '/apidocs/index.html'
}

# Built-in Users Authentication
USERS = {}

# Api version
VERSION = "1.1"
