import sys
from .. import app
from nose.tools import eq_

app.config['TESTING'] = True
app.debug = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['CACHING'] = False
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_TIMEOUT'] = 300
app.config['CACHE_KEY_PREFIX'] = 'Test/'

test_app = app.test_client()

__import__('goteoapi.controllers')

if '-v' in sys.argv:
    app.debug = True
    app.config['DEBUG'] = True

def check_content_type(headers):
  eq_(headers['Content-Type'], 'application/json')


# def teardown():
#   # db_session.remove()
#   pass
