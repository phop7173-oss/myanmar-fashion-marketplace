# Current Task

**Task:** T-011 Configuration and secrets handling ([card](cards/01-foundation.md#t-011-configuration-and-secrets-handling))
**Status:** Ready for review (built 2026-10-23; **not yet run or accepted by the Owner**)

## What was built
Settings now come from environment variables, validated at startup in `config/env.py`. Missing or unsafe values stop the app with a message that names the variable and never prints its value. `.env.example` has the final names. Tests cover the rules, a real startup in a fresh process, and that `.env` stays out of Git.

## What the Owner must do to close T-011
- [ ] Follow the commands in the task report (run `ruff format --check .`, `ruff check .`, `pytest` and the manual checks).
- [ ] Report anything that fails (paste the exact error). Then mark T-011 `Done` in [ROADMAP.md](ROADMAP.md).

## Other open items
- T-002 (hosting research) is Ready for review; ADR-0007 is Proposed and needs your checks A-D.

## Next task
T-012 Local database and migration baseline (needs T-011 Done).

## Rules
- Only one task is current at a time. Change this file only when the Owner starts a different task.
- Do not claim tests, commits or deployments succeeded unless verified in the session that did the work.
