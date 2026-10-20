# Data Model Contract

**Authoritative for:** tables, columns, constraints, indexes, transactions. This is a specification, not SQL. Implementation happens in migrations created by task cards ([ROADMAP](../tasks/ROADMAP.md)). Do not create a table before the task that needs it.

## Conventions
- Internal IDs: immutable UUID primary keys named `id`. Public references: product `slug`, order `public_ref`. **References are never authorization.**
- Money: whole-kyat integers in `*_mmk` columns (MMK has no practical minor unit). No floats, no decimals. Currency is MMK only in the MVP (CHECK constraint where a currency column exists).
- Timestamps: `timestamptz`, stored in UTC; displayed in Myanmar time (UTC+06:30). Every table has `created_at`; mutable tables also `updated_at`.
- Naming: snake_case, singular concepts, [CODE-STYLE](CODE-STYLE.md).
- Enumerations are text columns with a CHECK constraint listing allowed values.
- **No hard deletes** of anything referenced by another row. Use `status` (`archived`, `paused`, `suspended`). Foreign keys use `ON DELETE RESTRICT`. Reason: history (orders) must survive catalog changes.
- Every constraint below exists to block a specific failure; the "Why" column says which.

## Visibility rules (authoritative)
- A **product** is public iff `status = 'published'`.
- An **offer** is public iff `seller_offers.status = 'active'` AND `sellers.status = 'active'`.
- An **offer variant** is **orderable** iff its offer is public, its product variant is `active`, `is_available = true`, and (`stock_quantity IS NULL` or `stock_quantity > 0`).
- `stock_quantity = NULL` means **unknown**; `0` means **sold out**. Unknown stock is orderable (manual confirmation resolves it) but is shown as "availability to be confirmed".
- A product with no orderable offer variant is excluded from listings; its detail page still loads and says "currently unavailable".
- A price or stock value is **stale** when its `*_confirmed_at` is older than the stale threshold (default 7 days, D-07). Stale values are labelled "last confirmed N days ago".
- An image is public iff `permission_status = 'confirmed'` and its product is published.

## Tables

### sellers (T-020)
`id`, `display_name` (required, public), `status` (`pending`, `active`, `suspended`; default `pending`), `internal_note` (admin-only, never public), timestamps.
Unique: lower(`display_name`). Why: avoids impersonation by lookalike seller names.

### users (T-030)
Admin accounts, provided by the authentication framework. Flag `is_admin`. Sellers have **no web login** in the MVP, so no seller-user link exists.

### telegram_accounts (T-050)
`id`, `telegram_user_id` (bigint, required), `seller_id` (FK), `status` (`active`, `revoked`), `linked_at`, `revoked_at`, `last_username` (nullable, display only).
Unique: `telegram_user_id`; unique: `seller_id` (one Telegram account per seller in the MVP).
Why: identity is the **numeric** Telegram ID. Usernames change and can be reassigned; `last_username` is never used for authorization.

### telegram_link_codes (T-050)
`id`, `seller_id` (FK), `code_hash` (unique; the plain code is shown once to admin and never stored), `expires_at`, `used_at` (nullable), `created_by` (admin user FK), `created_at`.
Why: a one-time, expiring, admin-issued code is how a Telegram ID becomes linked to a seller. Consuming a code is a single conditional update (`used_at IS NULL AND expires_at > now`) inside a transaction so a code cannot be used twice.

### products (T-020)
`id`, `slug` (unique, URL-safe), `title` (English, required, length-limited), `title_my` (nullable Burmese), `description`, `brand` (nullable), `category` (CHECK against the category list, D-07), `specifications` (plain text, nullable, length-limited), `normalized_title` (lowercased, Unicode NFC, whitespace-collapsed), `status` (`draft`, `published`, `archived`), `published_at`, timestamps.
Indexes: unique `slug`; (`status`, `published_at` desc, `id`) for listings; `normalized_title` for duplicate detection.
Why: duplicate canonical products cannot be fully prevented by a constraint (titles legitimately repeat), so admin review shows a **duplicate warning** from `normalized_title` + `brand`; only `slug` is hard-unique.

