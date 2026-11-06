# Purpose: tests for the environment validation rules in config/env.py.
import pytest
from django.core.exceptions import ImproperlyConfigured

from config import env

# Obviously fake values; never use real secrets in tests.
FAKE_VALID_KEY = "fake-test-key-" + "abcdefghij" * 4
FAKE_HOSTS = "shop.example.test, www.shop.example.test"
FAKE_PASSWORD = "fake-db-password-12345"
FAKE_DATABASE_URL = f"postgresql://fake_user:{FAKE_PASSWORD}@localhost:5432/fake_db"


def development_environ(**overrides: str) -> dict[str, str]:
    values = {"APP_ENV": "development", "DATABASE_URL": FAKE_DATABASE_URL}
    values.update(overrides)
    return values


def production_environ(**overrides: str) -> dict[str, str]:
    values = {
        "APP_ENV": "production",
        "SECRET_KEY": FAKE_VALID_KEY,
        "ALLOWED_HOSTS": FAKE_HOSTS,
        "DATABASE_URL": FAKE_DATABASE_URL,
    }
    values.update(overrides)
    return values


def test_development_works_with_only_a_database_url_set() -> None:
    config = env.read_config(development_environ())

    assert config.is_development
    assert config.secret_key == env.DEVELOPMENT_ONLY_SECRET_KEY
    assert config.allowed_hosts == env.DEFAULT_DEVELOPMENT_ALLOWED_HOSTS


def test_development_uses_custom_hosts_and_key_when_given() -> None:
    config = env.read_config(
        development_environ(SECRET_KEY="my-local-key", ALLOWED_HOSTS="dev.test")
    )

    assert config.secret_key == "my-local-key"
    assert config.allowed_hosts == ("dev.test",)


@pytest.mark.parametrize("environ", [{}, {"APP_ENV": ""}, {"APP_ENV": "   "}])
def test_app_env_is_required(environ: dict[str, str]) -> None:
    with pytest.raises(ImproperlyConfigured, match="APP_ENV is required"):
        env.read_config(environ)


@pytest.mark.parametrize("value", ["developement", "prod", "Production", "staging"])
def test_invalid_app_env_is_rejected(value: str) -> None:
    with pytest.raises(ImproperlyConfigured, match="APP_ENV must be"):
        env.read_config({"APP_ENV": value})


def test_invalid_app_env_value_is_not_printed() -> None:
    # A distinctive value, so it cannot collide with words in the message itself.
    fake_value = "fake-env-value-12345"

    with pytest.raises(ImproperlyConfigured) as error:
        env.read_config({"APP_ENV": fake_value})

    assert fake_value not in str(error.value)


def test_valid_production_config_is_accepted_with_debug_off() -> None:
    config = env.read_config(production_environ())

    assert not config.is_development
    assert config.secret_key == FAKE_VALID_KEY
    assert config.allowed_hosts == ("shop.example.test", "www.shop.example.test")


@pytest.mark.parametrize(
    "bad_key",
    [
        "",
        env.DEVELOPMENT_ONLY_SECRET_KEY,
        "django-insecure-" + "x1y2z3" * 10,
        "short-fake-key",
        "ab" * 40,
    ],
)
def test_production_rejects_missing_placeholder_short_or_repetitive_secret_key(
    bad_key: str,
) -> None:
    with pytest.raises(ImproperlyConfigured, match="SECRET_KEY") as error:
        env.read_config(production_environ(SECRET_KEY=bad_key))

    if bad_key:
        assert bad_key not in str(error.value)


@pytest.mark.parametrize("bad_hosts", ["", "  ,  ", "*", "shop.example.test,*"])
def test_production_rejects_empty_or_wildcard_allowed_hosts(bad_hosts: str) -> None:
    with pytest.raises(ImproperlyConfigured, match="ALLOWED_HOSTS"):
        env.read_config(production_environ(ALLOWED_HOSTS=bad_hosts))


