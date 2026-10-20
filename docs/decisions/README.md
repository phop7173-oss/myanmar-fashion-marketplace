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

Also accepted (from the original charter, no separate ADR needed): English-first interface, clothing/fashion first, curated sellers only, zero-budget pilot, authorized images only, development on the owner's Ubuntu laptop, GitHub as source of truth, humans approve requirements/security/architecture/releases.

## Open decisions (need the human owner)

| ID | Question | Recommended default | Blocks | Detail |
|----|----------|---------------------|--------|--------|
| D-01 | Technology baseline (language/framework/UI approach) | Single Python/Django web app, server-rendered, plain CSS (beginner-friendly, one language, built-in admin/auth/CSRF) | T-010 and everything after | [0005](0005-platform-baseline.md) |
| D-02 | Hosting + database provider under zero budget | None chosen. Verify candidates in T-002 | T-063; real-world webhook testing | [0005](0005-platform-baseline.md), [TECH-STACK](../TECH-STACK.md) |
| D-03 | MVP order model (one seller per order, guest checkout, reserve stock at confirmation, delivery fee set manually, payment outside platform) | As listed | T-040 | [0006](0006-mvp-order-model.md) |
| D-04 | Business operations: revenue model, who delivers, returns policy, how payment happens, pilot success thresholds | None. Owner must define | T-064 (go/no-go) | [PROJECT](../PROJECT.md) |
| D-05 | Customer data retention period and privacy notice | Erase/anonymize personal data 12 months after order completion (PROVISIONAL) | T-064 | [SECURITY](../SECURITY.md) |
| D-06 | Image sourcing policy: who supplies images, how permission is recorded | Admin uploads only; seller photos via Telegram deferred; permission recorded per image | T-025, T-033 | [DATA-MODEL](../DATA-MODEL.md) |
| D-07 | Tunable defaults: stale threshold 7 days, max quantity per item 10, large price-change warning 50%, page size 20/max 50, category list | As listed; category list: tops, bottoms, dresses, outerwear, traditional wear, footwear, accessories, other | Nothing (defaults apply until changed); category list needed by T-020 | [PROJECT](../PROJECT.md) |
| D-08 | Telegram bot delivery mode: webhook vs polling | Webhook (no always-on worker needed) | T-052 | [0005](0005-platform-baseline.md), [INTEGRATIONS](../INTEGRATIONS.md) |
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
