# I'm OK (imok)

A bot that alerts a friend after a given period of time if you don't let it know you're ok. Intended use cases are first dates, travel across risky areas, and for those at risk of being deported.

Platforms supported: SMS, Telegram

## Installation

Provide Digital Ocean 1-click option

API keys needed: Twilio

Config options: admin email

## How it works (users)

## How it works (admins)

## Contributing

You can run this locally with the following steps:

1. `docker-compose up` to launch a postgresql database and the webserver
2. `docker-compose run web python manage.py migrate application` to run database migrations
3. `docker-compose run web python manage.py createsuperuser` to create an admin user

You may also want to `pip install -r requirements.txt` outside of Docker to get code completion in your editor

If you need to use a database other than the docker postgresql container, you can edit `DATABASES` in imok/settings.py

### Testing

You should be able to login to http://localhost:8000/admin using the admin user you created in step 3 above, and then register users on the system 

You should be able to send a mock SMS into the system with:

```shell
curl -X POST --data '{"Body": "in", "From": "+447763858444"}' localhost:8000/application/twilio`
```

### Known issues

* Twilio integration is untested
* Users can't set their own name and self-register
* Users can't checkout
* Nothing is scanning for timed-out checkouts
* Telegram integration is missing
* Production deployment still needs thinking about