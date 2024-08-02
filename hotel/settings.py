"""
Django settings for hotel project.

Generated by 'django-admin startproject' using Django 5.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-y0tjvd@thr%0jb6uuoqxt4i=yl-^tp$(nfupx3d+z(3$a+w(ky"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "hotelsite-7y00.onrender.com"]


# Application definition

INSTALLED_APPS = [
    "service.apps.ServiceConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_celery_beat",
    "cart.apps.CartConfig",
    "django_daraja",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hotel.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "service.context_processors.hotel_details",
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "hotel.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 4},
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"

USE_I18N = True

USE_TZ = True


# Set the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "service/static/service",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Define the media directory where uploaded files will be stored
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Define the URL for serving media files during development
MEDIA_URL = "/media/"

LOGIN_REDIRECT_URL = "service:home"
LOGOUT_REDIRECT_URL = "service:home"
LOGIN_URL = "service:login"
LOGOUT_URL = "service:logout"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "adamsquare64@gmail.com"
EMAIL_HOST_PASSWORD = "vyjk wktm vmli ljif"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_DEBUG = True


# settings.py

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "Africa/Nairobi"


CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CART_SESSION_ID = "cart"

MPESA_ENVIRONMENT = "sandbox"

MPESA_CONSUMER_KEY = "WHBx5igrXKq4jQhooZgg4YJkzGxn87ZUMr63teJ9oPS0h0Ay"
MPESA_CONSUMER_SECRET = (
    "t6FiOuoXYDkaj6GmKJN14WiJW3aJBaG3H2iBSvKHQIqArqgAQL9v22C0JAsIAyLw"
)

MPESA_SHORT_CODE = "174379"
MPESA_EXPRESS_SHORTCODE = "174379"

MPESA_SHORTCODE_TYPE = "till_number"

MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

MPESA_INITIATOR_USERNAME = "testapi"

MPESA_INITIATOR_SECURITY_CREDENTIALS = "Safaricom999!*!"

MPESA_CALLBACK_URL = "https://2d68-41-204-187-5.ngrok-free.app"


X_FRAME_OPTIONS = "SAMEORIGIN"
