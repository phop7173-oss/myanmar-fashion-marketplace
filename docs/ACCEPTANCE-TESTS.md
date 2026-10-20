# Acceptance Criteria

**Authoritative for:** testable requirements with IDs. Task cards reference these IDs; a task is not Done until its criteria have passing evidence ([TESTING](TESTING.md)). Behavior details live in the linked docs; this file states only what must be verifiably true.

## Catalog (AC-CAT)
- **AC-CAT-01** Public pages show only published products, active offers of active sellers ([visibility rules](DATA-MODEL.md#visibility-rules-authoritative)).
- **AC-CAT-02** Product, seller offer, product variant and offer variant are distinct records; price and stock exist only on offer variants.
- **AC-CAT-03** The database rejects: price <= 0, negative stock, duplicate (seller, product) offers, duplicate variants, an offer variant whose product variant belongs to another product.
- **AC-CAT-04** Listings are paginated (default 20, max 50), deterministically ordered, and reject larger page sizes.
- **AC-CAT-05** Stale price/stock is labelled; unknown stock is distinct from zero stock.
- **AC-CAT-06** Products with no orderable offer variant are excluded from listings; their detail page says "currently unavailable".
- **AC-CAT-07** Search input is parameterized, length-bounded, Unicode-normalized, and never returns unpublished products.
- **AC-CAT-08** Deleting referenced products/sellers/offers/variants is impossible; they are archived instead.

## Images (AC-IMG)
- **AC-IMG-01** Uploads of disallowed types, oversize files, oversize dimensions, and files whose content does not match their type are rejected.
- **AC-IMG-02** Stored images use generated names; metadata is stripped; derivatives are produced.
- **AC-IMG-03** An image is public only after permission is confirmed; source and confirmer are recorded.
- **AC-IMG-04** Grids use thumbnails/derivatives only, with reserved dimensions.

## Admin (AC-ADM)
- **AC-ADM-01** Anonymous and non-admin users are denied every admin URL (enumerating test).
- **AC-ADM-02** Sensitive admin changes write audit records without secrets or customer personal data.
- **AC-ADM-03** The first admin can be created only from the command line.
- **AC-ADM-04** Approving a draft atomically creates the product/offer rows and updates the draft; a failure leaves nothing partial.
- **AC-ADM-05** Duplicate-product warning appears for matching normalized titles.

## Orders (AC-ORD)
- **AC-ORD-01** The server recomputes prices and totals; tampered price, total, seller, or status values are ignored or rejected.
- **AC-ORD-02** A stale displayed price returns `price_changed` and creates no order.
- **AC-ORD-03** Resubmitting with the same idempotency key returns the same order; same key with different content returns `conflict`; parallel submissions create one order.
- **AC-ORD-04** One order contains items from one seller only.
- **AC-ORD-05** Order items keep product/seller/variant/price snapshots after later edits or archival.
- **AC-ORD-06** Only legal state transitions succeed; all other pairs are rejected.
- **AC-ORD-07** Confirmation deducts known stock under locks and never produces negative stock; insufficient stock leaves the order unchanged.
- **AC-ORD-08** Cancelling a confirmed order restores deducted stock exactly once.
- **AC-ORD-09** Customer personal data is visible only to admins and absent from logs, audit rows, URLs and bot messages.
- **AC-ORD-10** Rate limit and honeypot reject abusive submissions.

## Telegram seller bot (AC-TG)
- **AC-TG-01** Unlinked or revoked Telegram users receive a generic reply and no data; no write occurs.
- **AC-TG-02** Link codes are single-use, expiring, stored hashed; the linked ID comes from Telegram, not message text.
- **AC-TG-03** Username changes do not affect identity.
- **AC-TG-04** A seller cannot read or change another seller's offers (denied as `not_found`).
- **AC-TG-05** Price/stock changes require preview then confirm; a stale `row_version` or expired/used token is rejected.
- **AC-TG-06** Duplicate `update_id` deliveries cause no second effect.
- **AC-TG-07** Missing/wrong webhook secret token returns 403 and does nothing.
- **AC-TG-08** The bot never reports success for a write whose outcome is unknown.
- **AC-TG-09** New products/spec changes become drafts awaiting admin review.

## Security (AC-SEC)
- **AC-SEC-01** No secrets or real data in tracked files, history, or client-delivered pages.
- **AC-SEC-02** Errors shown to users contain no stack traces, SQL, or paths.
- **AC-SEC-03** Security headers present; no third-party scripts.
- **AC-SEC-04** Browser forms reject missing/invalid CSRF tokens.
- **AC-SEC-05** Seller/customer text is escaped on every page (script-injection test).
- **AC-SEC-06** Dependency audit run with results recorded.

## Performance (AC-PERF)
- **AC-PERF-01** Provisional budgets in [PERFORMANCE](PERFORMANCE.md) are measured and recorded; deviations explained.
- **AC-PERF-02** Listing/detail pages use a bounded number of queries (asserted).

## Operations (AC-OPS)
- **AC-OPS-01** A backup is restored to a scratch database and verified (row counts, sample queries).
- **AC-OPS-02** Rollback to the previous release is rehearsed.
- **AC-OPS-03** Secret rotation and seller/bot revocation runbooks are executed once in a test.
