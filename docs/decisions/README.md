# Decision Register

This is the **single authoritative list of project decisions**. Other documents link here; they do not restate decision status.

- **Accepted** = settled. Do not change without a new ADR approved by the human owner.
- **Proposed** = a recommended default exists, but the owner has not approved it. Work that depends on it is blocked (see "Blocks").
- One file per material decision: `NNNN-short-title.md`, using the template at the bottom.

## Accepted decisions

| ADR | Decision | File |
|-----|----------|------|
| 0001 | Shared canonical product catalog; seller-specific offers; variants separate | [0001-shared-catalog.md](0001-shared-catalog.md) |
| 0002 | Platform order form, manual confirmation, no payment gateway, no built-in chat | [0002-manual-order-confirmation.md](0002-manual-order-confirmation.md) |
| 0003 | Sellers operate through a guided Telegram bot; admin reviews new/sensitive catalog changes | [0003-telegram-seller-operations.md](0003-telegram-seller-operations.md) |
| 0004 | One trust boundary: business rules live in one server-side service layer | [0004-single-trust-boundary.md](0004-single-trust-boundary.md) |
| 0005 (D-01, D-08) | Single Python/Django web app, PostgreSQL, server-rendered HTML + plain CSS; Telegram bot as a webhook endpoint in the same app. **Hosting (D-02) is not part of this acceptance.** Accepted 2026-10-20 | [0005-platform-baseline.md](0005-platform-baseline.md) |
| 0006 (D-03) | MVP order model: one seller per order, guest checkout, stock deducted at admin confirmation, manual delivery fee, payment outside the platform, no automatic notifications. Accepted 2026-10-20 | [0006-mvp-order-model.md](0006-mvp-order-model.md) |

Accepted 2026-10-20 without a separate ADR: **D-06** image policy (admin uploads only; seller photos via Telegram deferred; permission recorded per image; see [DATA-MODEL](../DATA-MODEL.md)) and **D-07** tunable defaults (stale threshold 7 days, max quantity per item 10, large price-change warning 50%, page size 20/max 50; categories: tops, bottoms, dresses, outerwear, traditional wear, footwear, accessories, other; see [PROJECT](../PROJECT.md)).

Also accepted (from the original charter, no separate ADR needed): English-first interface, clothing/fashion first, curated sellers only, zero-budget pilot, authorized images only, development on the owner's Ubuntu laptop, GitHub as source of truth, humans approve requirements/security/architecture/releases.

## Open decisions (need the human owner)

| ID | Question | Recommended default | Blocks | Detail |
|----|----------|---------------------|--------|--------|
| D-02 | Hosting + database provider under zero budget | None chosen. Verify candidates in T-002 | T-063; real-world webhook testing | [0005](0005-platform-baseline.md), [TECH-STACK](../TECH-STACK.md) |
| D-04 | Business operations: revenue model, who delivers, returns policy, how payment happens, pilot success thresholds | None. Owner must define | T-064 (go/no-go) | [PROJECT](../PROJECT.md) |
| D-05 | Customer data retention period and privacy notice | Erase/anonymize personal data 12 months after order completion (PROVISIONAL) | T-064 | [SECURITY](../SECURITY.md) |
| D-09 | Legal/regulatory check for operating in Myanmar (registration, e-commerce, data protection) | Human task; AI cannot advise | Launch with real customers | [PROJECT](../PROJECT.md) |

## When to write an ADR

Write one for any choice affecting architecture, data model, security boundaries, deployment, cost, or compatibility. AI agents may **draft** an ADR as `Proposed`; only the human owner sets `Accepted`.

## Template

```
# ADR-NNNN: Title
- Status: Proposed | Accepted | Superseded by ADR-NNNN
- Date:
- Decision owner:

## Context
## Decision
## Alternatives considered
## Consequences
## Revisit triggers
```
