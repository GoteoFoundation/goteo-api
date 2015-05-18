# GOTEO API

## Flask command line order:

Cache clearing:

    ./console clearcache

Cache renewing:
    ./console renewcache

Crontab install for automatic cache renew:
    ./console crontab -i

Remove crontab install:
    ./console crontab -r

## Run tests:

All tests at once (verbose):
    ./run-tests -v

Specific tests: (verbose, with echoes):
    ./run-tests goteoapi -v -s

Running code coverage tests:
    ./run-tests --cover-html --with-coverage



Tests uses [nosetests](https://nose.readthedocs.org). Same nosetests command arguments applies to run-tests.sh

## Install/update dependencies:

    ./deployer

## Run a test server on localhost:

    ./run

Or (extra packages added: goteoapi_reports, goteoapi_digests)

    ./run-goteo
