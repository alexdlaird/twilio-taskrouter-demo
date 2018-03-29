#!/usr/bin/env bash

sudo mkdir -p /usr/local/venvs
sudo chown ubuntu:ubuntu /usr/local/venvs

cd /srv/twilio-taskrouter-demo

make install
make migrate
