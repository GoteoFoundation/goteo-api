#!/usr/bin/env bash

sudo apt-get update
sudo apt-get -y upgrade

# Install MySQL
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get install -y mysql-server

# fully accessible database
if [ "$(grep -c '#bind-address' /etc/mysql/my.cnf)" = "0" ]; then
    cat /etc/mysql/my.cnf | sed -e "s/bind-address$(printf '\t\t')= 127.0.0.1/#bind-address        = 127.0.0.1/" > /etc/mysql/my.cnf
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';" -proot
    mysql -e "GRANT ALL PRIVILEGES ON goteotest.* TO 'travis'@'%';" -proot
    iptables -t nat -A PREROUTING -i lo -p tcp --dport 3307 -j REDIRECT --to-port 3306
    iptables-save
    service mysql restart
fi

# Install goteodev & goteotest database
mysql -uroot -proot -e "CREATE DATABASE goteodev;"
mysql -uroot -proot -e "CREATE DATABASE goteotest;"
mysql -uroot -proot goteodev < /home/vagrant/goteo-api/goteoapi/tests/sql/schema_mysql.sql
mysql -uroot -proot goteodev < /home/vagrant/goteo-api/goteoapi/tests/sql/data_mysql.sql
mysql -utravis goteotest < /home/vagrant/goteo-api/goteoapi/tests/sql/schema_mysql.sql
mysql -utravis goteotest < /home/vagrant/goteo-api/goteoapi/tests/sql/data_mysql.sql

# Install Python libs
sudo apt-get install -y python3-setuptools python3-dev build-essential
sudo apt-get install -y libffi6 libffi-dev libevent1-dev libmysqlclient-dev libpython3-dev
sudo apt-get install -y python-virtualenv virtualenvwrapper
sudo apt-get install -y redis-server python-redis
sudo apt-get install -y python3-pip
sudo pip3 install virtualenvwrapper

if [ ! -d /home/vagrant/.virtualenvs ]; then
    mkdir /home/vagrant/.virtualenvs
    chown vagrant.vagrant /home/vagrant/.virtualenvs
fi

if [ ! -f /home/vagrant/.bash_profile ]; then
    touch /home/vagrant/.bash_profile
    echo "if [ -f ~/.bashrc ]; then" >> /home/vagrant/.bash_profile
    echo "   source ~/.bashrc" >> /home/vagrant/.bash_profile
    echo "fi" >> /home/vagrant/.bash_profile
    chown vagrant.vagrant /home/vagrant/.bash_profile
fi

if [ "$(grep -c 'WORKON_HOME=~/.virtualenvs' .bash_profile)" = "0" ]; then
    echo "export WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bash_profile
    echo "VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'" >> /home/vagrant/.bash_profile
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bash_profile
fi


if [ "$(grep -c 'GOTEO_API_CONFIG_FILE=' .bash_profile)" = "0" ]; then
    echo "if [ -f /home/vagrant/goteo-api/config_vagrant.py ]; then" >> /home/vagrant/.bash_profile
    echo "  export GOTEO_API_CONFIG_FILE=/home/vagrant/goteo-api/config_vagrant.py" >> /home/vagrant/.bash_profile
    echo "else" >> /home/vagrant/.bash_profile
    echo "  export GOTEO_API_CONFIG_FILE=/home/vagrant/goteo-api/config_vagrant.py.dist" >> /home/vagrant/.bash_profile
    echo "fi" >> /home/vagrant/.bash_profile
fi

if [ ! -d /home/vagrant/.virtualenvs/goteoapi ]; then
    sudo -H -u vagrant bash -l -c "mkvirtualenv goteoapi"
fi

if [ "$(grep -c 'workon goteoapi' .bash_profile)" = "0" ]; then
    echo "workon goteoapi" >> /home/vagrant/.bash_profile
fi

sudo -H -u vagrant bash -l -c "pip install -r /home/vagrant/goteo-api/requirements.txt"
sudo -H -u vagrant bash -l -c "pip install -r /home/vagrant/goteo-api/goteoapi_*/requirements.txt"

# autochange to development dir on login
if [ "$(grep -c 'cd ~/goteo-api' .bash_profile)" = "0" ]; then
    echo 'cd ~/goteo-api' >> /home/vagrant/.bash_profile
fi
