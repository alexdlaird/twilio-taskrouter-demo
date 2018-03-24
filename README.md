[![Build Status](https://travis-ci.org/alexdlaird/twilio-taskrouter-demo.svg?branch=master)](https://travis-ci.org/alexdlaird/twilio-taskrouter-demo)
[![codecov](https://codecov.io/gh/alexdlaird/twilio-taskrouter-demo/branch/master/graph/badge.svg)](https://codecov.io/gh/alexdlaird/twilio-taskrouter-demo)


TwilTwil
================

## Prerequisites
* Python (>= 3.6)
* Pip (>= 9.0)

## Getting Started
The project is developed using Python and [Django](https://www.djangoproject.com).

This repository contains the source code for the TwilTwil project, ChaCha using [Twilio's TaskRouter](https://www.twilio.com/taskrouter).

### Project Setup
To setup the Python/Django build environment, execute:

```
make install
```

To ensure the database is in sync with the latest schema, database migrations are generated and run with Django. To run migrations, execute:

```
make migrate
```

Once migrations have been run, you can create a super user, which is a standard user that also has access to the /admin site.

```
python manage.py createsuperuser
```

Now you're all set! To start the development server, execute:

```
python manage.py runserver
```

A development server will be started at http://localhost:8000.