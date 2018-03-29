#!/usr/bin/env bash

sudo mkdir -p /usr/local/venvs
sudo chown ubuntu:ubuntu /usr/local/venvs

cd /srv/twiltwil

make install
make migrate
