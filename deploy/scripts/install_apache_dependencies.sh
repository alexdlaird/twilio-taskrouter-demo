#!/usr/bin/env bash

apt-get install -y vim apache2 libapache2-mod-wsgi-py3

a2enmod wsgi ssl

mkdir -p /var/apache2/log/
mkdir -p /var/twiltwil/log/

sudo cp /srv/twiltwil/deploy/conf/django.conf /etc/apache2/sites-available/twiltwil.conf

a2ensite twiltwil
