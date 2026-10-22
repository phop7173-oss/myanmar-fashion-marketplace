# Current Task

**Task:** T-010 Project skeleton and tooling ([card](cards/01-foundation.md#t-010-project-skeleton-and-tooling))
**Status:** Ready for review (built 2026-10-23; **not yet run or accepted by the Owner**)

## What was built
Minimal Django 5.2 LTS project: `config/`, one `storefront` app with a placeholder home page, one trivial test, one small CSS file, pinned lockfiles, ruff and pytest configuration. No database, models, login or CI (non-goals).

## What the Owner must do to close T-010
- [ ] Follow the setup in [README](../README.md#development-environment) on your own machine.
- [ ] Run `ruff format --check .`, `ruff check .` and `pytest`; open the home page with `python manage.py runserver`.
- [ ] Report anything that fails (paste the exact error). Then mark T-010 `Done` in [ROADMAP.md](ROADMAP.md).

## Other open items
- T-002 (hosting research) is Ready for review; ADR-0007 is Proposed and needs your checks A-D.

## Next task
T-011 Configuration and secrets handling (needs T-010 Done).

## Rules
- Only one task is current at a time. Change this file only when the Owner starts a different task.
- Do not claim tests, commits or deployments succeeded unless verified in the session that did the work.
