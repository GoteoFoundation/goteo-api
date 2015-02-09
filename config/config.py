import settings


if hasattr(settings, 'requests_limit') and hasattr(settings, 'redis_uri'):
	requests_limit = settings.requests_limit
	REDIS_URI = settings.redis_uri
else:
	requests_limit = 0
	REDIS_URI = False

# api requests rate limit
# NEEDS REDIS_URL CONFIGURED
# Users are allowed 'requests_limit' requests in 'request_time' seconds:
if hasattr(settings, 'requests_time'):
	requests_time = settings.requests_time
else:
	requests_time = 60 * 15

if hasattr(settings, 'auth_enabled'):
	auth_enabled = settings.auth_enabled
else:
	auth_enabled = False

#Debug
if hasattr(settings, 'debug'):
	debug = settings.debug
else:
	debug = False

#Api description
if hasattr(settings, 'description'):
	description = settings.description
else:
	description = 'Goteo.org Api'

# Some usefull links
if hasattr(settings, 'links'):
	links = settings.links
else:
	links = {
		'Developers Documentation' : 'http://developers.goteo.org',
		'Swagger Interface' : 'http://api.goteo.org/v1/api/spec.html'
	}

# Generic valid auths
if hasattr(settings, 'users'):
	users = settings.users
else:
	users = {}

# Api version
version = 1.0

# DB URI
DB_URI = 'mysql://' + settings.dbuser + ':' + settings.dbpass + '@' + settings.dbhost + '/' + settings.dbname

#USEFULL VARS

#PROJECT STATUS IDs
PROJECT_STATUS_REJECTED = 0
PROJECT_STATUS_EDITING = 1
PROJECT_STATUS_REVIEWING = 2
PROJECT_STATUS_IN_CAMPAIGN = 3
PROJECT_STATUS_FUNDED = 4
PROJECT_STATUS_FULLFILED = 5 # 'Caso de exito'
PROJECT_STATUS_UNFUNDED = 6 # proyecto fallido

#INVEST STATUS IDs
INVEST_STATUS_PROCESSING = -1
INVEST_STATUS_PENDING = 0
INVEST_STATUS_CHARGED = 1
INVEST_STATUS_CANCELED = 2
INVEST_STATUS_PAID = 3
INVEST_STATUS_RETURNED = 4
INVEST_STATUS_RELOCATED = 5

#CALL STATUS IDs
CALL_STATUS_CANCELED = 0
CALL_STATUS_EDITING = 1
CALL_STATUS_REVIEWING = 2
CALL_STATUS_APPLYING = 3
CALL_STATUS_PUBLISHING = 4
CALL_STATUS_COMPLETED = 5
CALL_STATUS_EXPIRED = 6