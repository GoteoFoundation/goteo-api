#!/bin/bash
CURR=$(dirname $(readlink -f $0))

source "$CURR/"virtualenv/bin/activate
python "$CURR/"manage.py $@
