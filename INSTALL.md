## Goteo API

This is the code for the [goteo api](http://api.goteo.org/)

Made with python with [flask](http://flask.pocoo.org/), [sqlalchemy](http://www.sqlalchemy.org/) and [flask-restful](http://flask-restful.readthedocs.org)

### Installation

#### Requirements

    - Python 3.4
    - MySQL with a valid [Goteo database](https://github.com/GoteoFoundation/goteo)
    - Other python requirements can be installed using [pip](https://pip.pypa.io).
    - (Optional) REDIS server

This API uses [Redis](http://redis.io/) as a cache backend for complex SQL calculations and user/ratio management.

In Ubuntu 14.04 you can run this commands to install all requirements:

```bash
sudo apt-get install python-setuptools python-dev python3-dev build-essential
sudo apt-get install libffi6 libffi-dev libevent1-dev libmysqlclient-dev libpython-dev
sudo apt-get install python-virtualenv virtualenvwrapper
sudo apt-get install redis-server python-redis
sudo easy_install pip
```

For others systems, please refere to the oficial documentation for redis or pip.

There are two options for installing the system:

1. If you prefer to have everything organized in the same place (such as `/your/user/path/.virtualenv`), you can use the `mkvirtualenv` script as many other packages does:

    ```bash
    mkdir ~/.virtualenvs
    echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
    source ~/.bashrc
    mkvirtualenv goteoapi
    pip install -r requirements.txt
    ```

2. Otherwise, you can just use the `deployer` script bash script witch will create the virtual enviroment in the same directory as the code. This option won't mess or touch any personal configuration files (sucha as `~/.bashrc`. This is the method used by the real web server for instance. Just run:

    ```bash
    ./deployer
    ```

    This will install all required dependencies.

### Configuration

You should create a properly configured settings file, just copy the example config file and edit the result `config.py` file with your personal database credentials and preferences:

```bash
cp config.py.example config.py
```

### Running the local server

By default, local server listens to http://0.0.0.0:5000/

1. If you have used method 1 (global virtualenv installation), execute this commands and you'll be up and running:

    ```bash
    workon goteoapi
    ./run.py
    ```

2. If you have chosen method 2, just run the script:

    ```bash
    ./run
    ```

Now just point your browser (or curl) to http://0.0.0.0:5000/

Checkout the README.md file for more info.
