# Purpose: read and validate environment variables for the settings. Errors name the
# variable and the rule, and never print a value (SECURITY: Secrets).
from collections.abc import Mapping
from dataclasses import dataclass

from django.core.exceptions import ImproperlyConfigured

APP_ENV_DEVELOPMENT = "development"
APP_ENV_PRODUCTION = "production"
VALID_APP_ENVS = (APP_ENV_DEVELOPMENT, APP_ENV_PRODUCTION)

ENV_APP_ENV = "APP_ENV"
ENV_SECRET_KEY = "SECRET_KEY"  # noqa: S105 (this is a variable NAME, not a secret)
ENV_ALLOWED_HOSTS = "ALLOWED_HOSTS"
# Every variable this module reads; a test checks each one is listed in .env.example.
ENV_VARIABLE_NAMES = (ENV_APP_ENV, ENV_SECRET_KEY, ENV_ALLOWED_HOSTS)

# Local-only placeholder so `runserver` works with nothing set. It is NOT a secret and is
# rejected in production.
DEVELOPMENT_ONLY_SECRET_KEY = "development-only-not-a-secret"  # noqa: S105
DEFAULT_DEVELOPMENT_ALLOWED_HOSTS = ("localhost", "127.0.0.1")

# Same bar as Django's own deployment check (security.W009).
MIN_SECRET_KEY_LENGTH = 50
MIN_SECRET_KEY_UNIQUE_CHARACTERS = 5
DJANGO_INSECURE_KEY_PREFIX = "django-insecure-"


@dataclass(frozen=True)
class AppConfig:
    """Validated configuration values used by the Django settings."""

    app_env: str
    secret_key: str
    allowed_hosts: tuple[str, ...]

    @property
    def is_development(self) -> bool:
        return self.app_env == APP_ENV_DEVELOPMENT


def read_config(environ: Mapping[str, str]) -> AppConfig:
    """Validate environment variables and return the configuration.

    Anyone may call it. Raises ImproperlyConfigured when a required variable is missing or
    invalid. Guarantee: a production configuration never has debug on, a weak or placeholder
    secret key, or an empty or wildcard host list. Error messages never contain values.
    """
    app_env = _read_app_env(environ)
    is_development = app_env == APP_ENV_DEVELOPMENT
    return AppConfig(
        app_env=app_env,
        secret_key=_read_secret_key(environ, is_development),
        allowed_hosts=_read_allowed_hosts(environ, is_development),
    )


def _read_app_env(environ: Mapping[str, str]) -> str:
    # No silent default: a typo must not quietly become the wrong mode.
    value = environ.get(ENV_APP_ENV, "").strip()
    if not value:
        raise ImproperlyConfigured(
            f"{ENV_APP_ENV} is required. Set it to '{APP_ENV_DEVELOPMENT}' or "
            f"'{APP_ENV_PRODUCTION}'."
        )
    if value not in VALID_APP_ENVS:
        raise ImproperlyConfigured(
            f"{ENV_APP_ENV} must be '{APP_ENV_DEVELOPMENT}' or '{APP_ENV_PRODUCTION}'."
        )
    return value


def _read_secret_key(environ: Mapping[str, str], is_development: bool) -> str:
    value = environ.get(ENV_SECRET_KEY, "")
    if is_development:
        return value or DEVELOPMENT_ONLY_SECRET_KEY
    if not value:
        raise ImproperlyConfigured(f"{ENV_SECRET_KEY} is required in production.")
    if value == DEVELOPMENT_ONLY_SECRET_KEY or value.startswith(DJANGO_INSECURE_KEY_PREFIX):
        raise ImproperlyConfigured(
            f"{ENV_SECRET_KEY} must not be a development or placeholder key in production."
        )
    if len(value) < MIN_SECRET_KEY_LENGTH:
        raise ImproperlyConfigured(
            f"{ENV_SECRET_KEY} must be at least {MIN_SECRET_KEY_LENGTH} characters long."
        )
    if len(set(value)) < MIN_SECRET_KEY_UNIQUE_CHARACTERS:
        raise ImproperlyConfigured(
            f"{ENV_SECRET_KEY} must contain at least {MIN_SECRET_KEY_UNIQUE_CHARACTERS} "
            "different characters."
        )
    return value


def _read_allowed_hosts(environ: Mapping[str, str], is_development: bool) -> tuple[str, ...]:
    raw_value = environ.get(ENV_ALLOWED_HOSTS, "")
    hosts = tuple(host.strip() for host in raw_value.split(",") if host.strip())
    if is_development:
        return hosts or DEFAULT_DEVELOPMENT_ALLOWED_HOSTS
    if not hosts:
        raise ImproperlyConfigured(
            f"{ENV_ALLOWED_HOSTS} is required in production (comma-separated host names)."
        )
    if "*" in hosts:
        raise ImproperlyConfigured(f"{ENV_ALLOWED_HOSTS} must not contain '*' in production.")
    return hosts
