#!/usr/bin/env bash

cd /srv/twiltwil

mkdir -p ${TWILTWIL_VENV}

make install
make migrate
