# Data Model Contract

Candidate entities:
- users
- sellers
- telegram_users
- products
- product_variants
- product_images
- seller_offers
- offer_variants
- offer_images
- product_drafts
- orders
- order_items
- audit_logs

Do not create every table before defining the first working feature.

## Relationships
- One canonical product can have multiple seller offers.
- Each offer belongs to one seller and one canonical product.
- Offer variants hold seller-specific price, stock, and availability.
- Orders contain one or more order items.
- Order items preserve purchase-time snapshots.

## Constraints
- Use immutable UUID internal IDs.
- Enforce foreign keys and appropriate uniqueness constraints.
- Store timestamps in UTC and display local time when needed.
- Never use floating-point arithmetic for money.
- Decide and document MMK precision and rounding before implementation.
- Distinguish unknown stock from zero stock.
- Record when prices and stock were last confirmed.
- Index real query patterns and verify performance using query plans.

Order item snapshots should preserve product title, seller name, selected variant, unit price, quantity, line total, and currency.

Collect only customer data needed for fulfillment. Restrict access and define retention before production.
