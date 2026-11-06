# Current Task

**Task:** T-012 Local database and migration baseline ([card](cards/01-foundation.md#t-012-local-database-and-migration-baseline))
**Status:** Ready for review (built 2026-10-23; **not yet run or accepted by the Owner**)

## What was built
`DATABASE_URL` (PostgreSQL) is read and validated in `config/env.py` with the same safety rules as T-011: required in every mode, parse errors never print the URL, the password is hidden from `repr()`, and production refuses an unencrypted connection to a database on another host. `psycopg` 3 is added to the lockfile. One empty baseline migration exists (`storefront/migrations/0001_initial.py`). `pytest` runs against a real PostgreSQL, in its own throwaway `test_...` database.

## What the Owner must do to close T-012
- [ ] Set up the local database following [README](../README.md#local-database-postgresql).
- [ ] Run `ruff format --check .`, `ruff check .`, `pytest`, `pytest --create-db`, and `python manage.py migrate` twice (the second run must do nothing). Paste any failure.
- [ ] Then mark T-012 `Done` in [ROADMAP.md](ROADMAP.md).

## Other open items
- T-002 (hosting research) is Ready for review; ADR-0007 is Proposed and needs your checks A-D.

## Next task
T-013 Continuous integration and quality gates (needs T-012 Done). It reaches Gate 1.

## Rules
- Only one task is current at a time. Change this file only when the Owner starts a different task.
- Do not claim tests, commits or deployments succeeded unless verified in the session that did the work.
