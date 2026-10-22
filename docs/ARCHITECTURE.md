# Architecture

**Authoritative for:** system shape, module boundaries, trust boundaries, scope tiers. Technology names and versions: [TECH-STACK](TECH-STACK.md). Data: [DATA-MODEL](DATA-MODEL.md). Behavior: [API-CONTRACT](API-CONTRACT.md), [ORDER-WORKFLOW](ORDER-WORKFLOW.md).

## System shape
One web application and one PostgreSQL database serve three interfaces:
1. Customer storefront (server-rendered, mobile-first).
2. Admin website.
3. Telegram seller bot (webhook endpoint of the same application under the recommended baseline, [ADR-0005](decisions/0005-platform-baseline.md)).

```
Customer browser ─┐
Admin browser ────┼─> Views / Admin / Bot handlers (thin) ──> Service layer ──> Database
Telegram ─────────┘        parse + present only            all business rules   constraints
```

Everything left of the service layer is untrusted input. The database enforces integrity as a second line of defense.

## Layering rules
1. **Views, admin screens and bot handlers contain no business rules.** They validate shape, call one service operation, and render the result.
2. **Service layer** owns: authorization checks, validation, price/total calculation, stock changes, status transitions, audit records, transactions.
3. **Models/database** own: types, foreign keys, uniqueness, check constraints.
4. A rule needed in two places is implemented once in the service layer and called from both.
5. The bot never reads or writes database tables directly; it uses service operations only.

## Core domain model
See [DATA-MODEL](DATA-MODEL.md). In one line: product -> product variants; seller offer = (seller, product); offer variant = (offer, product variant) holding price and stock; order -> order items (snapshots).

## Repository layout
Created by T-010 (2026-10-23). Only these exist; AI agents must not assume others.
```
manage.py                  Django command-line entry point
pyproject.toml             ruff and pytest configuration
requirements.txt           pinned runtime dependencies (lockfile)
requirements-dev.txt       pinned development/test dependencies (lockfile)
config/                    project settings, URL routing, WSGI entry point
storefront/                customer-facing app (placeholder home page only)
  templates/storefront/    page templates
  static/storefront/       the single small CSS file
  tests/                   storefront tests
docs/  tasks/              documentation and task cards
```
No database, models, login, admin or bot exist yet (T-012 and later).

## Scope tiers

### Required for MVP
- Public catalog: listing, product detail, basic search/category filter, pagination.
- Admin: login, products/variants, images with permission record, sellers, offers/offer variants, draft review, orders, audit log.
- Orders: guest order form, server-side pricing, idempotent submission, manual confirm/complete/cancel.
- Telegram bot: account linking, My offers, update price, update stock, add-product draft.
- Image processing (validation + responsive derivatives) done at upload time.
- Automated tests, CI, local PostgreSQL, synthetic seed data.

### Required before real customers (production)
- Verified hosting with HTTPS and data export ([T-002](../tasks/cards/01-foundation.md), [T-063](../tasks/cards/04-pilot.md)).
- Tested encrypted off-site backup and restore ([DEPLOYMENT](DEPLOYMENT.md)).
- Security checklist passed ([SECURITY](SECURITY.md#pre-production-security-checklist)).
- Dependency vulnerability scan; secret scan.
- Privacy notice and retention rule (D-05); legal check (D-09).
- Admin multi-factor authentication if supported by the chosen stack (UNVERIFIED).
- Basic uptime/error monitoring.

### Future enhancements (not specified yet)
Burmese localization, seller photo uploads via bot, customer order tracking, notifications to sellers/customers, multi-seller carts, payments, delivery integration, search ranking, CDN, reservation of stock at submission, seller web dashboard.

### Rejected or unnecessary for now
Microservices, message queues, Redis/caching layers, separate search engine, GraphQL, single-page app framework, container orchestration, third-party analytics/chat/ad scripts, offer-specific image table (images share one table), custom authentication code, custom CSRF/session code.

## Environments
Local development (Ubuntu laptop) with synthetic data; production when verified. A separate preview environment is optional (cost). Never use production data or credentials in development. Details: [DEPLOYMENT](DEPLOYMENT.md).

## Changing this document
Material changes need an ADR approved by the owner ([decisions/README.md](decisions/README.md)).
