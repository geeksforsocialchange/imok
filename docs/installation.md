# Installation instructions

These instructions focus on Digital Ocean but should work for any VPS service.

We use the open source Heroku clone [Dokku](http://dokku.viewdocs.io/dokku/) and a Postgresql database.

## Getting started

You will need:

1. A [Digital Ocean account](https://www.digitalocean.com/). If you don't have one yet please consider using our [referral link](https://m.do.co/c/34b6bc6a1cf7).
1. A [Twilio account](https://www.twilio.org/). Twilio give generous credits to registered charities. [You can check your eligibility here](https://www.twilio.org/check-eligibility/).

## Installing imok

### Setting up a droplet

Anything not listed here you can just leave as it is.

1. **Create** a new droplet from the top right button
1. **Choose an image**
  1. Go to 'Marketplace' tab
  1. Search for 'dokku'
  1. Select 'Dokku 0.21.4 on Ubuntu 20.04' (or whatever the latest version is)
1. **Choose a plan:** 'Basic', 'Regular intel with SSD', '$5/mo'
1. **Choose a datacentre region:** whichever is closest to you
1. **Authentication:** we recommend using an SSH key method if you are able to follow the instructions in the interface. If not then a password is totally fine but make it a strong one, ideally using a strong password generator.
1. **Choose a hostname:** pick a memorable name for the server
1. **Enable backups:** this is up to you but we recommend it
1. Click **'Create Droplet'** and you're done!

### Signing into the droplet

You will then see a list of droplets in your interface.

1. Copy the IP address (e.g. 123.123.123.123)
1. In your terminal, type `ssh root@YOUR_IP`

### Setting up Dokku

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
