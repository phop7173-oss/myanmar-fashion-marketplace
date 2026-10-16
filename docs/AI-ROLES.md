# AI and Human Roles

## Human owner
Sets priorities, resolves business decisions, approves scope and releases, and accepts results.

## Architect
Inspects the repository, defines boundaries and contracts, identifies failure modes, and proposes small implementation tasks.

## Implementer
Changes only the approved scope, makes focused edits, adds tests, and updates affected documentation.

## Reviewer
Checks correctness, authorization, data leakage, race conditions, transaction safety, accessibility, and maintainability.

## Tester
Tests success, invalid input, denied access, stale state, duplicate requests, and integration failures.

## Release manager
Verifies checks, migrations, configuration, backups, recovery, and rollback. Production release requires human approval.

## Workflow
1. Owner prioritizes.
2. Architect defines task and acceptance criteria.
3. Implementer inspects and changes code.
4. Tester runs checks and records evidence.
5. Reviewer examines the diff.
6. Owner accepts or requests changes.
7. Update task status.

Every AI implementation report must list files changed, assumptions, commands actually run, observed results, risks, and the next proposed task. Never claim unobserved tests passed.
