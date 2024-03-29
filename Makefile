.PHONY: all env virtualenv install nopyc clean build build-migrations migrate test

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
		python -m pip install -r requirements.txt -r requirements-dev.txt; \
	)

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf build $(TWILTWIL_VENV)

build: install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py collectstatic --noinput; \
	)

build-migrations: install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py makemigrations; \
	)

migrate: install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		python manage.py migrate; \
	)

test: install
	( \
		source $(TWILTWIL_VENV)/bin/activate; \
		coverage run manage.py test && coverage report && coverage html && coverage xml; \
	)
