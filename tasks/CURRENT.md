# Current Task

**Task:** T-002 Verify hosting and free-tier facts ([card](cards/01-foundation.md#t-002-verify-hosting-and-free-tier-facts))
**Status:** Ready for review (research done 2026-10-20; **not yet accepted by the Owner**)

## Result
- U1-U12 table in [TECH-STACK](../docs/TECH-STACK.md) updated with sources and status; several items remain UNVERIFIED and need Owner-side checks.
- New ADR [0007-hosting](../docs/decisions/0007-hosting.md) is **Proposed**. No candidate was verified to meet every requirement.

## What the Owner must do to close T-002
- [ ] Read ADR-0007 and run the Owner-side checks A-D (signup from Myanmar, card, Telegram on sellers' phones, Burmese text).
- [ ] Accept, change or reject ADR-0007 (decides D-02). Mark T-002 `Done` in [ROADMAP.md](ROADMAP.md).

## Earlier task
T-001 (blocking decisions) is Ready for review; the Owner marks T-000 and T-001 Done when satisfied.

## Next task
T-010 Project skeleton (needs T-001 Done and an Owner-approved plan; does not depend on T-002).

## Rules
- Only one task is current at a time. Change this file only when the Owner starts a different task.
- No application code exists. Do not claim tests, commits or deployments succeeded unless verified in the session that did the work.