def test_database_url_is_parsed_into_connection_settings() -> None:
    url = "postgres://shop_user:p%40ss%2Fword@db.example.test:6543/shop_db?sslmode=require"

    database = env.read_config(production_environ(DATABASE_URL=url)).database

    assert database.user == "shop_user"
    assert database.password == "p@ss/word"  # percent-encoded characters are decoded
    assert database.host == "db.example.test"
    assert database.port == 6543
    assert database.name == "shop_db"
    assert database.ssl_mode == "require"


def test_database_url_defaults_to_standard_port_and_django_settings_shape() -> None:
    database = env.read_config(development_environ()).database
    django_settings = database.django_settings()

    assert database.port == env.DEFAULT_DATABASE_PORT
    assert django_settings["ENGINE"] == "django.db.backends.postgresql"
    assert django_settings["NAME"] == "fake_db"
    assert django_settings["PORT"] == "5432"
    assert django_settings["OPTIONS"] == {}


def test_database_url_is_required_in_every_mode() -> None:
    for environ in (development_environ(), production_environ()):
        del environ["DATABASE_URL"]
        with pytest.raises(ImproperlyConfigured, match="DATABASE_URL is required"):
            env.read_config(environ)


@pytest.mark.parametrize(
    "bad_url",
    [
        "mysql://u:fake-pw-1@localhost/db",  # wrong database type
        "postgresql://u:fake-pw-1@/db",  # no host
        "postgresql://:fake-pw-1@localhost/db",  # no user
        "postgresql://u:fake-pw-1@localhost",  # no database name
        "postgresql://u:fake-pw-1@localhost/a/b",  # more than one path part
        "postgresql://u:fake-pw-1@localhost:notaport/db",  # port is not a number
        "postgresql://u:fake-pw-1@localhost/db?connect_timeout=5",  # unsupported option
        "postgresql://u:fake-pw-1@localhost/db?sslmode=bogus",  # unknown SSL mode
    ],
)
def test_bad_database_urls_are_rejected_without_printing_the_url(bad_url: str) -> None:
    with pytest.raises(ImproperlyConfigured, match="DATABASE_URL|sslmode") as error:
        env.read_config(development_environ(DATABASE_URL=bad_url))

    assert "fake-pw-1" not in str(error.value)
    assert bad_url not in str(error.value)


def test_production_requires_a_database_password() -> None:
    url = "postgresql://shop_user@localhost:5432/shop_db"

    with pytest.raises(ImproperlyConfigured, match="password in production"):
        env.read_config(production_environ(DATABASE_URL=url))

    assert env.read_config(development_environ(DATABASE_URL=url)).database.password == ""


@pytest.mark.parametrize("host", ["localhost", "127.0.0.1", "[::1]"])
def test_production_allows_unencrypted_connection_to_a_local_database(host: str) -> None:
    url = f"postgresql://shop_user:fake-pw-2@{host}:5432/shop_db"

    assert env.read_config(production_environ(DATABASE_URL=url)).database.ssl_mode is None


@pytest.mark.parametrize("query", ["", "?sslmode=disable", "?sslmode=prefer"])
def test_production_rejects_unencrypted_connection_to_a_remote_database(query: str) -> None:
    url = f"postgresql://shop_user:fake-pw-3@db.example.test:5432/shop_db{query}"

    with pytest.raises(ImproperlyConfigured, match="another host") as error:
        env.read_config(production_environ(DATABASE_URL=url))

    assert "fake-pw-3" not in str(error.value)


@pytest.mark.parametrize("mode", ["require", "verify-ca", "verify-full"])
def test_production_accepts_remote_database_with_secure_ssl_mode(mode: str) -> None:
    url = f"postgresql://shop_user:fake-pw-4@db.example.test:5432/shop_db?sslmode={mode}"

    database = env.read_config(production_environ(DATABASE_URL=url)).database

    assert database.django_settings()["OPTIONS"] == {"sslmode": mode}


def test_printing_the_config_never_shows_the_database_password() -> None:
    config = env.read_config(development_environ())

    assert FAKE_PASSWORD not in repr(config)
    assert FAKE_PASSWORD not in str(config)
