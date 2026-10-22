#!/usr/bin/env python
# Purpose: Django's command-line entry point (runserver, test helpers, later migrations).
import os
import sys


def main() -> None:
    """Run a Django management command from the command line."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
