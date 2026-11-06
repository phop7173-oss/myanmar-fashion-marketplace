# Purpose: proves the real app refuses to start with a bad configuration, and that the
# failure message names the problem without printing a secret value.
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FAKE_SECRET_VALUE = "fake-short-secret-value-for-test"
FAKE_VALID_KEY = "fake-test-key-" + "abcdefghij" * 4


def import_settings(environ: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """Import the real settings in a fresh process with only the given variables set."""
    clean_environ = {"PATH": os.environ.get("PATH", ""), **environ}
    return subprocess.run(
        [sys.executable, "-c", "import config.settings"],
        cwd=PROJECT_ROOT,
        env=clean_environ,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_startup_fails_when_app_env_is_missing() -> None:
    result = import_settings({})

    assert result.returncode != 0
    assert "ImproperlyConfigured" in result.stderr
    assert "APP_ENV" in result.stderr


def test_startup_fails_in_production_without_secret_key() -> None:
    result = import_settings({"APP_ENV": "production", "ALLOWED_HOSTS": "shop.example.test"})

    assert result.returncode != 0
    assert "SECRET_KEY is required" in result.stderr


def test_startup_failure_does_not_print_the_secret_value() -> None:
    result = import_settings(
        {
            "APP_ENV": "production",
            "SECRET_KEY": FAKE_SECRET_VALUE,
            "ALLOWED_HOSTS": "shop.example.test",
        }
    )

    assert result.returncode != 0
    assert "SECRET_KEY" in result.stderr
    assert FAKE_SECRET_VALUE not in result.stderr
    assert FAKE_SECRET_VALUE not in result.stdout


def test_startup_succeeds_with_a_valid_production_configuration() -> None:
    result = import_settings(
        {
            "APP_ENV": "production",
            "SECRET_KEY": FAKE_VALID_KEY,
            "ALLOWED_HOSTS": "shop.example.test",
        }
    )

    assert result.returncode == 0, result.stderr


def test_startup_succeeds_in_development_with_nothing_else_set() -> None:
    result = import_settings({"APP_ENV": "development"})

    assert result.returncode == 0, result.stderr
