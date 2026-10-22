# Roadmap

Ordered sequence from documentation to a pilot-ready MVP. Task cards (full detail) are in `tasks/cards/`. Rules for working on tasks: [AGENTS.md](../AGENTS.md), [docs/AI-WORKFLOW.md](../docs/AI-WORKFLOW.md).

## Rules
- Tasks are done in order unless the Owner approves a different order. One task at a time.
- A task is `Done` only when the **Owner** marks it, with evidence (test output, screenshots, or notes) recorded in its report.
- Status values: `Not started`, `In progress`, `Ready for review`, `Done`, `Blocked`.
- Prefer one working vertical slice over many incomplete features. Do not start a phase before the previous phase's gate is met.
- A card is a contract: if the work needs something the card does not allow, stop and ask.

## Index
| ID | Task | Needs first | Status | Card |
|----|------|-------------|--------|------|
| T-000 | Documentation baseline v2 | none | Done | [01](cards/01-foundation.md) |
| T-001 | Resolve blocking decisions | T-000 Done | Done | [01](cards/01-foundation.md) |
| T-002 | Verify hosting and free-tier facts | T-001 | Ready for review | [01](cards/01-foundation.md) |
| T-010 | Project skeleton and tooling | T-001 Done (D-01 Accepted) | Blocked: Owner marks T-001 Done | [01](cards/01-foundation.md) |
| T-011 | Configuration and secrets handling | T-010 | Blocked | [01](cards/01-foundation.md) |
| T-012 | Local database and migration baseline | T-011 | Blocked | [01](cards/01-foundation.md) |
| T-013 | Continuous integration | T-012 | Blocked | [01](cards/01-foundation.md) |
| T-020 | Catalog schema and constraints | T-012, D-07 categories | Blocked | [02](cards/02-catalog-admin.md) |
| T-021 | Synthetic seed data | T-020 | Blocked | [02](cards/02-catalog-admin.md) |
| T-022 | Public product listing | T-021 | Blocked | [02](cards/02-catalog-admin.md) |
| T-023 | Public product detail | T-022 | Blocked | [02](cards/02-catalog-admin.md) |
| T-024 | Search and category filter | T-022 | Blocked | [02](cards/02-catalog-admin.md) |
| T-025 | Image processing service | T-020, D-06 | Blocked | [02](cards/02-catalog-admin.md) |
| T-026 | Images on catalog pages | T-023, T-025 | Blocked | [02](cards/02-catalog-admin.md) |
| T-030 | Admin authentication and role enforcement | Phase 2 gate | Blocked | [02](cards/02-catalog-admin.md) |
| T-031 | Audit log service | T-030 | Blocked | [02](cards/02-catalog-admin.md) |
| T-032 | Admin: products and variants | T-031 | Blocked | [02](cards/02-catalog-admin.md) |
| T-033 | Admin: image upload and permission | T-032, T-025, D-06 | Blocked | [02](cards/02-catalog-admin.md) |
| T-034 | Admin: sellers, offers, offer variants | T-032 | Blocked | [02](cards/02-catalog-admin.md) |
| T-035 | Admin: draft review queue | T-034 | Blocked | [02](cards/02-catalog-admin.md) |
| T-040 | Order schema and state machine | T-034, D-03 | Blocked | [03](cards/03-orders-telegram.md) |
| T-041 | Order submission operation | T-040 | Blocked | [03](cards/03-orders-telegram.md) |
| T-042 | Order form page | T-041 | Blocked | [03](cards/03-orders-telegram.md) |
| T-043 | Admin: order management | T-041, T-034 | Blocked | [03](cards/03-orders-telegram.md) |
| T-050 | Telegram account linking | T-043 (Phase 4 gate) | Blocked | [03](cards/03-orders-telegram.md) |
| T-051 | Seller operations (service layer) | T-050 | Blocked | [03](cards/03-orders-telegram.md) |
| T-052 | Telegram webhook and bot infrastructure | T-050, D-08 | Blocked | [03](cards/03-orders-telegram.md) |
| T-053 | Bot flows: My offers, price, stock | T-051, T-052 | Blocked | [03](cards/03-orders-telegram.md) |
| T-054 | Bot flow: Add product draft | T-052, T-035 | Blocked | [03](cards/03-orders-telegram.md) |
| T-060 | Security review and hardening | T-053, T-054, T-043 | Blocked | [04](cards/04-pilot.md) |
| T-061 | Performance measurement | T-026, T-042 | Blocked | [04](cards/04-pilot.md) |
| T-062 | Backup and restore drill | T-054 | Blocked | [04](cards/04-pilot.md) |
| T-063 | Production deployment and runbooks | T-060, T-061, T-062, T-002 | Blocked | [04](cards/04-pilot.md) |
| T-064 | Pilot readiness and protocol | T-063, D-04, D-05, D-09 | Blocked | [04](cards/04-pilot.md) |

## Phase gates (Owner confirms with evidence)
- **Gate 0 (after T-001, T-002):** ADRs 0005 and 0006 Accepted; hosting facts recorded.
- **Gate 1 (after T-013):** app starts locally; lint and tests run; CI runs; no secrets tracked.
- **Gate 2 (after T-026):** a phone-sized browser can list, search and view synthetic products; AC-CAT-* pass.
- **Gate 3 (after T-035):** admin can manage the catalog and review drafts; AC-ADM-* and AC-IMG-* pass.
- **Gate 4 (after T-043):** order can be submitted and confirmed end to end on synthetic data; AC-ORD-* pass.
- **Gate 5 (after T-054):** seller can link, change price/stock, and submit a draft in a test chat; AC-TG-* pass.
- **Gate 6 (after T-064):** pilot go/no-go checklist signed by the Owner.

## Card format (use for any new card)
```
### T-NNN Title
- Objective:
- Prerequisites:
- Scope:
- Non-goals:
- Docs:
- Expected files/components:
- Acceptance:        (reference AC-IDs where they exist)
- Required tests:
- Risks:
- Done when:         (standard Definition of Done in docs/AI-WORKFLOW.md, plus any additions)
```
Concrete file paths are set by T-010 and then recorded in [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md); until then cards name components, not paths.
