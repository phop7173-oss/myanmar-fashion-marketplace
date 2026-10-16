# AI Engineering Rules

## Before coding
Read docs/PROJECT.md, docs/ARCHITECTURE.md, relevant technical contracts, and tasks/CURRENT.md.

## Mandatory rules
- Inspect existing files before editing.
- Implement only the approved task, using small, focused changes.
- Never overwrite unrelated working code.
- Never invent existing files, APIs, database tables, or configuration.
- Never commit secrets, API tokens, bot tokens, or real customer data.
- Treat client input as untrusted and validate it at runtime.
- Enforce authorization on the server for every protected operation.
- Never trust a submitted seller_id as proof of identity.
- Sellers may manage only their own approved offers.
- Calculate order prices and totals on the server.
- Preserve purchase-time order item snapshots.
- Use database constraints, transactions, and idempotency where required.
- Add tests for behavior changes and report only tests actually run.
- Record significant architecture changes in docs/decisions/.
- Do not add payments, built-in chat, or a seller dashboard without approval.
- Use product images only with permission or an authorized source.

## Implementation workflow
1. Inspect the repository.
2. Confirm task scope and acceptance criteria.
3. Implement one small feature.
4. Run relevant tests and checks.
5. Review security and changed files.
6. Update documentation and task status.
7. Report results, limitations, and the next task.

Markdown rules guide the AI; application code, database constraints, and tests must enforce security.
