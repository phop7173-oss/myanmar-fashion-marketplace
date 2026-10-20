# ADR-0004: One trust boundary and one place for business rules
- Status: Accepted
- Date: 2026-10-20
- Decision owner: Project owner

## Context
The storefront, admin site and Telegram bot all change the same data. Duplicated rules lead to security holes and inconsistent prices.

## Decision
- All business rules (validation, authorization, pricing, stock, order transitions) live in **one server-side service layer**.
- Web pages, admin screens and Telegram handlers are thin: they parse input, call a service operation, and present the result.
- The browser and Telegram are untrusted. No client-supplied identity, ownership, price, total or status is trusted.
- Whether the bot reaches the service layer in-process or over authenticated HTTP depends on ADR-0005; the rules above apply either way.

## Alternatives considered
Bot with direct database access; business rules in the frontend or bot. Both rejected.

## Consequences
Every new feature starts as a service operation with tests; UI comes after.

## Revisit triggers
None expected for the MVP.
