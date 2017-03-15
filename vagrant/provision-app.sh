sudo apt-get -y update
sudo apt-get -y install apache2

###
# Set database password below
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password seniorproj'
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password seniorproj'
####

sudo apt-get install -y mysql-server-5.5 
sudo apt-get install -y libapache2-mod-auth-mysql
sudo apt-get install -y libapache2-mod-wsgi python-dev
sudo apt-get install -y python-pip
sudo service mysql start

###
# Enter database password again
mysql -u root --password=seniorproj < /vagrant/db/Predictor-setup.sql
mysql -u root --password=seniorproj < /vagrant/db/Predictor-build.sql
###

sudo a2enmod wsgi
sudo apt-get install -y python-pip
sudo pip install Flask
sudo pip install PyGithub
sudo apt-get -y install git
sudo apt-get -y install libapache2-mod-wsgi
sudo apt-get -y install python-pip python-dev libmysqlclient-dev
sudo pip install MySQL-python
sudo apt-get install -y python-numpy python-scipy
sudo pip install sklearn
sudo pip install nltk
sudo pip install python-levenshtein
cp /vagrant/Predictor.conf /etc/apache2/sites-available/Predictor.conf
cp -r /vagrant/code/ /var/www/Predictor
cp /vagrant/wsgi.conf /etc/apache2/mods-available/wsgi.conf
cp -r /vagrant/nltk_data /var/www/
sudo a2ensite Predictor
sudo apache2 restart
