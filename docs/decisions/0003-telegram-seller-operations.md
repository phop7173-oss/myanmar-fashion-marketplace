# ADR-0003: Sellers operate through a guided Telegram bot
- Status: Accepted (carried over from the original project charter)
- Date: 2026-10-20 (recorded)
- Decision owner: Project owner

## Context
Sellers are curated and few, likely mobile-only, and should not need a web dashboard.

## Decision
- Sellers manage their own approved offers (price, stock, availability) and submit new-product drafts through a guided Telegram bot.
- New canonical products and canonical changes go to admin review.
- No seller web dashboard in the MVP.
- Telegram identity = the numeric Telegram user ID linked to an approved seller by admin ([INTEGRATIONS](../INTEGRATIONS.md)).

## Alternatives considered
Seller web dashboard (rejected: scope), spreadsheet upload (rejected: validation burden), admin entering everything (rejected: does not scale and stale prices).

## Consequences
Bot UX must be simple and safe against mistakes (preview and confirm). Sellers need reliable Telegram access (UNVERIFIED for each seller; confirm during pilot recruitment).

## Revisit triggers
Sellers cannot or will not use Telegram, or error rates in bot updates are high.
