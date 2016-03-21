import sys
import json
from .. import app

# TODO: from config
app.config['TESTING'] = True
app.debug = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['CACHING'] = False
app.config['REDIS_URL'] = None
app.config['CACHE_TYPE'] = 'null'
app.config['CACHE_TIMEOUT'] = 300
app.config['CACHE_KEY_PREFIX'] = 'Test/'
app.config['AUTH_ENABLED'] = False
redis_url = 'redis://localhost:6379/0'
app.config['REDIS_URL'] = redis_url

if '-v' in sys.argv:
    app.debug = True
    app.config['DEBUG'] = True

test_app = app.test_client()

__import__('goteoapi.controllers')

def get_json(rv_object):
  return json.loads(rv_object.get_data(as_text=True))

def get_swagger(file, objectName=None):
    import yaml
    docs = yaml.load_all(open(file, "r"))
    next(docs)
    yaml = next(docs)
    if not objectName:
        return yaml

    for k in yaml['definitions']:
        if k['schema']['id'] == objectName:
            return k['schema']['properties']


# def teardown():
#   # db_session.remove()
#   pass
