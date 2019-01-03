#!/usr/bin/env bash

isExistApp = $(pgrep apache2)
if [[ -n  $isExistApp ]]; then
    sudo service apache2 stop
fi
