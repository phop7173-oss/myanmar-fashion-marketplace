# Purpose: proves the app talks to a real PostgreSQL database and that migrations work.
# pytest-django builds a separate "test_..." database by running every migration from
# scratch, so your development data is never touched (run `pytest --create-db` to force it).
import pytest
from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

pytestmark = pytest.mark.django_db


def test_connection_is_a_real_postgresql_database() -> None:
    assert connection.vendor == "postgresql"


def test_tests_use_a_separate_test_database_not_the_development_one() -> None:
    assert connection.settings_dict["NAME"].startswith("test_")


def test_database_answers_a_simple_query() -> None:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

        assert cursor.fetchone() == (1,)


def test_initial_migration_was_applied_from_scratch() -> None:
    applied = MigrationRecorder.Migration.objects.filter(
        app="storefront", name="0001_initial"
    ).exists()

    assert applied


def test_no_model_change_is_missing_a_migration() -> None:
    # Raises SystemExit if Django finds model changes that have no migration yet.
    call_command("makemigrations", "--check", "--dry-run")
