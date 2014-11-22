#!/bin/bash
#
# This script will run all operations needed in order to provide
# a self-contained environment for the pytohn app
#

/usr/bin/virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt

if [ $? == "0" ]; then
	echo -e "\e[32mDone, if you want to execute the Flask application manually please run this commands:\e[0m"
	echo "source virtualenv/bin/activate"
	echo "./goteoapi-restful.py"
fi