### product_variants (T-020)
`id`, `product_id` (FK), `size` (required), `color` (required), `status` (`active`, `archived`), `sort_order`, timestamps. Use the literal `N/A` when size or color does not apply.
Unique: (`product_id`, lower(`size`), lower(`color`)); unique (`id`, `product_id`) (target for composite keys).
Why: prevents duplicate variants of the same product. Variants belong to the canonical product, so sellers cannot create them.

### seller_offers (T-020)
`id`, `seller_id` (FK), `product_id` (FK), `status` (`active`, `paused`, `archived`), `created_from_draft_id` (nullable), timestamps.
Unique: (`seller_id`, `product_id`) -- Why: one seller cannot create duplicate offers for the same product; they pause or archive instead. Unique (`id`, `seller_id`) and (`id`, `product_id`) -- targets for composite keys.
Indexes: (`product_id`) filtered to active; (`seller_id`).

### offer_variants (T-020)
`id`, `offer_id`, `product_id`, `product_variant_id`, `price_mmk` (bigint, required), `stock_quantity` (integer, nullable), `is_available` (boolean, default true), `price_confirmed_at` (required), `stock_confirmed_at` (nullable), `row_version` (integer, default 1, incremented on every update), timestamps.
- Check: `price_mmk > 0` and `price_mmk <= 100000000` (sanity ceiling, PROVISIONAL). Why: invalid prices.
- Check: `stock_quantity IS NULL OR stock_quantity >= 0`. Why: negative stock.
- Unique: (`offer_id`, `product_variant_id`). Why: no duplicate rows for one variant of one offer.
- Composite foreign keys: (`offer_id`, `product_id`) -> `seller_offers (id, product_id)` and (`product_variant_id`, `product_id`) -> `product_variants (id, product_id)`. Why: guarantees an offer cannot list a variant of a *different* product, even if an admin form allows the mistake.
- `row_version`: updates specify the version they read; a mismatch is rejected as a conflict (optimistic concurrency). Why: concurrent or replayed updates must not overwrite newer data silently.
- Index: (`offer_id`), (`product_variant_id`).

