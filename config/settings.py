# Purpose: project settings for the T-010 skeleton. T-011 will extend env handling and
# startup validation; T-012 will add the PostgreSQL database.
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Local-only placeholder so tests and `runserver` work. It is NOT a secret and must never
# be used in production; T-011 will make a real SECRET_KEY mandatory outside development.
DEVELOPMENT_ONLY_SECRET_KEY = "development-only-not-a-secret"  # noqa: S105

APP_ENV = os.environ.get("APP_ENV", "production")
IS_DEVELOPMENT = APP_ENV == "development"

# Debug is off unless APP_ENV is explicitly "development" (safe default).
DEBUG = IS_DEVELOPMENT
SECRET_KEY = os.environ.get("SECRET_KEY", DEVELOPMENT_ONLY_SECRET_KEY)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

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
