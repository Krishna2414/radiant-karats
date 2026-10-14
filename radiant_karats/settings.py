"""
Django settings for the Radiant Karats ring request app.

Secret values are read from environment variables. Locally they come
from env.py, which Git ignores. On Heroku they are set as Config Vars.
"""
import os
import sys
from pathlib import Path

import cloudinary
import dj_database_url
from django.contrib.messages import constants as message_constants

if os.path.isfile("env.py"):
    import env  # noqa: F401  Sets the local environment variables.

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

# DEBUG is only on when the DEBUG variable is exactly "True", so the
# deployed site runs with DEBUG off unless it is switched on on purpose.
DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = [
    ".herokuapp.com",
    ".codeinstitute-ide.net",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.herokuapp.com",
    "https://*.codeinstitute-ide.net",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "crispy_forms",
    "crispy_bootstrap5",
    "cloudinary",
    "designs",
    "ring_requests",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "radiant_karats.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "radiant_karats.wsgi.application"

# PostgreSQL comes from DATABASE_URL. Tests, and local setups without
# DATABASE_URL, use SQLite instead, because the Code Institute database
# doesn't let Django create the separate database it needs for tests.
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and "test" not in sys.argv:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Accounts (django-allauth): sign up with a username and email address,
# log in with the username. There's no email confirmation step, so
# anyone can register and use the site straight away.
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Cloudinary reads CLOUDINARY_URL from the environment. Serving images
# over https stops browsers blocking them on the deployed site.
cloudinary.config(secure=True)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Bootstrap calls its red alert "danger"; Django calls it "error".
MESSAGE_TAGS = {message_constants.ERROR: "danger"}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"