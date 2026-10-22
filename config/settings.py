# Purpose: project settings. Environment handling is in config/env.py (T-011);
# T-012 will add the PostgreSQL database.
import os
from pathlib import Path

from config.env import read_config

BASE_DIR = Path(__file__).resolve().parent.parent

# Validated at import time, so a bad configuration stops the app at startup with a clear
# message (see config/env.py). Debug is on only when APP_ENV is explicitly "development".
_config = read_config(os.environ)

DEBUG = _config.is_development
SECRET_KEY = _config.secret_key
ALLOWED_HOSTS = list(_config.allowed_hosts)

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "storefront",
]

# No sessions, admin or login yet: those need the database (T-012) and later tasks.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Intentionally empty: the skeleton has no database. T-012 configures PostgreSQL.
DATABASES: dict[str, dict[str, str]] = {}

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
