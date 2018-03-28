#!/usr/bin/env bash

apt-get install software-properties-common
add-apt-repository ppa:certbot/certbot
apt-get update

apt-get install -y vim apache2 libapache2-mod-wsgi-py3 python-certbot-apache

a2enmod wsgi ssl

mkdir -p /var/apache2/log/
mkdir -p /var/twiltwil/log/

sudo cp /srv/twiltwil/deploy/conf/django.conf /etc/apache2/sites-available/twiltwil.conf

a2dissite 000-default default-ssl
a2ensite twiltwil

certbot --apache --authenticator standalone --installer apache --non-interactive --agree-tos --email ${TWILTWIL_ADMIN_EMAIL} --domains twiltwil.alexlaird.com
