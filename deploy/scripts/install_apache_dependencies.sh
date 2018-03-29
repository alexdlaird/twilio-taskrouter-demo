#!/usr/bin/env bash

sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:certbot/certbot
sudo apt-get update

sudo apt-get install -y vim apache2 libapache2-mod-wsgi-py3 python-certbot-apache

sudo a2enmod wsgi ssl

sudo mkdir -p /var/log/apache2
sudo mkdir -p /var/log/twiltwil
sudo chown ubuntu:ubuntu /var/log/twiltwil

sudo cp /srv/twiltwil/deploy/conf/django.conf /etc/apache2/sites-available/twiltwil.conf

sudo a2dissite 000-default default-ssl
sudo a2ensite twiltwil

sudo certbot --apache --authenticator standalone --installer apache --non-interactive --agree-tos --email ${TWILTWIL_ADMIN_EMAIL} --domains twiltwil.alexlaird.com
