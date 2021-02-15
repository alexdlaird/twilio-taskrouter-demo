.PHONY: all env virtualenv install install-dev build build-migrations migrate test

SHELL := /usr/bin/env bash
TWILTWIL_VENV ?= .venv

all: env virtualenv install build migrate test

env:
	cp -n .env.example .env | true

virtualenv:
	if [ ! -d "$(TWILTWIL_VENV)" ]; then \
		python3 -m pip install virtualenv --user; \
        python3 -m virtualenv $(TWILTWIL_VENV); \
	fi

install: env virtualenv
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)

install-dev: install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python -m pip install -r requirements-dev.txt; \
	)

build: virtualenv
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py collectstatic --noinput; \
	)

build-migrations: env virtualenv install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py makemigrations; \
	)

migrate: virtualenv
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py migrate; \
	)

test: virtualenv
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python -m coverage run --source='.' manage.py test && python -m coverage html -d _build/coverage && python -m coverage xml -o _build/coverage/coverage.xml; \
	)
