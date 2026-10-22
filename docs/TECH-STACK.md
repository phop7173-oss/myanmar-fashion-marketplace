# Technology Stack

**Authoritative for:** chosen technologies, dependency policy, items needing external verification. Rationale and alternatives: [ADR-0005](decisions/0005-platform-baseline.md) (**Accepted** for D-01 and D-08; hosting D-02 still open).

> ADR-0005 is Accepted, but **no dependency is installed and no scaffold is created until task T-010 starts with an Owner-approved plan** (AGENTS.md R8).

## Chosen baseline (Option B, accepted)
| Area | Choice | Notes |
|------|--------|-------|
| Language | Python (current supported 3.x; version chosen and pinned in T-010) | One language for web, admin and bot |
| Web framework | Django | Built-in auth, admin, CSRF, ORM, migrations |
| Database | PostgreSQL | Same engine locally and in production |
| UI | Server-rendered templates, one small hand-written CSS file, minimal vanilla JavaScript only where required | No client framework, no Tailwind, no web fonts |
| Telegram | Webhook endpoint in the same app; plain HTTPS calls or a small maintained library chosen in T-052 | Webhook mode accepted (D-08); polling only if the chosen host cannot receive webhooks |
| Images | Pillow | Processing at upload time |
| Tests | pytest (+ Django test support) | Browser end-to-end tests optional, added only if needed |
| Lint/format | ruff | One tool |
| Source control | Git + GitHub | |

Exact package versions are **not** fixed in documentation. T-010 selects current supported releases, records them in the committed lockfile, and states the choice in the task report.

## Not chosen (Option A: original proposal)
Next.js (App Router), strict TypeScript, Tailwind, PostgreSQL, Sharp, Vitest, Playwright, separate Python bot worker. If ever revisited, update this file, [CODE-STYLE](CODE-STYLE.md) and task cards, and remove the unused Supabase variables from `.env.example` (see ADR-0005).

