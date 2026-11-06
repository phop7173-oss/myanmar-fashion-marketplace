# Purpose: read and validate environment variables for the settings. Errors name the
# variable and the rule, and never print a value (SECURITY: Secrets).
from collections.abc import Mapping
from dataclasses import dataclass, field
from urllib.parse import parse_qsl, unquote, urlsplit

from django.core.exceptions import ImproperlyConfigured

APP_ENV_DEVELOPMENT = "development"
APP_ENV_PRODUCTION = "production"
VALID_APP_ENVS = (APP_ENV_DEVELOPMENT, APP_ENV_PRODUCTION)

ENV_APP_ENV = "APP_ENV"
ENV_SECRET_KEY = "SECRET_KEY"  # noqa: S105 (this is a variable NAME, not a secret)
ENV_ALLOWED_HOSTS = "ALLOWED_HOSTS"
ENV_DATABASE_URL = "DATABASE_URL"
# Every variable this module reads; a test checks each one is listed in .env.example.
ENV_VARIABLE_NAMES = (ENV_APP_ENV, ENV_SECRET_KEY, ENV_ALLOWED_HOSTS, ENV_DATABASE_URL)

# Local-only placeholder so `runserver` works with nothing set. It is NOT a secret and is
# rejected in production.
DEVELOPMENT_ONLY_SECRET_KEY = "development-only-not-a-secret"  # noqa: S105
DEFAULT_DEVELOPMENT_ALLOWED_HOSTS = ("localhost", "127.0.0.1")

# Same bar as Django's own deployment check (security.W009).
MIN_SECRET_KEY_LENGTH = 50
MIN_SECRET_KEY_UNIQUE_CHARACTERS = 5
DJANGO_INSECURE_KEY_PREFIX = "django-insecure-"

DATABASE_URL_SCHEMES = ("postgresql", "postgres")
DEFAULT_DATABASE_PORT = 5432
# A database on the same machine needs no encryption on the wire.
LOCAL_DATABASE_HOSTS = ("localhost", "127.0.0.1", "::1")
SECURE_SSL_MODES = ("require", "verify-ca", "verify-full")
VALID_SSL_MODES = ("disable", "allow", "prefer", *SECURE_SSL_MODES)
SSL_MODE_OPTION = "sslmode"


@dataclass(frozen=True)
class DatabaseConfig:
    """PostgreSQL connection settings parsed from DATABASE_URL.

    The password is excluded from repr() so printing or logging this object cannot leak it.
    """

    name: str
    user: str
    host: str
    port: int
    password: str = field(repr=False)
    ssl_mode: str | None = None

    def django_settings(self) -> dict[str, object]:
        """Return this connection as a Django DATABASES entry."""
        options = {SSL_MODE_OPTION: self.ssl_mode} if self.ssl_mode else {}
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": self.name,
            "USER": self.user,
            "PASSWORD": self.password,
            "HOST": self.host,
            "PORT": str(self.port),
            "OPTIONS": options,
        }


@dataclass(frozen=True)
class AppConfig:
    """Validated configuration values used by the Django settings."""

    app_env: str
    secret_key: str
    allowed_hosts: tuple[str, ...]
    database: DatabaseConfig

    @property
    def is_development(self) -> bool:
        return self.app_env == APP_ENV_DEVELOPMENT


def read_config(environ: Mapping[str, str]) -> AppConfig:
    """Validate environment variables and return the configuration.

    Anyone may call it. Raises ImproperlyConfigured when a required variable is missing or
    invalid. Guarantee: a production configuration never has debug on, a weak or placeholder
    secret key, an empty or wildcard host list, or an unencrypted connection to a remote
    database. Error messages never contain values (the database URL holds a password).
    """
    app_env = _read_app_env(environ)
    is_development = app_env == APP_ENV_DEVELOPMENT
    return AppConfig(
        app_env=app_env,
        secret_key=_read_secret_key(environ, is_development),
        allowed_hosts=_read_allowed_hosts(environ, is_development),
        database=_read_database(environ, is_development),
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


def _read_database(environ: Mapping[str, str], is_development: bool) -> DatabaseConfig:
    raw_url = environ.get(ENV_DATABASE_URL, "").strip()
    if not raw_url:
        raise ImproperlyConfigured(
            f"{ENV_DATABASE_URL} is required, in the form "
            "postgresql://USER:PASSWORD@HOST:5432/DATABASE_NAME"
        )
    try:
        parts = urlsplit(raw_url)
        port = parts.port or DEFAULT_DATABASE_PORT
    except ValueError:
        raise ImproperlyConfigured(
            f"{ENV_DATABASE_URL} is not a valid URL (check the port number and that special "
            "characters in the password are percent-encoded)."
        ) from None
    if parts.scheme not in DATABASE_URL_SCHEMES:
        raise ImproperlyConfigured(f"{ENV_DATABASE_URL} must start with postgresql://")
    host = parts.hostname or ""
    if not host:
        raise ImproperlyConfigured(f"{ENV_DATABASE_URL} must include a host name.")
    user = unquote(parts.username or "")
    if not user:
        raise ImproperlyConfigured(f"{ENV_DATABASE_URL} must include a user name.")
    password = unquote(parts.password or "")
    if not password and not is_development:
        raise ImproperlyConfigured(f"{ENV_DATABASE_URL} must include a password in production.")
    name = unquote(parts.path.removeprefix("/"))
    if not name or "/" in name:
        raise ImproperlyConfigured(f"{ENV_DATABASE_URL} must include one database name.")
    ssl_mode = _read_ssl_mode(parts.query)
    if not is_development and host not in LOCAL_DATABASE_HOSTS and ssl_mode not in SECURE_SSL_MODES:
        raise ImproperlyConfigured(
            f"In production, a database on another host needs {SSL_MODE_OPTION}=require "
            f"(or stronger) in {ENV_DATABASE_URL}."
        )
    return DatabaseConfig(
        name=name, user=user, host=host, port=port, password=password, ssl_mode=ssl_mode
    )


def _read_ssl_mode(query: str) -> str | None:
    ssl_mode = None
    for option, value in parse_qsl(query, keep_blank_values=True):
        if option != SSL_MODE_OPTION:
            raise ImproperlyConfigured(
                f"{ENV_DATABASE_URL} has an unsupported option; only {SSL_MODE_OPTION} is allowed."
            )
        if value not in VALID_SSL_MODES:
            raise ImproperlyConfigured(
                f"{SSL_MODE_OPTION} in {ENV_DATABASE_URL} must be one of: "
                f"{', '.join(VALID_SSL_MODES)}."
            )
        ssl_mode = value
    return ssl_mode
