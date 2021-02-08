# Deployment Documentation

In test and production we deploy to [Dokku](http://dokku.viewdocs.io/dokku/) using a Postgresql database.  This can be any VPS.

## Dokku

Assuming a Dokku installation is available to use, and assuming the application name is `imok`, the configuration on the server should look something like the following:

```shell
# Install the postgres plugin
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git

# Create and link a postgres database
dokku postgres:link imok imok
dokku postgres:create imok

# Configure Twilio
dokku config:set --no-restart imok TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxx
dokku config:set --no-restart imok TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
dokku config:set --no-restart imok TWILIO_FROM_NUMBER='+15005550000'

dokku config:set --no-restart imok DJANGO_SECRET_KEY=`pwgen 64 1`

# Turn off HTTP (optional)
dokku proxy:ports-remove imok 80

# Provide some storage for static content
dokku storage:mount imok /var/lib/dokku/data/storage:/code/static

# Create a superuser to login with
dokku --rm run imok python manage.py createsuperuser
```

You can then add a git remote to push to:

```shell
git remote add dokku dokku@<ip address>:imok
```

Deploying Dokku is out of scope for this documentation, see the Dokku installation documentation and pick Debian as the base OS for simplicity.