## Dependency policy
- Every new dependency (library, tool, GitHub Action, external service) needs owner approval via the plan step ([AI-WORKFLOW](AI-WORKFLOW.md)). The request states purpose, why existing/standard-library code is not enough, license, maintenance status, install size, and cost.
- Prefer widely used, actively maintained packages. Pin versions; commit the lockfile.
- No dependency that requires payment, a credit card, or an account at a third party without owner approval.
- Run the dependency vulnerability scan before each release ([SECURITY](SECURITY.md#dependencies)).

## UNVERIFIED items (must be checked from official sources before relying on them)
Status after T-002 (read 2026-10-20). **Verified** = stated by the provider's or Telegram's own documentation (or text quoted from it); **Partly** = some parts confirmed; **UNVERIFIED** = not confirmed, with the reason. "Third-party" means a blog or comparison site, not the provider; treat as a lead, not proof. Terms change: re-check at T-063. Hosting decision proposal: [ADR-0007](decisions/0007-hosting.md).

| # | Check | Status | Finding and source |
|---|-------|--------|--------------------|
| U1 | Free tier allows a commercial/marketplace pilot? | Partly | **Vercel Hobby: NO**, restricted to non-commercial personal use ([fair use guidelines](https://vercel.com/docs/limits/fair-use-guidelines)). **Render, Neon, Oracle Always Free: UNVERIFIED**, no explicit commercial-use statement found in what was retrieved; Render's own page describes the free tier as a preview of the platform ([render.com/docs/free](https://render.com/docs/free)); read each provider's terms. GitHub public repo: no issue found |
| U2 | Hosting sleeping rules, limits, request time | Partly | **Render free web service:** spins down after 15 minutes without inbound traffic; filesystem changes lost on restart/redeploy/spin-down; may restart at any time; monthly free instance-hour limit exists, suspended when used up ([render.com/docs/free](https://render.com/docs/free); wake-up about 1 minute per [Render article](https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026.md)). Telegram retry behavior when the webhook is slow: UNVERIFIED. **Oracle:** VM is always on; idle-reclaim rule UNVERIFIED (official page says Always Free resources are not reclaimed after the trial ends; third-party sources say idle instances can be reclaimed; read Oracle's current policy) |
| U3 | Database free tier: storage, pausing, backups, `pg_dump` | Partly | **Neon free:** 0.5 GB per project, 100 CU-hours/month, scale to zero after 5 minutes (cannot be disabled), no expiry, writes fail at the storage cap ([Neon limits](https://neon.com/faqs/free-plan-limits-and-quotas), [Neon cost docs](https://neon.com/docs/introduction/cost-optimization)). **Render free Postgres:** 1 GB, **expires after 30 days, no backups of any kind** ([render.com/docs/free](https://render.com/docs/free)). Neon backup/restore window on Free, connection limit, and an actual `pg_dump` run: UNVERIFIED. **Koyeb free Postgres:** a few compute-hours per month (third-party, conflicting) |
| U4 | Image/file storage | Partly | Render free: storage is **not persistent** (above). Oracle VM: persistent disk; sizes UNVERIFIED from official text (third-party says 200 GB block total). Cloudflare R2 free tier: 10 GB-month, 1M Class A and 10M Class B operations, free egress ([Cloudflare R2 docs](https://developers.cloudflare.com:8443/r2/llms-full.txt)); whether signup needs a payment method and whether overage bills (instead of stopping): UNVERIFIED (third-party says a payment method is requested) |
| U5 | Signup possible from Myanmar? | UNVERIFIED | **Oracle:** needs mobile number and a credit/debit card; virtual, single-use, prepaid and PIN debit cards not accepted ([Oracle FAQ](https://www.oracle.com/cloud/free/faq/), [Oracle docs](https://docs.oracle.com/iaas/Content/FreeTier/freetier.htm)). Oracle says Free Tier is available where commercial OCI is available; Myanmar eligibility was not found. Render, Neon: no regional statement found. **Owner must test** (ADR-0007 check A-B) |
| U6 | Public HTTPS URL with valid certificate; Telegram needs HTTPS | Partly | Telegram webhook URL must be HTTPS on port 443, 80, 88 or 8443 ([Bot API setWebhook](https://core.telegram.org/bots/api#setwebhook), text quoted by [aiogram docs](https://docs.aiogram.dev/en/latest/_modules/aiogram/methods/set_webhook.html)). Render provides an onrender.com URL with managed TLS ([Render article](https://render.com/articles/platforms-with-a-real-free-tier-for-developers-in-2026.md)). Oracle VM: you must set up HTTPS yourself; a free domain name for it is UNVERIFIED. Cloudflare quick tunnels give a random URL for testing only and no uptime guarantee; a stable named tunnel needs your own domain ([Cloudflare docs](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/index.md)) |
| U7 | Telegram Bot API details | Partly | Webhook `secret_token` is 1-256 characters and sent in the `X-Telegram-Bot-Api-Secret-Token` header (same aiogram quote of the official text). `callback_data` is 1-64 bytes of UTF-8 (third-party library docs). Rate limits: UNVERIFIED. Re-read core.telegram.org at T-052 |
| U8 | Telegram usable by every pilot seller in Myanmar | UNVERIFIED | No source found either way. **Owner test on the sellers' real phones and networks** (ADR-0007 check C) |
| U9 | GitHub features for this repo | Partly | GitHub Actions is free on standard runners in public repositories; Dependabot alerts included in GitHub Free ([GitHub plans](https://docs.github.com/en/enterprise-server@latest/get-started/learning-about-github/githubs-plans)). Secret scanning and push protection for public repos: UNVERIFIED (not stated in the text retrieved). The repository is **public**: never commit secrets or real data |
| U10 | Burmese (Unicode) rendering on low-end Android; Zawgyi input | UNVERIFIED | Not researched in T-002. Owner device test (ADR-0007 check D) |
| U11 | Available PostgreSQL version on the host | UNVERIFIED | Not found for any candidate; on an Oracle VM you choose the version yourself. Check at T-012 |
| U12 | Free subdomain acceptable for the pilot | UNVERIFIED | Render offers an onrender.com subdomain. Whether customers and sellers trust it is an Owner judgment. A stable domain of your own costs money |

Candidate hosting categories to examine in T-002 (no claims made here): free web-app platforms, free managed PostgreSQL, a free cloud VM, or the owner's own machine exposed through a free tunnel (lowest cost, lowest reliability).
