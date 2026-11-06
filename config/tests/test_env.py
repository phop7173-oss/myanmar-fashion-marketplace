# Purpose: tests for the environment validation rules in config/env.py.
import pytest
from django.core.exceptions import ImproperlyConfigured

from config import env

# Obviously fake values; never use real secrets in tests.
FAKE_VALID_KEY = "fake-test-key-" + "abcdefghij" * 4
FAKE_HOSTS = "shop.example.test, www.shop.example.test"


def production_environ(**overrides: str) -> dict[str, str]:
    values = {
        "APP_ENV": "production",
        "SECRET_KEY": FAKE_VALID_KEY,
        "ALLOWED_HOSTS": FAKE_HOSTS,
    }
    values.update(overrides)
    return values


def test_development_works_with_nothing_else_set() -> None:
    config = env.read_config({"APP_ENV": "development"})

    assert config.is_development
    assert config.secret_key == env.DEVELOPMENT_ONLY_SECRET_KEY
    assert config.allowed_hosts == env.DEFAULT_DEVELOPMENT_ALLOWED_HOSTS


def test_development_uses_custom_hosts_and_key_when_given() -> None:
    config = env.read_config(
        {"APP_ENV": "development", "SECRET_KEY": "my-local-key", "ALLOWED_HOSTS": "dev.test"}
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
