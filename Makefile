.PHONY: all env install nopyc clean build build-migrations migrate test

SHELL := /usr/bin/env bash
PYTHON_BIN ?= python
TWILTWIL_VENV ?= venv

all: build migrate test

env:
	cp -n .env.example .env | true

venv:
	$(PYTHON_BIN) -m pip install virtualenv --user
	$(PYTHON_BIN) -m virtualenv $(TWILTWIL_VENV)

install: env venv
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
