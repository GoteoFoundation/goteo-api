# GOTEO API

This is the code for the [goteo api](http://api.goteo.org/). 

Please referer to the INSTALL.md file for info about installing this API.

Full documentation to use the official api can be found here: https://developers.goteo.org/doc/

## Flask command line order:

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

## Running tests:

All tests at once (verbose):

```bash
./run-tests -v
```

Specific tests: (verbose, with echoes):

```bash
./run-tests goteoapi -v -s
```

Running code coverage tests:

```bash
./run-tests --cover-html --with-coverage
```

Tests uses [nosetests](https://nose.readthedocs.org). Same nosetests command arguments applies to `run-tests` script

## Install/update dependencies:

```bash
./deployer
```

## Run a test server on localhost:

```bash
./run
```

Or (extra packages added: goteoapi_reports, goteoapi_digests)

```bash
./run-goteo
```

## Examples

Obtain a list of active projects:

```bash
curl -i http://0.0.0.0:5000/projects
```

Getting details for a custom project:

```bash
curl -i http://0.0.0.0:5000/projects/057ce063ee014dee885b13840774463c
```

Filtering some data, in this case, all projectes published starting in october 2015:

```bash
curl --user "goteo:goteo" -i -X GET -H "Content-Type: application/json" -d '{"from_date":"2015-10-01"}' http://localhost:5000/projects/
```

Obtaining an error message:

```bash
curl -i -X GET -H "Content-Type: application/json" http://0.0.0.0:5000/projects
```

Response:

    HTTP/1.0 400 BAD REQUEST
    Content-Type: application/json
    Content-Length: 53
    Server: Werkzeug/0.9.6 Python/2.7.6
    Date: Sun, 05 Oct 2014 10:30:41 GMT
    
    {
        "message": "Bad Request",
        "error": 400
    }

Check the full documentation here: https://developers.goteo.org/doc/

## Notes

- Check version [versión 2.0](https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md) for swagger compatibility in the flask-restful-swagger (currently in 1.2).

Mor info here:
https://github.com/rantav/flask-restful-swagger/issues/50#issuecomment-65641980
