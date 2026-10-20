# Cards: Phase 4 Orders and Phase 5 Telegram

"Standard DoD" = [Definition of Done](../../docs/AI-WORKFLOW.md#definition-of-done-standard-task-cards-add-to-it). Order rules: [ORDER-WORKFLOW](../../docs/ORDER-WORKFLOW.md) (depends on D-03).

## Phase 4: Orders

### T-040 Order schema and state machine
- **Objective:** Order tables and a single, tested transition function.
- **Prerequisites:** T-034; D-03 Accepted.
- **Scope:** `orders` and `order_items` migrations per DATA-MODEL; public reference generator; transition function with the allowed pairs only.
- **Non-goals:** submission logic, UI.
- **Docs:** DATA-MODEL, ORDER-WORKFLOW, ADR-0006.
- **Components:** migrations, models, transition function.
- **Acceptance:** AC-ORD-06; constraint checks (line total, totals positive, unique idempotency key, unique reference).
- **Required tests:** every state pair (allowed/forbidden); constraint tests; reference uniqueness and non-sequential format.
- **Risks:** deviating from DATA-MODEL; transitions implemented in several places.
- **Done when:** Standard DoD.

### T-041 Order submission operation
- **Objective:** Safe, idempotent order creation (ORD-1) with no UI.
- **Prerequisites:** T-040.
- **Scope:** all submission steps in ORDER-WORKFLOW: validation, rate limits, honeypot handling, idempotency, one-seller rule, quantity/stock checks, displayed-price comparison, server-side totals, snapshots, transaction.
- **Non-goals:** form page, notifications, stock deduction.
- **Docs:** ORDER-WORKFLOW, API-CONTRACT (ORD-1), SECURITY (Rate limiting).
- **Components:** order service, rate-limit helper, tests.
- **Acceptance:** AC-ORD-01..05, AC-ORD-09 (logs), AC-ORD-10.
- **Required tests:** tampered price/total/seller/status; `price_changed`; same key twice; same key different content; two parallel submissions (real transactions); mixed sellers rejected; archived variant after submission keeps snapshots; no personal data in logs.
- **Risks:** proxy/IP handling for rate limits; concurrency test flakiness; money arithmetic.
- **Done when:** Standard DoD; security-sensitive: second-AI review.

### T-042 Order form page
- **Objective:** Mobile-first order form and confirmation page.
- **Prerequisites:** T-041.
- **Scope:** form from product detail (offer variant + quantity), customer fields, hidden idempotency key and displayed price, CSRF, honeypot, error display, confirmation page with public reference; works without JavaScript.
- **Non-goals:** accounts, order lookup, notifications, payment.
- **Docs:** ORDER-WORKFLOW, PERFORMANCE, SECURITY.
- **Components:** form view, templates.
- **Acceptance:** AC-SEC-04, AC-SEC-05, AC-ORD-03 (double submit via UI), performance budget for the form page.
- **Required tests:** missing CSRF rejected; script text escaped in echo-back; double submit creates one order; validation errors shown; no JS needed.
- **Risks:** weak-network re-submission; Burmese input encoding (U10).
- **Done when:** Standard DoD; manual mobile checklist.

### T-043 Admin: order management
- **Objective:** Admin processes orders.
- **Prerequisites:** T-041, T-034.
- **Scope:** ADM-6: list/filter, detail, confirm (locked stock deduction, optional delivery fee, price-difference warning), complete, cancel with reason (stock restoration); audit; personal data visible to admins only.
- **Non-goals:** notifications, refunds, sellers viewing orders.
- **Docs:** ORDER-WORKFLOW, DATA-MODEL (Transactions, Concurrency), SECURITY.
- **Components:** admin order screens, services.
- **Acceptance:** AC-ORD-06..09, AC-ADM-02.
- **Required tests:** concurrent confirmations of the last unit (one succeeds, no negative stock); insufficient stock leaves order unchanged; cancel restores exactly once; repeated confirm is idempotent; non-admin denied; audit written without personal data.
- **Risks:** deadlocks (lock ordering), double deduction, PII in audit.
- **Done when:** Standard DoD; Gate 4 review (end-to-end on synthetic data).

## Phase 5: Telegram seller bot

### T-050 Telegram account linking
- **Objective:** Admin-issued code links a Telegram ID to a seller.
- **Prerequisites:** Gate 4 (T-043).
- **Scope:** `telegram_accounts`, `telegram_link_codes` migrations; ADM-7 (issue code, revoke); SEL-5 service operation (no Telegram transport yet); atomic code consumption.
- **Non-goals:** webhook, flows.
- **Docs:** INTEGRATIONS (Identity and linking), SECURITY, DATA-MODEL.
- **Components:** migrations, services, admin screens.
- **Acceptance:** AC-TG-02, AC-TG-03, AC-TG-01 (service level).
- **Required tests:** expired code; reused code; two parallel uses of one code (one succeeds); Telegram ID already linked; revoked account denied; username change ignored.
- **Risks:** code leakage in logs; plain code stored (must store hash only).
- **Done when:** Standard DoD; security-sensitive: second-AI review.

### T-051 Seller operations (service layer)
- **Objective:** Own-offer listing and price/stock/availability changes with preview/confirm.
- **Prerequisites:** T-050.
- **Scope:** SEL-1, SEL-2, SEL-4 as service operations; `bot_pending_actions` migration (first use); `row_version` check; bounds; large-change warning; audit.
- **Non-goals:** Telegram transport, drafts.
- **Docs:** API-CONTRACT, INTEGRATIONS, SECURITY, DATA-MODEL.
- **Components:** seller services, migration, tests.
- **Acceptance:** AC-TG-04, AC-TG-05, AC-CAT-03 (via service), AC-ADM-02.
- **Required tests:** seller A on seller B's offer variant (`not_found`); stale `row_version`; expired token; token reuse; token belonging to another seller; invalid price/stock; unknown vs zero stock; audit rows.
- **Risks:** IDOR through token or offer IDs; trusting seller-supplied IDs.
- **Done when:** Standard DoD; security-sensitive: second-AI review.

### T-052 Telegram webhook and bot infrastructure
- **Objective:** Receive and answer Telegram updates safely.
- **Prerequisites:** T-050; D-08 Accepted; Telegram API facts checked (U7).
- **Scope:** TG-1 endpoint; secret-token verification; `telegram_updates_processed`; private-chat-only; unlinked-user generic reply; outbound client with timeout and bounded retries; Telegram calls fully mocked in tests; documented manual test procedure with a test bot and tunnel.
- **Non-goals:** flows, real production bot, real sellers.
- **Docs:** INTEGRATIONS, SECURITY, API-CONTRACT (TG-1).
- **Components:** webhook view, update dispatcher, Telegram client, migration.
- **Acceptance:** AC-TG-01, AC-TG-06, AC-TG-07, AC-TG-08.
- **Required tests:** missing/wrong secret -> 403 and no processing; duplicate `update_id`; unlinked sender; group chat ignored; Telegram API timeout path; outcome-unknown reporting.
- **Risks:** webhook reachability on the chosen host; token in logs.
- **Done when:** Standard DoD; Owner performs one manual test with a test bot (reported honestly).

### T-053 Bot flows: My offers, Update price, Update stock
- **Objective:** Guided conversational flows over SEL-1/SEL-2.
- **Prerequisites:** T-051, T-052.
- **Scope:** My offers (paginated), Update price, Update stock; preview/confirm/cancel; expiry; plain English messages; no customer data.
- **Non-goals:** new products, images, notifications.
- **Docs:** INTEGRATIONS (MVP commands), API-CONTRACT.
- **Components:** conversation handlers (thin), message formatting.
- **Acceptance:** AC-TG-04, AC-TG-05, AC-TG-08.
- **Required tests:** full flow with simulated updates; cancel; expired confirmation; double-tapped Confirm applies once; malformed callback data; message length bounds.
- **Risks:** business rules creeping into handlers; confusing UX for sellers (usability test in T-064).
- **Done when:** Standard DoD.

### T-054 Bot flow: Add product draft
- **Objective:** Seller submits a text-only draft for admin review.
- **Prerequisites:** T-052, T-035.
- **Scope:** SEL-3 guided steps, preview/confirm, idempotency key, duplicate-submission protection, status feedback to the seller on request ("My drafts" optional).
- **Non-goals:** images, direct publishing, notifications on approval.
- **Docs:** INTEGRATIONS, DATA-MODEL (product_drafts), ADR-0003.
- **Components:** wizard handlers, draft service call.
- **Acceptance:** AC-TG-09, AC-TG-06.
- **Required tests:** draft created as `pending`; replay creates no second draft; seller cannot set status or seller_id; payload validation (lengths, price bounds, allowed category); wizard abandonment and expiry.
- **Risks:** abusive or oversized input; Zawgyi text (U10).
- **Done when:** Standard DoD; Gate 5 review.
