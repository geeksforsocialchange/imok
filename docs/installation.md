# Setting up an imok server

These instructions focus on Digital Ocean but should work for any VPS service. This guide currently assumes you are developing imok locally.

We use the open source Heroku clone [Dokku](http://dokku.viewdocs.io/dokku/) and a Postgresql database.

## Getting started

You will need:

1. A server.  We'll walk you through some different options for that later in the document.
1. A Telegram account to use for creating a Telegram bot.  This enables the system to run for almost free.
1. (optional) A [Twilio account](https://www.twilio.org/) for using imok via SMS. Twilio give generous credits to registered charities. [You can check your eligibility here](https://www.twilio.org/check-eligibility/).
1. A domain name to use with the service. This guide assumes you will install imok on a subdomain, e.g. `imok.mydomain.com`.

### Setting up Telegram

Send `/newbot` to @BotFather and follow the instructions. It will give you a token to use.

You need this token to configure IMOK to use the token to send replies

You also need to use this token to tell your bot about IMOK

On the server:

```shell
export BOT_TOKEN='123:abc'
# Only the hostname should need changing here
export WEBHOOK='https://imok.example.com/application/telegram'

curl "https://api.telegram.org/bot${BOT_TOKEN}/setWebHook?url=${WEBHOOK}"
```

## Installing imok

Follow the hosting-specific instructions to setup your server.

For development, we recommend Digital Ocean as we have the most experience with them and the server is charged on a per-minute basis.

For production, you may want to use a server in a more legally-friendly country, such as 1984.is

If you are using a server provider not listed here, then follow the [1984.is installation documentation](installation-1984.md) because it includes steps to install Dokku which isn't necessary on Digital Ocean.

* [Digital Ocean](installation-digital-ocean.md)
* [1984.is](installation-1984.md)

### Setting up Dokku

Hopefully you're now logged into the remote server and the prompt says `root@HOSTNAME`. Type the following commands to set up the imok environment.

```shell
# Set up the server
apt update && apt upgrade --assume-yes # Select the default for all options that pop up
apt install pwgen

# Add your locale
locale-gen en_GB en_GB.UTF-8
dpkg-reconfigure locales # We recommend defaulting to en_GB.UTF-8 for UK installations

# Install needed plugins
dokku plugin:install https://github.com/dokku/dokku-postgres.git

# Create the app and database, and link the two
dokku apps:create imok
dokku postgres:create imok
dokku postgres:link imok imok
dokku config:set --no-restart imok DJANGO_SECRET_KEY=`pwgen 64 1`

# Configure Telegram using the information you created above.
dokku config:set --no-restart imok TELEGRAM_TOKEN="${BOT_TOKEN}"
# Configure imok to send admin notifications to a telegram group
dokku config:set imok TELEGRAM_GROUP="example-group"

# Allow HTTP requests to use the server IP address
dokku config:set imok ALLOWED_HOSTS=$(curl https://icanhazip.com)
```

Now browse to SERVER_IP in a web browser.

1. Set **Hostname** to the domain name you want to use, e.g. `imok.mydomain.com`.
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

This will take a little while to run as it pushes the code to the remote server and sets up the Dokku app.

### Create a superuser to login with and set up server storage

Back on your server run the following to set up an admin account.

```shell
dokku --rm run imok python manage.py createsuperuser
```

Follow the instructions on screen to create your root user login. Make sure to use a secure password.

Provide some storage for static content and generate the static content

```shell
dokku storage:mount imok /var/lib/dokku/data/storage:/code/static
dokku --rm run imok python manage.py collectstatic
dokku ps:restart imok # you'll get a 500 error if you don't restart after generating static content
```

### Configuring a domain name

Setting up a domain name is mandatory for imok in order to ensure https security for users.

In your domain name config you need to add an A record for the subdomain you want to use that points to the IP address of your server.

* Type: A Record
* Host: imok
* Value: YOUR_IP
* TTL: Automatic

On Namecheap this will look something like this:

![Example screenshot on Namecheap](dns-config.png)

Back on your imok server:

```shell
# Set the hostname
dokku domains:set imok imok.example.net
dokku config:set imok ALLOWED_HOSTS="$(curl https://icanhazip.com),imok.example.net"

# Install letsencrypt
dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku config:set --no-restart imok DOKKU_LETSENCRYPT_EMAIL=YOUR_EMAIL
dokku letsencrypt:enable imok
dokku letsencrypt:cron-job --add
```

HTTP traffic will be automatically redirected to HTTPS.  You need to leave the HTTP port in place because LetsEncrypt uses this for certificate renewals.

That's it! You've finished the basic setup. You can now log into your site at https://imok.mydomain.com/ruok.


## Optional steps

You might want to add a few extra features if you're going to use this in a production setting.

### Turn off invites

By default, users must be invited before they can use the service.  You can turn this off and allow anyone to use it:

```shell
dokku config:set imok REQUIRE_INVITE=False
```

### Configuring email

By default, imok will not send notification emails to admins.  To configure this you will need to set a few things:

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

### Configuring airbrake

If you want application errors to appear in an airbrake project, you can define the project and project key:

```shell
dokku config:set --no-restart imok AIRBRAKE_PROJECT=123456
dokku config:set --no-restart imok AIRBRAKE_PROJECT_KEY='780740ee075aeedacbbe794517ce64f2'
```

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

```shell
# Configure Twilio using the information you created above.
dokku config:set --no-restart imok TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
dokku config:set --no-restart imok TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxx
# Make sure to add the single quotes around your phone number
dokku config:set --no-restart imok TWILIO_FROM_NUMBER='+15005550000'
# If you are running somewhere other than Great Britain then set the country
dokku config:set --no-restart imok PHONENUMBER_DEFAULT_REGION=US

```

### Communication Channels

By default, both Twilio and Telegram are assumed to be supported and Telegram is the preferred channel.

You can override this:

```shell
dokku config:set imok SUPPORTED_CHANNELS=TELEGRAM,TWILIO
dokku config:set imok PREFERRED_CHANNEL=TELEGRAM
```

### Debugging

You can turn on debugging in production by setting 'DEBUG=True' (case-sensitive):

```shell
dokku config:set imok DEBUG=True
```

This will give you helpful errors, but should be turned off when the site is live:

```shell
dokku config:unset imok DEBUG
```
