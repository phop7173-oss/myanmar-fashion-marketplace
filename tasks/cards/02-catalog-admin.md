# Cards: Phase 2 Catalog and Phase 3 Admin

"Standard DoD" = [Definition of Done](../../docs/AI-WORKFLOW.md#definition-of-done-standard-task-cards-add-to-it). Components are named generically; paths are in [ARCHITECTURE](../../docs/ARCHITECTURE.md) after T-010.

## Phase 2: Catalog (read-only public site)

### T-020 Catalog schema and constraints
- **Objective:** Database tables and constraints for sellers, products, product variants, seller offers, offer variants.
- **Prerequisites:** T-012; D-07 category list confirmed.
- **Scope:** migrations exactly per [DATA-MODEL](../../docs/DATA-MODEL.md) for these five tables, including composite foreign keys, checks, uniques, indexes, restrict-on-delete.
- **Non-goals:** images, drafts, orders, UI, seed data, admin screens.
- **Docs:** DATA-MODEL, ADR-0001, ACCEPTANCE-TESTS.
- **Components:** migrations, models, constraint tests.
- **Acceptance:** AC-CAT-02, AC-CAT-03, AC-CAT-08.
- **Required tests:** each constraint rejects its bad case (price 0/negative, negative stock, duplicate offer, duplicate variant, cross-product variant, delete of referenced row); valid rows accepted.
- **Risks:** getting composite keys wrong; schema drift from DATA-MODEL (report any deviation and ask).
- **Done when:** Standard DoD; migration runs on a fresh database.

### T-021 Synthetic seed data
- **Objective:** Repeatable fake catalog for development and tests.
- **Prerequisites:** T-020.
- **Scope:** a seed command creating about 30 fake products, variants, 3 fake sellers, offers and offer variants, including edge cases (unknown stock, zero stock, stale dates, paused offer, unpublished product, suspended seller); refuses to run when the environment is production.
- **Non-goals:** images, real names, real data.
- **Docs:** DATA-MODEL (Visibility rules), TESTING.
- **Components:** seed command, tests.
- **Acceptance:** idempotent re-run behavior documented; production guard works.
- **Required tests:** seed runs; production guard test; counts of edge cases.
- **Risks:** fake data looking like real people/businesses; keep obviously fictional.
- **Done when:** Standard DoD.

### T-022 Public product listing
- **Objective:** Server-rendered, mobile-first, paginated product list.
- **Prerequisites:** T-021.
- **Scope:** CAT-1 without search; visibility rules; "from price"; stale labels; pagination (default 20, max 50); minimal CSS; no JavaScript required.
- **Non-goals:** search, images, product detail, caching.
- **Docs:** API-CONTRACT (CAT-1), DATA-MODEL (Visibility), PERFORMANCE.
- **Components:** listing view, service operation, template, CSS.
- **Acceptance:** AC-CAT-01, AC-CAT-04, AC-CAT-05, AC-CAT-06, AC-PERF-02.
- **Required tests:** visibility matrix; pagination cap; deterministic order; query-count assertion; stale label.
- **Risks:** N+1 queries; business rules leaking into the template.
- **Done when:** Standard DoD; manual check in a phone-sized browser.

### T-023 Public product detail
- **Objective:** Product page with variants and each seller's price/stock/freshness.
- **Prerequisites:** T-022.
- **Scope:** CAT-2; unavailable state; unknown vs sold-out display.
- **Non-goals:** order button behavior (added in T-042), images.
- **Docs:** API-CONTRACT (CAT-2), DATA-MODEL.
- **Components:** detail view, service, template.
- **Acceptance:** AC-CAT-01, AC-CAT-05, AC-CAT-06, AC-SEC-05 (escaping).
- **Required tests:** unpublished product returns not found; hidden offers not shown; script text in seller-controlled fields is escaped.
- **Risks:** leaking `internal_note` or suspended sellers.
- **Done when:** Standard DoD.

### T-024 Search and category filter
- **Objective:** Basic search by title/brand and category filter.
- **Prerequisites:** T-022.
- **Scope:** CAT-1 `q` and `category`; Unicode normalization; length limit; parameterized queries; `EXPLAIN` on 1,000 synthetic products; add an index only if evidence supports it.
- **Non-goals:** relevance ranking, external search engine, Burmese word segmentation.
- **Docs:** API-CONTRACT, DATA-MODEL (Indexes), PERFORMANCE.
- **Components:** search service function, form, tests.
- **Acceptance:** AC-CAT-07, AC-CAT-04.
- **Required tests:** injection-like and very long input; unpublished never returned; empty/odd Unicode input.
- **Risks:** slow queries at scale; plan evidence required.
- **Done when:** Standard DoD with `EXPLAIN` output recorded.

### T-025 Image processing service
- **Objective:** Safe image validation and derivative generation (service only, no UI).
- **Prerequisites:** T-020; D-06 resolved.
- **Scope:** `product_images` migration; validate/decode, size and dimension limits, strip metadata, generate derivatives with generated names, store via a storage setting; permission fields.
- **Non-goals:** upload screens, seller uploads, CDN.
- **Docs:** SECURITY (Uploads), DATA-MODEL (product_images), PERFORMANCE.
- **Components:** image service, migration, tests with synthetic images.
- **Acceptance:** AC-IMG-01, AC-IMG-02, AC-IMG-03 (data-level).
- **Required tests:** wrong type, disguised file (wrong content), oversize bytes, oversize dimensions, valid image; derivative sizes within PERFORMANCE targets; stored name is generated.
- **Risks:** decompression bombs; storage location unknown until T-002 (use a storage setting).
- **Done when:** Standard DoD.

### T-026 Images on catalog pages
- **Objective:** Show derivatives responsibly in listing and detail.
- **Prerequisites:** T-023, T-025.
- **Scope:** responsive images with width/height, lazy-loading below the fold, public only when permission confirmed; seed with synthetic placeholder images created by the project.
- **Non-goals:** real photos, zoom/gallery scripts.
- **Docs:** PERFORMANCE, DATA-MODEL (Visibility).
- **Components:** templates, image selection logic.
- **Acceptance:** AC-IMG-03, AC-IMG-04, AC-CAT-01.
- **Required tests:** unconfirmed image never rendered; grid never references originals; dimensions present.
- **Risks:** layout shift; page weight over budget (measured in T-061).
- **Done when:** Standard DoD; Gate 2 review.

## Phase 3: Admin

### T-030 Admin authentication and role enforcement
- **Objective:** Admin login using the framework's maintained authentication; central admin protection.
- **Prerequisites:** Gate 2.
- **Scope:** admin site enabled; first admin created by command line only; session cookie settings; login rate limit; everything admin requires `is_admin`.
- **Non-goals:** seller web login, customer accounts, MFA (record UNVERIFIED availability).
- **Docs:** SECURITY (Authentication, Authorization), API-CONTRACT (ADM-8).
- **Components:** auth settings, admin site configuration, create-admin command.
- **Acceptance:** AC-ADM-01, AC-ADM-03, AC-SEC-04.
- **Required tests:** an enumerating test over all admin URLs for anonymous and non-admin users; login rate limit; cookie flags.
- **Risks:** default admin URL exposure; weak passwords; custom auth code (forbidden).
- **Done when:** Standard DoD; security-sensitive: second-AI review.

### T-031 Audit log service
- **Objective:** Append-only audit recording usable by later tasks.
- **Prerequisites:** T-030.
- **Scope:** `audit_logs` migration; one service function to record; sanitizer excluding sensitive fields; production-role note in DEPLOYMENT.
- **Non-goals:** audit viewer beyond a read-only admin list.
- **Docs:** DATA-MODEL (audit_logs), SECURITY.
- **Components:** audit service, migration, read-only admin list.
- **Acceptance:** AC-ADM-02 (foundation).
- **Required tests:** record creation; no update/delete path in code; sensitive keys rejected or stripped.
- **Risks:** PII leaking into `before/after`.
- **Done when:** Standard DoD.

### T-032 Admin: products and variants
- **Objective:** Admin creates, edits, publishes and archives products and variants.
- **Prerequisites:** T-031.
- **Scope:** ADM-1; normalized title; duplicate warning; no hard delete; audit on publish/archive/edit.
- **Non-goals:** images, offers, drafts.
- **Docs:** API-CONTRACT (ADM-1), DATA-MODEL.
- **Components:** admin configuration, services, tests.
- **Acceptance:** AC-ADM-02, AC-ADM-05, AC-CAT-08.
- **Required tests:** non-admin denied; duplicate warning; archive instead of delete; audit rows written.
- **Risks:** admin screens bypassing the service layer (rules must stay in services).
- **Done when:** Standard DoD.

### T-033 Admin: image upload and permission
- **Objective:** Upload images and record source/permission.
- **Prerequisites:** T-032, T-025, D-06.
- **Scope:** ADM-2 using the T-025 service; source and permission recording; confirmation audited.
- **Non-goals:** seller uploads, bulk import.
- **Docs:** SECURITY (Uploads), DATA-MODEL.
- **Components:** admin upload form, service calls.
- **Acceptance:** AC-IMG-01..03, AC-ADM-02.
- **Required tests:** rejected uploads via the admin form; permission required before public; audit rows.
- **Risks:** large uploads on a free host; limits from T-002.
- **Done when:** Standard DoD.

### T-034 Admin: sellers, offers, offer variants
- **Objective:** Admin approves sellers and manages offers and offer variants.
- **Prerequisites:** T-032.
- **Scope:** ADM-3, ADM-4; `row_version` handling; `price_confirmed_at`/`stock_confirmed_at` updates; audit.
- **Non-goals:** Telegram, drafts.
- **Docs:** API-CONTRACT, DATA-MODEL.
- **Components:** admin configuration, services.
- **Acceptance:** AC-CAT-03 (via admin), AC-ADM-02.
- **Required tests:** conflicting concurrent edit rejected; invalid price/stock rejected; cross-product variant rejected; suspended seller's offers disappear from the public site.
- **Risks:** admin forms offering invalid combinations (database constraint is the backstop).
- **Done when:** Standard DoD.

### T-035 Admin: draft review queue
- **Objective:** Review seller-submitted drafts.
- **Prerequisites:** T-034.
- **Scope:** `product_drafts` migration; ADM-5; atomic approval creating product/variants/offer/offer variants; reject with note; duplicate warning; draft payload validation schema.
- **Non-goals:** bot submission (T-054); drafts are created by test fixtures here.
- **Docs:** DATA-MODEL (product_drafts), ADR-0003.
- **Components:** migration, review services, admin screen.
- **Acceptance:** AC-ADM-04, AC-ADM-05, AC-TG-09 (admin side).
- **Required tests:** approval atomicity (failure leaves nothing partial); reject path; idempotent approve; non-admin denied.
- **Risks:** unvalidated JSON payload; Zawgyi text in submissions (admin visually checks; U10).
- **Done when:** Standard DoD; Gate 3 review.
