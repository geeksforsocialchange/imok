# Important Settings

This document describes all the important settings in once place. These are all set as environment variables:

```shell
dokku config:set imok KEY=value
```

## Imok

These settings are specific to imok.

| Key | Default | Description |
|-----|---------|-------------|
| TELEGRAM_TOKEN       | ''              | Bot token for the Telegram bot |
| TELEGRAM_GROUP       | ''              | Telegram group to send admin notifications to |
| REQUIRE_INVITE       | True            | Require members to be invited through the admin panel before they can use imok |
| NOTIFY_EMAIL         | ''              | The email address to send admin notifications to |
| MAIL_FROM            | root@localhost  | The email address that emails will come from  |
| AIRBRAKE_PROJECT     | ''              | An Airbrake project ID for collecting errors |
| AIRBRAKE_PROJECT_KEY | ''              | An Airbrake project key for collecting errors |
| TWILIO_ACCOUNT_SID   | ''              | Twilio account SID |
| TWILIO_AUTH_TOKEN    | ''              | Twilio auth token |
| TWILIO_FROM_NUMBER   | ''              | The phone number you have registered to use in Twilio |
| SUPPORTED_CHANNELS   | TELEGRAM,TWILIO | A comma separated list of channels you want to support (currently only telegram and twilio) |
| PREFERRED_CHANNEL    | TELEGRAM        | The default channel to contact members through (can be overridden by member) |

## Dokku

| Key | Default | Description |
|-----|---------|-------------|
| DOKKU_LETSENCRYPT_EMAIL | '' | Email address to register an SSL certificate with |

## Django

These settings are generic Django settings that are important to know about

| Key | Default | Description | Documentation |
|-----|---------|-------------|---------------|
| DJANGO_SECRET_KEY          | ''          | used for sessions and password reset tokens | https://docs.djangoproject.com/en/dev/ref/settings/#secret-key |
| ALLOWED_HOSTS              | 'localhost' | A list of hostnames that Django is allowed to serve | https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts |
| EMAIL_HOST                 | 'localhost' | The email server to use | https://docs.djangoproject.com/en/dev/ref/settings/#email-host |
| EMAIL_PORT                 | 25          | Port to use for the SMTP server defined in EMAIL_HOST | https://docs.djangoproject.com/en/dev/ref/settings/#email-port |
| EMAIL_HOST_USER            | ''          | An optional username for the SMTP server defined in EMAIL_HOST | https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user |
| EMAIL_HOST_PASSWORD        | ''          | An optional password for the SMTP server defined in EMAIL_HOST | https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user |
| EMAIL_USE_TLS              | False       | Whether to use TLS for the SMTP server defined in EMAIL_HOST   | https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls |
| EMAIL_USE_SSL              | False       | Whether to use SSL for the SMTP server defined in EMAIL_HOST   | https://docs.djangoproject.com/en/dev/ref/settings/#email-use-ssl |
| PHONENUMBER_DEFAULT_REGION | GB          | A region supported by libphonenumber in order to accept telephone numbers in the local format | https://github.com/stefanfoulis/django-phonenumber-field |

