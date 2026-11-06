# Purpose: AC-SEC-01 foundations: local .env files stay out of Git, and .env.example holds
# variable names only (no secret values).
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from config.env import ENV_VARIABLE_NAMES

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
SECRET_NAME_PARTS = ("KEY", "TOKEN", "SECRET", "PASSWORD")
VARIABLE_LINE = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def example_variables() -> dict[str, str]:
    variables = {}
    for line in ENV_EXAMPLE.read_text().splitlines():
        match = VARIABLE_LINE.match(line.strip())
        if match:
            variables[match.group(1)] = match.group(2)
    return variables


def test_dotenv_file_is_ignored_by_git() -> None:
    result = run_git("check-ignore", "-q", ".env")

    assert result.returncode == 0, ".env must be listed in .gitignore"


def test_no_dotenv_file_is_tracked_by_git() -> None:
    tracked = run_git("ls-files").stdout.splitlines()
    tracked_env_files = [
        path
        for path in tracked
        if Path(path).name.startswith(".env") and Path(path).name != ".env.example"
    ]

    assert tracked_env_files == []


def test_env_example_lists_every_variable_the_app_reads() -> None:
    assert set(ENV_VARIABLE_NAMES) <= set(example_variables())


def test_env_example_database_url_has_only_a_placeholder_password() -> None:
    # The URL holds a password, so its value must show the format with a placeholder only.
    password = urlsplit(example_variables()["DATABASE_URL"]).password

    assert password in (None, "", "CHANGE_ME")


def test_env_example_holds_no_secret_values() -> None:
    secret_variables = {
        name: value
        for name, value in example_variables().items()
        if any(part in name for part in SECRET_NAME_PARTS)
    }

    assert secret_variables, "expected at least SECRET_KEY to be listed"
    assert all(value == "" for value in secret_variables.values())
