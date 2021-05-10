"""
Django settings for imok project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from django.utils import timezone
import os
from pathlib import Path
import environ
import socket

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', 'vlek*n@f-!^ezbwfrris$vd6zqwza)yus44nvp28+mimi7)#i_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

SERVER_NAME = env.str('SERVER_NAME', 'imok')

# Use Alice's test credentials if nothing is set in environment variables
TWILIO_ACCOUNT_SID = env.str('TWILIO_ACCOUNT_SID', 'AC4a7b7b6bc015a2fd82d3eedea46c04f0')
TWILIO_AUTH_TOKEN = env.str('TWILIO_AUTH_TOKEN', '5886fb88ba4dd6bc45da49bc9d10a449')
TWILIO_FROM_NUMBER = env.str('TWILIO_FROM_NUMBER', '+15005550006')

TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN', '')
TELEGRAM_GROUP = env.str('TELEGRAM_GROUP', '')

SECURE_REFERRER_POLICY = "same-origin"
SECURE_BROWSER_XSS_FILTER = True

CHECKIN_TTL = timezone.timedelta(minutes=60)
WARNING_TTL = timezone.timedelta(minutes=55)

NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL', '')
MAIL_FROM = os.environ.get('MAIL_FROM', 'root@localhost')
EMAIL_SUBJECT_PREFIX = '[IMOK] '
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = (os.environ.get('EMAIL_USE_TLS', 'False') == 'True')
EMAIL_USE_SSL = (os.environ.get('EMAIL_USE_SSL', 'False') == 'True')

PHONENUMBER_DEFAULT_REGION = os.environ.get("PHONENUMBER_DEFAULT_REGION", "GB")

SUPPORTED_CHANNELS = os.environ.get("SUPPORTED_CHANNELS", "TELEGRAM,TWILIO").split(",")
PREFERRED_CHANNEL = os.environ.get("PREFERRED_CHANNEL", "TELEGRAM")
REQUIRE_INVITE = (os.environ.get('REQUIRE_INVITE', 'True') == 'True')

# Application definition

INSTALLED_APPS = [
    'application.apps.ApiConfig',
    'phonenumber_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imok.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imok.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'postgres',
           'USER': 'postgres',
           'PASSWORD': 'postgres',
           'HOST': '127.0.0.1',
           'PORT': '5432',
        }
    }

# Use environment variables for the database in Dokku, and use whitenoise and prod settings
if 'DATABASE_URL' in env:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
    ALLOWED_HOSTS.append(socket.getaddrinfo(socket.gethostname(), 'http')[0][4][0])
    DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
    DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    DEBUG = (os.environ.get('DEBUG', 'False') == 'True')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_PRELOAD = True

    AIRBRAKE_PROJECT = os.environ.get('AIRBRAKE_PROJECT', 0)
    AIRBRAKE_PROJECT_KEY = os.environ.get('AIRBRAKE_PROJECT_KEY', '')
    if AIRBRAKE_PROJECT_KEY != '':
        AIRBRAKE = dict(
            project_id=AIRBRAKE_PROJECT,
            project_key=AIRBRAKE_PROJECT_KEY,
        )
        MIDDLEWARE.append('pybrake.django.AirbrakeMiddleware')
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'airbrake': {
                    'level': 'ERROR',
                    'class': 'pybrake.LoggingHandler',
                },
            },
            'loggers': {
                'app': {
                    'handlers': ['airbrake'],
                    'level': 'ERROR',
                    'propagate': True,
                },
            },
        }
else:
    INSTALLED_APPS += ['behave_django']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
LOCALE_PATHS = (os.path.join(SITE_ROOT, 'locale'), )
LANGUAGE_CODE = 'en-gb'
LANGUAGES = (
    ('en-gb', 'English'),
    ('fr-fr', 'French')
)

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
