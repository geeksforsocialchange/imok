# Development

For local development we use docker-compose so that we don't need to configure postgresql.

1. `docker-compose up` to launch a postgresql database and the webserver
2. `docker-compose run web python manage.py migrate` to run database migrations
3. `docker-compose run web python manage.py createsuperuser` to create an admin user

You may also want to `pip install -r requirements.txt` outside of Docker to get code completion in your editor

## Internationalisation

You should assume that we need to provide everything in multiple languages and support multiple timezones.

Specifically, you should make all strings translatable though:

```python
from django.utils.translation import gettext as _
myvar = _("A string that a user or administrator will see")
print(myvar)
```

We are, however, not yet using any language other than en_gb.

## Testing

Tests are written using BDD in the features directory.

To run the tests:

`docker-compose run web python manage.py behave --simple`

We also provide webhook.py for use with manual testing of the Twilio webhooks.  It allows you to send a message to the system as follows:

```shell
python webhook.py -f +15005550006 -m "NAME alice"
```

You can also achieve this through an HTTP Post using your favorite client:

```shell
curl -X POST --data '{"Body": "NAME alice", "From": "+15005550006"}' localhost:8000/application/twilio
```

## CI/CD

We use Github Actions to run the BDD tests on push. There is currently no automation to deploy anywhere.
