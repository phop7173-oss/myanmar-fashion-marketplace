# Current Task

**Task:** T-001 Resolve blocking decisions ([card](cards/01-foundation.md#t-001-resolve-blocking-decisions))
**Status:** Ready for review (decisions recorded; **not yet marked Done by the Owner**)

## What was decided (2026-10-20)
- D-01 / D-08 (ADR-0005): Django baseline; Telegram webhook mode. **D-02 hosting remains open.**
- D-03 (ADR-0006): all seven order-model defaults accepted.
- D-06, D-07: defaults accepted.

## What the Owner must do to close T-001
- [ ] Review the diff of ADR-0005, ADR-0006 and the decision register.
- [ ] Mark T-000 and T-001 `Done` in [ROADMAP.md](ROADMAP.md) and commit.

## Next task
**T-002 Verify hosting and free-tier facts** (research, no code). T-010 (scaffold) may start once T-001 is Done and the Owner approves its plan; it does not depend on T-002.

## Rules
- Only one task is current at a time. Change this file only when the Owner starts a different task.
- No application code exists. Do not claim tests, commits or deployments succeeded unless verified in the session that did the work.
