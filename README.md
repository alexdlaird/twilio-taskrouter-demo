![Python Versions](https://img.shields.io/badge/python-%203.9%20|%203.10%20|%203.11%20-blue)
[![Coverage](https://img.shields.io/codecov/c/github/alexdlaird/twilio-taskrouter-demo)](https://codecov.io/gh/alexdlaird/twilio-taskrouter-demo)
[![Build](https://img.shields.io/github/actions/workflow/status/alexdlaird/twilio-taskrouter-demo/build.yml)](https://github.com/alexdlaird/twilio-taskrouter-demo/actions/workflows/build.yml)
![GitHub License](https://img.shields.io/github/license/alexdlaird/twilio-taskrouter-demo)

# TwilTwil

## Getting Started
The project is developed using Python and [Django](https://www.djangoproject.com).

This repository contains the source code for the TwilTwil project, ChaCha using [Twilio's TaskRouter](https://www.twilio.com/taskrouter).

### Project Setup

To setup the Python/Django build environment, execute:

```sh
make install
```

Create a Twilio account and purchase a phone number. You'll also need to generate a [Twilio API key](https://www.twilio.com/docs/iam/keys/api-key-resource).

Update the `.env` file and set the following variables:

* `TWILTWIL_TWILIO_ACCOUNT_SID`
* `TWILTWIL_TWILIO_AUTH_TOKEN`
* `TWILTWIL_TWILIO_PHONE_NUMBER`
* `TWILTWIL_TWILIO_API_KEY`
* `TWILTWIL_TWILIO_API_SECRET`

This project is configured to work with a Virtualenv which has now been setup in the `venv` folder. If you're
unfamiliar with how this works, [read up on Virtualenv here](https://virtualenv.pypa.io/en/stable). The short version
is, virtualenv creates isolated environments for each project's dependencies. To activate and use this environment when
developing, execute:

```sh
source venv/bin/activate
```

All commands below will now be run within the virtualenv (though `make` commands will always automatically enter the
virtualenv before executing).

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
bin/runserver
```

A development server will be started at <http://localhost:8000>.

If the `USE_NGROK` environment variable is set when a dev server is started (using `runserver`, [pyngrok](https://github.com/alexdlaird/pyngrok)
will be used to open a `ngrok` tunnel. This is especially useful when using webhooks.
