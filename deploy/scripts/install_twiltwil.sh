#!/usr/bin/env bash

cd /srv/twiltwil

sudo mkdir -p ${TWILTWIL_VENV}

make install
make migrate
