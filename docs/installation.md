# Setting up an imok server

These instructions focus on Digital Ocean but should work for any VPS service. This guide currently assumes you are developing imok locally.

We use the open source Heroku clone [Dokku](http://dokku.viewdocs.io/dokku/) and a Postgresql database.

## Getting started

You will need:

1. A [Digital Ocean account](https://www.digitalocean.com/). If you don't have one yet please consider using our [referral link](https://m.do.co/c/34b6bc6a1cf7).
1. A [Twilio account](https://www.twilio.org/). Twilio give generous credits to registered charities. [You can check your eligibility here](https://www.twilio.org/check-eligibility/).

## Setting up Twilio

1. [Go to the Twilio console](https://www.twilio.com/console/projects/summary) and click **Create new account**
1. Write a memorable name and click OK.
1. Add a phone number. We recommend using a new SIM card just for this if you are doing sensitive work. Companies like GiffGaff [send them for free](https://www.giffgaff.com/free-sim-cards) (not an endorsement).
1. Pick 'With code', 'Python' and 'No, I want to use my own hosting service'. The rest you can answer how you like.
1. Click **Get a trial phone number** and then click 'Don't like this one? Search for a different number' in the top right (unless you are happy using a USA phone number).
1. Make sure your country is selected, and select **SMS** in the 'capabilities' choices.
1. Pick a phone number by pressing **buy**. This is the number that all messages from your service will come from.
1. Go back to the project dashboard by clicking in the top left where it says your project name.
1. Make a note of your **Account SID**, **Auth Token** and **Phone number** in a text file or notes app for later use.
1. That's enough for testing, but when you're ready you will need to upgrade your account to be able to send messages using the **Upgrade project** button.

## Installing imok

### Setting up a droplet

A 'droplet' is Digital Ocean's term for a virtual server.

Anything not listed here you can just leave as it is.

1. Click **Create** in the top right corner, and then **Droplets**
1. **Choose an image**
  1. Go to 'Marketplace' tab
  1. Search for 'dokku'
  1. Select 'Dokku 0.21.4 on Ubuntu 20.04' (or whatever the latest version is)
1. **Choose a plan:** 'Basic', 'Regular intel with SSD', '$5/mo'
1. **Choose a datacentre region:** pick whichever datacentre is closest to you
1. **Authentication:** we recommend using an SSH key method if you are able to follow the instructions in the interface. If not then a password is totally fine but make it a strong one, ideally using a strong password generator.
1. **Choose a hostname:** pick a memorable name for the server
1. **Enable backups:** this is up to you but we recommend it
1. Click **'Create Droplet'** and you're done!

### Signing into the droplet

You will then see a list of droplets in your interface. Give it a second while it sets up your new droplet.

1. Copy the IP address (e.g. 123.123.123.123)
1. In the terminal on your computer, type `ssh root@YOUR_IP`. Type 'yes' when it asks you if you want to proceed.

### Setting up Dokku

Hopefully you're now logged into the remote server and the prompt says `root@HOSTNAME`. Type the following commands to set up the imok environment.

```shell
# Set up the server
apt update && apt upgrade # Select 'yes', then select the default for all options
apt install pwgen

# Install needed plugins
dokku plugin:install https://github.com/dokku/dokku-postgres.git

# Create the app and database, and link the two
dokku apps:create imok
dokku postgres:create imok
dokku postgres:link imok imok
dokku config:set --no-restart imok DJANGO_SECRET_KEY=`pwgen 64 1`

# Configure Twilio using the information you created above.
dokku config:set --no-restart imok TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
dokku config:set --no-restart imok TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxx
# Make sure to add the single quotes around your phone number
dokku config:set --no-restart imok TWILIO_FROM_NUMBER='+15005550000'

# Provide some storage for static content and generate the static content
dokku storage:mount imok /var/lib/dokku/data/storage:/code/static
dokku --rm run imok python manage.py collectstatic

# Allow HTTP requests to use the server IP address
dokku config:set imok ALLOWED_HOSTS=$(curl https://icanhazip.com)
```

Now browse to SERVER_IP in a web browser.

1. Select **Use virtualhost naming for apps**.
1. Click **Finish Setup**.

### Setting up your local environment

Open up a terminal window on your local computer

```shell
git clone https://github.com/geeksforsocialchange/imok.git
cd imok
git remote add dokku dokku@SERVER_IP:imok
git push dokku
```

### Create a superuser to login with

Back on your server run the following to set up an admin account.

```shell
dokku --rm run imok python manage.py createsuperuser
```

Follow the instructions on screen to create your root user login. Make sure to use a secure password.

### Configuring email

By default imok will try and email root@localhost using a local SMTP server.  To get email notifications you will need to configure a few things.

```shell
dokku config:set --no-restart imok NOTIFY_EMAIL='alice@example.net'
dokku config:set --no-restart imok MAIL_FROM='alice@example.net'
dokku config:set --no-restart imok EMAIL_HOST='mail.example.com'
dokku config:set --no-restart imok EMAIL_PORT=587
dokku config:set --no-restart imok EMAIL_HOST_USER='alice'
dokku config:set --no-restart imok EMAIL_HOST_PASSWORD='Password123'
dokku config:set --no-restart imok EMAIL_USE_TLS=True
dokku ps:restart imok
```

### WIP: Setting up a domain name

_This section is incomplete_

```shell
# Install letsencrypt
dokku plugin:install letsencrypt
dokku config:set --no-restart imok DOKKU_LETSENCRYPT_EMAIL=YOUR_EMAIL
dokku letsencrypt imok
dokku letsencrypt:cron-job --add

# Set the hostname
dokku domains:add imok imok.example.net
dokku config:set imok ALLOWED_HOSTS="$(curl https://icanhazip.com),imok.example.net"

# Turn off HTTP (optional)
dokku proxy:ports-remove imok 80
```

Deploying Dokku is out of scope for this documentation, see the Dokku installation documentation and pick Debian as the base OS for simplicity.
