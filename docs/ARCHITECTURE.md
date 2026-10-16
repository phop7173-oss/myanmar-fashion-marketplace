# Architecture

## System shape
One authoritative backend and database serve three interfaces:
1. Customer storefront.
2. Admin web interface.
3. Telegram seller bot.

The Telegram bot calls authenticated backend APIs. It must not duplicate business rules or directly access the production database by default.

## Proposed technology stack
- Web: Next.js App Router.
- Language: TypeScript with strict checking.
- Styling: Tailwind CSS.
- Database: PostgreSQL; Supabase is a candidate.
- Seller bot: Python and python-telegram-bot.
- Image processing: Sharp, subject to hosting compatibility.
- Testing: Vitest and Playwright.

These are proposals until the existing repository is inspected and the stack is approved.

## Core domain model
- product_id: shared canonical product.
- offer_id: one seller's offer for a product.
- variant_id: size/color or another product variant.
- Offer-variant data: seller-specific price, stock, and availability.
- Internal identifiers: immutable UUIDs.
- Human-readable references: support purposes only, never authorization.

## Business invariants
- One canonical product may have many seller offers.
- Admin approval is required for new canonical products and canonical specification changes.
- Sellers can modify only their own approved offers.
- Orders preserve product, seller, variant, quantity, and price snapshots.
- The server validates requests and calculates totals.
- Database constraints protect relationships and uniqueness.
- Use transactions for operations that must succeed or fail together.
- Never use floating-point arithmetic for money.

## Performance
Use server-side pagination, optimized responsive images, bounded queries, minimal client JavaScript, and explicit stale-price/stock indicators.

## Architecture changes
Record major changes to stack, database, API, security boundaries, or deployment in docs/decisions/.
