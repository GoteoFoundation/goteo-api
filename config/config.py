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

#Timezone used in Goteo database
if hasattr(settings, 'timezone'):
	timezone = settings.timezone
else:
	# timezone = 'US/Eastern'
	timezone = 'Europe/Madrid'

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


