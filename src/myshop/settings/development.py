from .base import *


ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}
