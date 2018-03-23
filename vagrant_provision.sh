#!/usr/bin/env bash
export DEBIAN_FRONTEND=noninteractive
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
mysql -uroot -proot goteodev < /home/ubuntu/goteo-api/goteoapi/tests/sql/schema_mysql.sql
mysql -uroot -proot goteodev < /home/ubuntu/goteo-api/goteoapi/tests/sql/data_mysql.sql
mysql -utravis goteotest < /home/ubuntu/goteo-api/goteoapi/tests/sql/schema_mysql.sql
mysql -utravis goteotest < /home/ubuntu/goteo-api/goteoapi/tests/sql/data_mysql.sql

# Install Python libs
sudo apt-get install -y python3-setuptools python3-dev build-essential
sudo apt-get install -y libffi6 libffi-dev libevent1-dev libmysqlclient-dev libpython3-dev
sudo apt-get install -y python-virtualenv virtualenvwrapper
sudo apt-get install -y redis-server python-redis
sudo apt-get install -y python3-pip
sudo apt-get install -y libmysqlclient-dev libffi-dev
sudo pip3 install virtualenvwrapper

if [ ! -f /home/ubuntu/.bash_profile ]; then
    touch /home/ubuntu/.bash_profile
    echo "if [ -f ~/.bashrc ]; then" >> /home/ubuntu/.bash_profile
    echo "   source ~/.bashrc" >> /home/ubuntu/.bash_profile
    echo "fi" >> /home/ubuntu/.bash_profile
    echo 'export LC_ALL="en_US.UTF-8"' >> /home/ubuntu/.bash_profile
    chown ubuntu.ubuntu /home/ubuntu/.bash_profile
fi

if [ "$(grep -c 'GOTEO_API_CONFIG_FILE=' .bash_profile)" = "0" ]; then
    echo "if [ -f /home/ubuntu/goteo-api/config_ubuntu.py ]; then" >> /home/ubuntu/.bash_profile
    echo "  export GOTEO_API_CONFIG_FILE=/home/ubuntu/goteo-api/config_ubuntu.py" >> /home/ubuntu/.bash_profile
    echo "else" >> /home/ubuntu/.bash_profile
    echo "  export GOTEO_API_CONFIG_FILE=/home/ubuntu/goteo-api/config_ubuntu.py.dist" >> /home/ubuntu/.bash_profile
    echo "fi" >> /home/ubuntu/.bash_profile
fi


sudo -H -u ubuntu bash -l -c "/home/ubuntu/goteo-api/deployer"

# autochange to development dir on login
if [ "$(grep -c 'cd ~/goteo-api' .bash_profile)" = "0" ]; then
    echo 'cd ~/goteo-api' >> /home/ubuntu/.bash_profile
fi
