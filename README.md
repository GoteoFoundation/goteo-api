GOTEO API
=========

[![Build Status](https://travis-ci.org/GoteoFoundation/goteo-api.svg?branch=master)](https://travis-ci.org/GoteoFoundation/goteo-api) [![Code Climate](https://codeclimate.com/github/GoteoFoundation/goteo-api/badges/gpa.svg)](https://codeclimate.com/github/GoteoFoundation/goteo-api) [![Test Coverage](https://codeclimate.com/github/GoteoFoundation/goteo-api/badges/coverage.svg)](https://codeclimate.com/github/GoteoFoundation/goteo-api/coverage)

This is the code for the [goteo api](http://api.goteo.org/).

Please referer to the INSTALL.md file for info about installing this API.

Full documentation to use the official api can be found here: https://developers.goteo.org/doc/

Flask command line order:
----------

Cache clearing:

```bash
./console clearcache
```

Cache renewing:

```bash
./console renewcache
```

Crontab install for automatic cache renew:

```bash
./console crontab -i
```

Remove crontab install:
```bash
./console crontab -r
```

Running tests:
----------

**NOTE:** Testing with the argument `--reset-database` will remove all tables in the test database!

Configure a proper `config_test.py` before testing

First time you may want to reste the test database:

```bash
./run-tests --reset-database
```

All tests at once (verbose):

```bash
./run-tests -v
```

Specific tests: (verbose, with echoes):

```bash
./run-tests goteoapi -v -s goteoapi/tests/testprojects.py
```

Running code coverage tests:

```bash
./run-tests --cover-html --with-coverage
```

Running code coverage tests with all packages:

```bash
./run-tests --cover-html --with-coverage --cover-package=goteoapi_reports --cover-package=goteoapi_digests
```

Tests uses [nosetests](https://nose.readthedocs.org). Same nosetests command arguments applies to `run-tests` script

Install/update dependencies:
----------

```bash
./deployer
```

Run a test server on localhost:
----------

```bash
./run
```

To run the API with extra packages you must configure the variable `MODULES` int the file `config.py` (extra packages such as: goteoapi_reports, goteoapi_digests)

```python
...

MODULES = {
    # reports endpoints
    'goteoapi_reports.controllers',
    # digests endpoints
    'goteoapi_digests.controllers'
}

...
```

Examples
----------

Obtain a list of active projects:

```bash
curl -i --user "goteo:goteo" http://0.0.0.0:5000/projects
```

Getting details for a custom project:

```bash
curl -i --user "goteo:goteo" http://0.0.0.0:5000/projects/project-id
```

Filtering some data, in this case, all projectes published starting in october 2015:

```bash
curl --user "goteo:goteo" -i -X GET -H "Content-Type: application/json" -d '{"from_date":"2015-10-01"}' http://localhost:5000/projects/
```

Obtaining an error message:

```bash
curl -i --user "goteo:goteo" -X GET -H "Content-Type: application/json" http://0.0.0.0:5000/projects/
```

Response:

```json
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 53
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: POST, OPTIONS, GET
Access-Control-Allow-Headers: Authorization
Access-Control-Max-Age: 1
Server: Werkzeug/0.10.4 Python/2.7.6
Date: Mon, 01 Feb 2016 13:36:53 GMT

{
    "message": "Bad Request",
    "status": 400
}
```

Check the full documentation here: https://developers.goteo.org/doc/

License
-------

The code licensed here under the **GNU Affero General Public License**, version 3 AGPL-3.0 has been developed by the Goteo team led by Platoniq and subseque
ntly transferred to the Fundación Goteo, as detailed in http://www.goteo.org/about#info6

This is a web tool that allows the receipt, review and publishing of collective campaigns for their collective funding and the receiving of collaborations a
s well as the dynamic visualization of the support received, classification of initiatives and campaign tracking. The system also permits secure and distrib
uted communication with users and between users, administration of highlighted projects on the home page and the creation of periodical publications such as
 blogs, a FAQ section and static pages.



