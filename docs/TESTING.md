# Testing Strategy

**Authoritative for:** how we test and what counts as evidence. What must be true: [ACCEPTANCE-TESTS](ACCEPTANCE-TESTS.md). Tests are the enforcement mechanism for security and data rules.

## Commands
Run from the project folder with the virtual environment active (setup: [README](../README.md#development-environment)).

| Purpose | Command |
|---------|---------|
| (1) Format | `ruff format .` (add `--check` to only check) |
| (1) Lint | `ruff check .` |
| (2) Unit tests | `pytest` |
| (3) Full suite including database tests | `pytest` (same command until T-012 adds a database; then database tests join it) |
| Django configuration check | `APP_ENV=development python manage.py check` |

Notes: ruff also checks Python code blocks inside the Markdown docs. With a valid production configuration, `python manage.py check --deploy` reports 3 expected warnings (HSTS, SSL redirect, secure CSRF cookie); T-063 resolves them with the chosen host. `pytest` forces development mode (`config/settings_test.py`), so results do not depend on your shell variables; startup tests run the real settings in a fresh process.

## Layers
| Layer | Covers |
|-------|--------|
| Unit | Pricing, validation, permissions, state transitions, normalization |
| Database/integration | Constraints (price, stock, uniqueness, composite keys, restrict-on-delete), transactions, migrations on a fresh database, service operations |
| Web | Page responses, authorization of every admin URL, form validation, CSRF, escaping, pagination caps |
| Bot | Webhook secret, unlinked users, malformed/replayed updates, duplicate `update_id`, timeouts (Telegram calls mocked) |
| Security | Cross-seller access, admin-only operations, upload abuse, order tampering |
| Manual mobile check | Checklist below, run by the human before each phase gate |

## Critical scenarios (each must have an automated test)
1. Public users see only published products, active offers, active sellers.
2. Seller A cannot read or change seller B's offers (Telegram path).
3. Unlinked or revoked Telegram users cannot read or change anything.
4. Sellers can change only price/stock/availability of their own offer variants.
5. New canonical products and spec changes require admin approval.
6. Order totals come from the server; tampered price/total/seller/status are ignored or rejected.
7. Stale displayed price is rejected with `price_changed`.
8. Order items keep snapshots after later edits/archival.
9. Duplicate submission (same key) returns one order; two parallel submissions do not create duplicates.
10. Confirmation under concurrency never makes stock negative.
11. Invalid or oversize uploads are rejected safely.
12. Sensitive admin changes create audit records.
13. List operations enforce page-size caps.
14. Every admin URL denies anonymous and non-admin users.
15. Duplicate/replayed Telegram updates and reused confirmation tokens have no second effect.

## Rules
- **Synthetic data only**; never real customer, seller, or credential data.
- Every behavior change needs tests; every bug fix gets a regression test.
- Tests must be deterministic and independent. Do not weaken, skip, delete, or loosen tests to make a task pass; if a test is wrong, stop and ask the human.
- Concurrency tests use real database transactions, not mocks.
- Report only commands actually run, with the observed result; list what was **not** run and why.

## Evidence format (in the task report)
`command` -> pass/fail counts (or the exact error). Failing or unrun tests are reported, never hidden.

## Manual mobile checklist (human, per phase gate)
- [ ] Listing, detail, order form usable on a phone screen without horizontal scrolling.
- [ ] Works with JavaScript disabled.
- [ ] Throttled-network run done; numbers recorded in [PERFORMANCE](PERFORMANCE.md).
- [ ] Burmese and English text render correctly on the target phone.
- [ ] Order submitted twice quickly (double tap) creates one order.
