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

# Optional config:
# ================

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
CACHE = { 'CACHE_TYPE' : 'null' }
# Minimun timeout for function caching
CACHE_MIN_TIMEOUT = 0

# Use Http Authentication
AUTH_ENABLED = False

# debug (False by default)
DEBUG = False

#Year when goteo started
INITIAL_YEAR = 2011

#Api description
DESCRIPTION = 'Goteo.org Api'

#Timezone used in Goteo database
# timezone = 'US/Eastern'
TIMEZONE = 'Europe/Madrid'

# Default language used in Goteo
DEFAULT_LANG = 'es'

# Default db language used in Goteo
DEFAULT_DB_LANG = 'es'

# Some usefull links
LINKS = {
    'Swagger Interface' : '/apidocs/spec.json',
    'Swagger Documentation' : '/apidocs/index.html'
}

# Built-in Users Authentication
# Users can be bind to a ip or a ip range using a mask (eg: ip/mask)
USERS = {
    'goteo' : {'password':'goteo', 'remotes' : ['127.0.0.0/16', '192.168.0.0/24']}
}

# Api version
VERSION = "1.1"


