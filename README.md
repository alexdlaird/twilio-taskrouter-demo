[![Build Status](https://travis-ci.org/alexdlaird/twilio-taskrouter-demo.svg?branch=master)](https://travis-ci.org/alexdlaird/twilio-taskrouter-demo)
[![codecov](https://codecov.io/gh/alexdlaird/twilio-taskrouter-demo/branch/master/graph/badge.svg)](https://codecov.io/gh/alexdlaird/twilio-taskrouter-demo)
[![Updates](https://pyup.io/repos/github/alexdlaird/twilio-taskrouter-demo/shield.svg)](https://pyup.io/repos/github/alexdlaird/twilio-taskrouter-demo/)
[![Python 3](https://pyup.io/repos/github/alexdlaird/twilio-taskrouter-demo/python-3-shield.svg)](https://pyup.io/repos/github/alexdlaird/twilio-taskrouter-demo/)

# TwilTwil

## Prerequisites

- Python (>= 3.6)
- Pip (>= 9.0)

## Getting Started
The project is developed using Python and [Django](https://www.djangoproject.com).

This repository contains the source code for the TwilTwil project, ChaCha using [Twilio's TaskRouter](https://www.twilio.com/taskrouter).

### Project Setup

To setup the Python/Django build environment, execute:

```sh
make install-dev
```

Create a Twilio account and purchase a phone number. You'll also need to generate a [Twilio API key](https://www.twilio.com/docs/iam/keys/api-key-resource).

Update the `.env` file and set the following variables:

* `TWILTWIL_TWILIO_ACCOUNT_SID`
* `TWILTWIL_TWILIO_AUTH_TOKEN`
* `TWILTWIL_TWILIO_PHONE_NUMBER`
* `TWILTWIL_TWILIO_API_KEY`
* `TWILTWIL_TWILIO_API_SECRET`

To ensure the database is in sync with the latest schema, database migrations are generated and run with Django. To run migrations, execute:

```sh
make migrate
```

Once migrations have been run, you can create a super user, which is a standard user that also has access to the /admin site.

```sh
python manage.py createsuperuser
```

Now you're all set! To start the development server, execute:

```sh
python manage.py runserver
```

A development server will be started at <http://localhost:8000>.

If the `USE_NGROK` environment variable is set when a dev server is started (using `runserver`, [pyngrok](https://github.com/alexdlaird/pyngrok)
will be used to open a `ngrok` tunnel. This is especially useful when using webhooks.
