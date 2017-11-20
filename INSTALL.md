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
sudo apt-get install python3-setuptools python-dev python3-dev build-essential
sudo apt-get install libffi6 libffi-dev libevent1-dev libmysqlclient-dev libpython-dev
sudo apt-get install python-virtualenv
sudo apt-get install redis-server python-redis
sudo apt-get install python3-pip
sudo pip3 install virtualenvwrapper
```

For others systems, please refer to the oficial documentation for redis or pip.

There are two options for installing the system:

1. If you prefer to have everything organized in the same place (such as `/your/user/path/.virtualenv`), you can use the `mkvirtualenv` script as many other packages does:

    ```bash
    mkdir ~/.virtualenvs
    echo "export WORKON_HOME=~/.virtualenvs" >> ~.bashrc
    echo "VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'" >> ~.bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~.bashrc
    mkvirtualenv goteoapi
    ./deployer
    ```

2. Otherwise, you can just use the `deployer` script bash script witch will create the virtual environment in the same directory as the code. This option won't mess or touch any personal configuration files (such as `~/.bashrc`. This is the method used by the real web server for instance. Just run:

    ```bash
    ./deployer
    ```

    This will install all required dependencies.

### Configuration

You should create a properly configured settings file, just copy the example config file and edit the result `config.py` file with your personal database credentials and preferences:

```bash
cp config.py.example config.py
```

Alternatively, a config file can be read from the env var `GOTEO_API_CONFIG_FILE`. This configuration file will be parsed **after** the normal `config.py` file;

```bash
export GOTEO_API_CONFIG_FILE=/path/to/config/file.py
```

### Using Vagrant

For convenience, a `Vagrantfile` is provided to automatically set up a pre-configured development environment.  You'll need [Vagrant](https://www.vagrantup.com/) and some virtual machine application like [Virtualbox](https://www.virtualbox.org/wiki/Downloads)

To install the system using vagrant, just run:

```bash
vagrant up
vagrant ssh
```

The vagrant provisioning script automatically creates the `GOTEO_API_CONFIG_FILE` environment var pointing to the `config_vagrant.py` configuration file. This file must be created by the user, if this file does not exists `GOTEO_API_CONFIG_FILE` will point to the fallback `config_vagrant.py.dist` file.

### Running the local server

By default, local server listens to http://0.0.0.0:5000/

1. If you have used method 1 (global virtualenv installation), execute this commands and you'll be up and running:

    ```bash
    workon goteoapi
    ./run
    ```

2. If you have chosen method 2 or are using Vagrant, just run the script:

    ```bash
    ./run
    ```

Now it is time to point your browser (or curl) to http://0.0.0.0:5000/

Checkout the README.md file for more info.
