# Project Charter

**Authoritative for:** product goals, scope, roles, pilot metrics. Decision status lives in [decisions/README.md](decisions/README.md).

## Purpose
A mobile-first, low-bandwidth marketplace for clothing and fashion in Myanmar. Run a **zero-budget pilot** with a small, curated group of sellers to learn whether customers order and sellers keep information current.

## Product decisions (final)
- Initial category: clothing and fashion. Initial category list is a default (D-07).
- Shared canonical product catalog with seller-specific offers ([ADR-0001](decisions/0001-shared-catalog.md)).
- Customers order via a platform form; confirmation is manual ([ADR-0002](decisions/0002-manual-order-confirmation.md)).
- Admin manages products, specifications, images, sellers, offers, draft reviews and orders.
- Sellers manage price/stock of their own approved offers and submit new-product drafts through a guided Telegram bot; they do not use the web admin ([ADR-0003](decisions/0003-telegram-seller-operations.md)).
- English-first interface. Burmese product text is optional; no localization framework in the MVP.
- Curated seller onboarding only. No public seller registration.
- Only authorized product images.
- No payments, wallets, built-in chat, seller dashboard, delivery tracking, recommendations, or automated procurement in the MVP.

## Roles
| Role | Can do |
|------|--------|
| Anonymous visitor | Browse published products; submit an order (guest) |
| Admin | Everything in the admin site; approve sellers, products, drafts; handle orders |
| Approved seller (via Telegram only) | View and change price/stock/availability of **own** offers; submit drafts |
| System | Run seed/maintenance commands and webhook processing as defined in [API-CONTRACT](API-CONTRACT.md) |

The full permission matrix is in [SECURITY](SECURITY.md#permission-matrix).

## Pilot questions and metrics
The pilot exists to measure (definitions only; thresholds are owner decisions, D-04):
1. Seller participation: share of invited sellers who link Telegram and make at least one update.
2. Price/stock freshness: share of offer variants confirmed within the stale threshold.
3. Order completion: submitted orders that reach `completed` / all submitted.
4. Cancellation reasons, including stale price or stock.
5. Admin time spent per order.
6. Page weight and load time on throttled mobile ([PERFORMANCE](PERFORMANCE.md)).

## Business questions still open (owner)
Revenue model, delivery responsibility, returns policy, payment arrangement, retention period, legal checks: see D-04, D-05, D-09. Engineering can proceed without them until T-064.
