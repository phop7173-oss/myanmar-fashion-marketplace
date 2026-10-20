# API and Operation Contract

**Authoritative for:** what operations exist, who may call them, and how they behave. Business rules: [ARCHITECTURE](ARCHITECTURE.md) layering. Order details: [ORDER-WORKFLOW](ORDER-WORKFLOW.md). Fields: [DATA-MODEL](DATA-MODEL.md).

Every operation below is implemented **once** in the service layer. Web pages, admin screens, and bot handlers are only different front doors to the same operation with the same authorization.

## Rules for every operation
1. Identity comes from verified authentication (admin session, verified Telegram numeric ID), never from request fields.
2. Check authorization inside the service operation, then check ownership of every resource ID supplied (prevents IDOR/BOLA). A seller asking for another seller's offer gets `not_found`, not `forbidden`.
3. Validate and normalize all input; reject unknown fields; limit lengths and sizes.
4. Prices, totals, statuses, seller IDs and timestamps are computed or read on the server.
5. Lists are paginated: `page` >= 1, `page_size` default 20, maximum 50; deterministic ordering.
6. Writes that must be atomic use one transaction ([DATA-MODEL](DATA-MODEL.md#transactions-must-be-atomic)).
7. Sensitive writes append an audit record in the same transaction.
8. Each operation ships with tests for: success, invalid input, denied access, and (where applicable) duplicate/replay and stale state.

## Error model
Stable machine codes; friendly text; never internal details (no stack traces, SQL, file paths, other users' data).

| Code | Meaning | HTTP-like status |
|------|---------|------------------|
| `validation_error` | Input invalid (with per-field messages) | 400 |
| `unauthenticated` | No valid login/identity | 401 |
| `forbidden` | Authenticated but not allowed | 403 |
| `not_found` | Missing **or not visible to the caller** | 404 |
| `conflict` | State changed (`price_changed`, `insufficient_stock`, stale `row_version`, duplicate with different content, illegal transition) | 409 |
| `rate_limited` | Too many requests | 429 |
| `unexpected_error` | Anything else; logged with a request ID shown to the user | 500 |

## Idempotency
- Order submission: client-generated UUID per form render; see [ORDER-WORKFLOW](ORDER-WORKFLOW.md).
- Bot updates: duplicate `update_id` ignored; confirmation tokens usable once; price/stock changes use absolute values plus `row_version`.
- Draft submission: unique idempotency key per seller.
- Admin state changes are idempotent by state check (repeating "confirm" on a confirmed order returns the current state, not a second deduction).

## Operations

### Public (no login)
| ID | Operation | Rules |
|----|-----------|-------|
| CAT-1 | List products (`q`, `category`, `page`) | Only public data; bounded; no unpublished leakage; search input parameterized |
| CAT-2 | Product detail by `slug` | Variants, public offers, prices, stale labels, public images only |
| ORD-1 | Submit order | Full rules in ORDER-WORKFLOW; rate limited; honeypot; idempotent |

### Admin (admin session required; every operation checks `is_admin`)
| ID | Operation | Rules |
|----|-----------|-------|
| ADM-1 | Create/edit/publish/archive product and variants | No hard delete; duplicate warning; audited |
| ADM-2 | Upload image + record source and permission | Upload rules in SECURITY; confirmation audited |
| ADM-3 | Create/approve/suspend seller | Audited |
| ADM-4 | Create/edit offer and offer variants (price, stock, availability) | Composite integrity; `row_version`; audited |
| ADM-5 | Review product draft (approve/reject) | Atomic creation on approve; audited |
| ADM-6 | Orders: list, view, confirm, complete, cancel | State machine; stock locking; viewing customer data restricted to admin |
| ADM-7 | Issue Telegram link code; revoke Telegram account | Code shown once, stored hashed; audited |
| ADM-8 | Create first admin | Command-line only, never a web page |

### Seller (Telegram only; caller is a linked, active seller)
| ID | Operation | Rules |
|----|-----------|-------|
| SEL-1 | List my offer variants (paginated) | Only own offers |
| SEL-2 | Change price / stock / availability of own offer variant | Two steps: preview creates a pending action; confirm applies it. Validates bounds, `row_version`, large-change warning (default 50%, D-07); audited |
| SEL-3 | Submit draft (`new_product`, `new_offer`, `spec_change`) | Goes to admin review; idempotent; no images in the MVP |
| SEL-4 | Cancel pending action / draft in progress | Own actions only |
| SEL-5 | Link account with code | Single-use, expiring; ID taken from Telegram, never from message text |

### Telegram inbound (system)
| ID | Operation | Rules |
|----|-----------|-------|
| TG-1 | Receive update | Verify secret token header (else 403, no processing); dedupe by `update_id`; unknown/unlinked sender gets a generic reply and **no data**; replies never contain customer personal data |

## Change control
Any change to an operation's behavior updates this file and its tests in the same task.