### product_images (T-025)
`id`, `product_id` (FK), `offer_id` (nullable; set only for an image of a specific seller's item), `storage_key` (generated, unique, never user-supplied), `content_type`, `width`, `height`, `byte_size`, `alt_text`, `sort_order`, `source_type` (`own_photo`, `seller_permission`, `licensed`, `other_authorized`), `source_note` (required: who granted permission or where from), `permission_status` (`unverified`, `confirmed`), `permission_confirmed_by` (admin FK), `permission_confirmed_at`, timestamps.
- Check: `permission_status = 'confirmed'` requires confirmer and time.
- Composite FK (`offer_id`, `product_id`) -> `seller_offers (id, product_id)` when `offer_id` is set.
- Index: (`product_id`, `sort_order`).
Why one table: product and offer images share the same rules; a separate offer-image table duplicates them. Why permission fields: AGENTS rule "authorized images only" must be provable per image.

### product_drafts (T-035)
`id`, `seller_id` (FK), `kind` (`new_product`, `new_offer`, `spec_change`), `target_product_id` (nullable), `payload` (JSON, validated against a schema before storage), `status` (`pending`, `approved`, `rejected`, `withdrawn`), `reviewed_by`, `reviewed_at`, `review_note`, `result_product_id`, `result_offer_id`, `idempotency_key` (unique per seller), timestamps.
Why: sensitive changes wait for admin review (ADR-0003). Approval creates product/offer rows and flips status in one transaction. The idempotency key stops a retried bot request from creating two drafts.

### bot_pending_actions (T-052)
`id` (UUID used as the short opaque token in button data), `telegram_user_id`, `seller_id`, `action` (`update_price`, `update_stock`, `draft_wizard`, ...), `payload` (JSON: target offer variant, field, new value, expected `row_version`, wizard step), `status` (`in_progress`, `awaiting_confirmation`, `confirmed`, `cancelled`, `expired`), `expires_at`, timestamps.
Why: Telegram button data is attacker-controllable and size-limited, so buttons carry only the token; everything meaningful is stored server-side and re-checked against the acting seller.

### telegram_updates_processed (T-052)
`update_id` (bigint, primary key), `received_at`. Purged after a short period (default 7 days, PROVISIONAL).
Why: Telegram may deliver the same update more than once; inserting the update id first lets duplicates be ignored. Because a crash can leave an update half-processed, writes are *also* idempotent by design (absolute values + `row_version`, tokens used once).

### orders (T-040)
`id`, `public_ref` (unique, random, non-sequential, e.g. 8 characters from an unambiguous alphabet), `seller_id` (FK), `status` (`submitted`, `confirmed`, `completed`, `cancelled`), `idempotency_key` (UUID, unique), `request_hash`, `customer_name`, `customer_phone`, `contact_channel` (nullable), `delivery_address`, `township`, `region`, `customer_note` (nullable), `currency` (CHECK = `MMK`), `items_total_mmk` (> 0), `delivery_fee_mmk` (nullable, >= 0), `submitted_at`, `confirmed_at`, `confirmed_by`, `completed_at`, `cancelled_at`, `cancel_reason` (CHECK: `customer_request`, `seller_unavailable`, `price_or_stock_changed`, `unreachable`, `duplicate`, `other`), `personal_data_erased_at` (nullable), timestamps.
Indexes: (`status`, `submitted_at` desc); (`seller_id`, `status`).
Why: unique idempotency key = a retried or double-clicked submission cannot create two orders; `request_hash` detects the same key reused with different content (conflict).

### order_items (T-040)
`id`, `order_id` (FK), `offer_variant_id` (FK, reference only), snapshots: `product_id`, `product_title`, `seller_name`, `variant_size`, `variant_color`, `unit_price_mmk` (> 0), `quantity` (> 0), `line_total_mmk`, `stock_deducted` (boolean, default false).
- Check: `line_total_mmk = unit_price_mmk * quantity`.
- `orders.items_total_mmk` = sum of line totals; enforced in the order service inside the transaction and verified by tests.
- Index: (`order_id`).
Why snapshots: history must not change when products, sellers or prices are edited or archived. Display uses snapshot columns, not live data.

### audit_logs (T-031)
`id` (identity), `occurred_at`, `actor_type` (`admin`, `seller_bot`, `customer`, `system`), `actor_user_id` (nullable), `actor_seller_id` (nullable), `action` (e.g. `offer_variant.price_changed`), `entity_type`, `entity_id`, `before` and `after` (JSON, only the changed non-sensitive fields), `request_id` (nullable).
Indexes: (`entity_type`, `entity_id`, `occurred_at`); (`occurred_at`).
Rules: append-only (application code never updates or deletes rows; production database role should lack update/delete). **Never store secrets or customer phone/address** in `before`/`after`.
Audited actions: price/stock/availability changes, publish/archive, seller approval/suspension, offer changes, draft decisions, image permission confirmation, Telegram link/revoke, order status changes, admin login failures, admin creation.

## Transactions (must be atomic)
1. Order submission: order + items.
2. Order confirmation: stock locks/deductions + status + audit.
3. Order cancellation: stock restoration + status + audit.
4. Draft approval: created product/variants/offer/offer variants + draft status + audit.
5. Link-code consumption + telegram account creation.
6. Any price/stock update: row update + `row_version` increment + audit.

## Concurrency rules
- Lock offer variant rows with `SELECT ... FOR UPDATE` in ascending `id` order when a transaction touches several (avoids deadlocks).
- Updates to `offer_variants` always include the expected `row_version`.

## Indexes
Create only those listed above, plus any added with query-plan evidence recorded in the task report. Listing "from price" is computed by query; no denormalized column until measurement proves a need.

## Migrations
Reviewed in the plan step; never edit an applied migration; destructive changes (drop/rename/data loss) need explicit owner approval and a backup first. Each migration is tested on a fresh database. Rollback approach: [DEPLOYMENT](DEPLOYMENT.md#rollback).
