#!/usr/bin/env bash

isExistApp = `pgrep apache2`
if [[ -n  $isExistApp ]]; then
    service apache2 stop
fi
