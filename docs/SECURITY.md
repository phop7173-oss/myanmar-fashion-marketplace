# Security and Privacy Requirements

**Authoritative for:** authentication, authorization, input handling, secrets, privacy, audit. Written assuming an inexperienced developer and an AI agent could introduce a serious vulnerability by accident. **Markdown does not enforce security; code, database constraints and tests do.**

## Always on the server
These must never rely on browser or Telegram checks: authentication; authorization and ownership; price and total calculation; stock checks and changes; status transitions; validation of every field; rate limiting; upload validation; audit logging; idempotency.

## Permission matrix
| Action | Visitor | Linked seller (Telegram) | Admin |
|--------|:------:|:------------------------:|:-----:|
| View published catalog | yes | yes | yes |
| Submit order | yes | yes | yes |
| View orders / customer data | no | **no** | yes |
| Change own offer price/stock | no | yes (own only) | yes |
| Change another seller's offer | no | **no** | yes |
| Create/publish products, variants | no | no (drafts only) | yes |
| Upload images, confirm permission | no | no | yes |
| Approve sellers, issue link codes | no | no | yes |
| Review drafts | no | no | yes |
| Read audit logs | no | no | yes |

A role check exists in the service operation for every row marked "no". Tests cover each ([ACCEPTANCE-TESTS](ACCEPTANCE-TESTS.md)).

## Authentication
- Admin: the framework's maintained authentication; no hand-written password, session or token code. Strong password policy; session cookies `Secure`, `HttpOnly`, `SameSite=Lax`; login rate limit; admin login failures audited. Multi-factor authentication before real customers if the stack supports it (UNVERIFIED).
- First admin created from the command line only (ADM-8). No default credentials in code, docs or seed data.
- Seller identity: numeric Telegram user ID linked via admin-issued single-use code ([INTEGRATIONS](INTEGRATIONS.md)). Usernames, display names and button callbacks are **not** identity.
- Customers have no accounts in the MVP.

## Authorization
- Default deny. Each operation states who may call it ([API-CONTRACT](API-CONTRACT.md)).
- Every supplied ID is checked for ownership/visibility. Cross-seller access returns `not_found`.
- Admin routes are protected by one central mechanism; a test enumerates all admin URLs and asserts anonymous and non-admin callers are denied.

## Input, injection, XSS, CSRF
- Validate type, length, range and format at the boundary; reject unknown fields.
- SQL: use the ORM/parameterized queries only. Raw SQL, string-built queries, shell execution, `eval`, unsafe deserialization, and marking text as "safe HTML" need explicit owner approval in the plan.
- XSS: all seller/customer/admin text is escaped on output (template auto-escaping stays on). Telegram messages are sent as plain text or escaped.
- Add a restrictive Content-Security-Policy and standard headers (`X-Content-Type-Options: nosniff`, frame protection, referrer policy). No third-party scripts, fonts or trackers.
- CSRF: every state-changing browser form carries a CSRF token. The Telegram webhook is exempt from CSRF **only because** it is authenticated by the secret-token header.
- User-facing errors never expose internals.

## Rate limiting and abuse
Limits apply on the server, per IP and per relevant key. Starting values (PROVISIONAL, tune with evidence): order submission 5/hour per IP and 3/hour per phone number; admin login 5 failed attempts per 15 minutes per account+IP; bot messages 30/minute per Telegram ID. The order form also has a hidden honeypot field. No CAPTCHA (third-party script weight). Behind a proxy, the client IP source must be configured deliberately, or limits can be bypassed or can block everyone (verify in T-041).

## Uploads (admin only in the MVP, D-06)
- Allow JPEG, PNG, WebP only; **no SVG**. Maximum file size (default 5 MB) and maximum pixel dimensions (default 4000 x 4000), PROVISIONAL.
- Decode the file with the image library to verify it is a real image; never trust the extension or declared content type.
- Re-encode into generated derivatives; strip metadata (EXIF/GPS). Store under generated names (never the user's file name), outside any executable path, served with correct content types and `nosniff`.
- Record source and permission per image; an image is not public until permission is confirmed ([DATA-MODEL](DATA-MODEL.md#product_images-t-025)).

## Secrets
- Never commit, print, log, or paste into AI prompts: bot tokens, webhook secrets, database passwords, secret keys, real customer data.
- `.env*` is git-ignored; `.env.example` holds names and empty/placeholder values only.
- Secrets reach the application only through environment variables validated at startup; never in client-side code or templates.
- Separate credentials for development and production.
- If a secret leaks: rotate it immediately, assume it is compromised, then clean history ([DEPLOYMENT](DEPLOYMENT.md#runbooks)).

## Personal data
- **Inventory:** customer name, phone, optional contact channel, address, township, region, note (orders only). Seller internal notes. Telegram numeric IDs.
- **Minimize:** collect only what fulfillment needs. Do not send customer personal data through Telegram (MVP).
- **Access:** admins only. Never in logs, error messages, audit `before/after`, or URLs.
- **Retention (D-05, PROVISIONAL default):** erase or anonymize order personal fields 12 months after completion/cancellation (`personal_data_erased_at`); keep order totals/snapshots. A documented manual procedure is sufficient for the pilot.
- **Privacy notice:** shown at checkout before real customers (T-064). Legal review: D-09.
- Development and tests use synthetic data only.

## Audit and logging
Audit sensitive changes ([DATA-MODEL](DATA-MODEL.md#audit_logs-t-031)). Application logs: request ID, route, status, timing; no tokens, no passwords, no full phone numbers or addresses.

## Dependencies
Pin and commit lockfile. Run the ecosystem's vulnerability audit in CI or before each release and record the result. Update vulnerable dependencies deliberately, with tests. See [TECH-STACK](TECH-STACK.md#dependency-policy).

## Backups
Backups contain personal data: encrypt before leaving the server, store off-site, restrict access, test restores ([DEPLOYMENT](DEPLOYMENT.md#backup-and-restore)).

## Pre-production security checklist
All must be evidenced (command output or screenshot noted in the task report) before real customers:
- [ ] Authorization tests for the permission matrix pass.
- [ ] Anonymous/non-admin access to every admin URL is denied (enumerating test).
- [ ] Cross-seller access test passes (SEL-1, SEL-2).
- [ ] Webhook rejects missing/wrong secret token.
- [ ] Order tampering (price, seller, total, status) test passes.
- [ ] Upload tests (wrong type, oversize, disguised file, huge dimensions) pass.
- [ ] Secret scan of the repository history shows no secrets; `.env` not tracked.
- [ ] Debug mode off; secret key unique; allowed hosts set; HTTPS enforced.
- [ ] Security headers verified on the deployed site.
- [ ] Dependency audit run; no unaddressed high/critical findings.
- [ ] Rate limits verified through the real proxy path.
- [ ] Backup restored successfully to a scratch database.
- [ ] Privacy notice and retention procedure in place (D-05).
