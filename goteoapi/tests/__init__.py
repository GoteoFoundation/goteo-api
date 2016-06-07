import sys
import json
from .. import app

if '-v' in sys.argv:
    app.debug = True
    app.config['DEBUG'] = True

test_app = app.test_client()

# Import database

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
