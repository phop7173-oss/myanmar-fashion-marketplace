# Technology Stack

**Authoritative for:** chosen technologies, dependency policy, items needing external verification. Rationale and alternatives: [ADR-0005](decisions/0005-platform-baseline.md) (**Proposed**, pending D-01).

> Until the owner approves ADR-0005, **no dependency may be installed and no project scaffold created.**

## Recommended baseline (Option B)
| Area | Choice | Notes |
|------|--------|-------|
| Language | Python (current supported 3.x; version chosen and pinned in T-010) | One language for web, admin and bot |
| Web framework | Django | Built-in auth, admin, CSRF, ORM, migrations |
| Database | PostgreSQL | Same engine locally and in production |
| UI | Server-rendered templates, one small hand-written CSS file, minimal vanilla JavaScript only where required | No client framework, no Tailwind, no web fonts |
| Telegram | Webhook endpoint in the same app; plain HTTPS calls or a small maintained library chosen in T-052 | Polling only if D-08 says so |
| Images | Pillow | Processing at upload time |
| Tests | pytest (+ Django test support) | Browser end-to-end tests optional, added only if needed |
| Lint/format | ruff | One tool |
| Source control | Git + GitHub | |

Exact package versions are **not** fixed in documentation. T-010 selects current supported releases, records them in the committed lockfile, and states the choice in the task report.

## Alternative (Option A: original proposal)
Next.js (App Router), strict TypeScript, Tailwind, PostgreSQL, Sharp, Vitest, Playwright, separate Python bot worker. If chosen, update this file, [CODE-STYLE](CODE-STYLE.md) and task cards, and remove the unused Supabase variables from `.env.example` (see ADR-0005).

## Dependency policy
- Every new dependency (library, tool, GitHub Action, external service) needs owner approval via the plan step ([AI-WORKFLOW](AI-WORKFLOW.md)). The request states purpose, why existing/standard-library code is not enough, license, maintenance status, install size, and cost.
- Prefer widely used, actively maintained packages. Pin versions; commit the lockfile.
- No dependency that requires payment, a credit card, or an account at a third party without owner approval.
- Run the dependency vulnerability scan before each release ([SECURITY](SECURITY.md#dependencies)).

## UNVERIFIED items (must be checked from official sources before relying on them)
Do not fill these from memory. Record findings (with source link and date) in the ADR for D-02.

| # | Check | Why it matters |
|---|-------|----------------|
| U1 | Hosting free tier: terms allow a commercial/marketplace pilot? | Some free plans prohibit commercial use |
| U2 | Hosting free tier: sleeping/inactivity rules, memory/CPU limits, request time limits | Webhook must answer reliably |
| U3 | Database free tier: storage cap, connection limit, pausing on inactivity, built-in backups, export (`pg_dump`) access | Backup and restore requirement |
| U4 | Image/file storage: persistent disk or object storage, quota, transfer limits | Product photos |
| U5 | Can signup be completed from Myanmar (payment card/identity requirements, regional restrictions)? | May rule out candidates |
| U6 | Public HTTPS URL with valid certificate on a free subdomain; Telegram requires HTTPS for webhooks | Webhook mode |
| U7 | Telegram Bot API details used: secret-token header on webhooks, callback data size limit, rate limits | Bot design |
| U8 | Telegram reachable and usable by every pilot seller in Myanmar | Seller workflow |
| U9 | GitHub features for this repo (public/private): Actions minutes, Dependabot alerts, secret scanning/push protection | CI and security checks |
| U10 | Burmese (Unicode) text renders correctly on the pilot's low-end Android devices; Zawgyi-encoded input handling | Product text and search |
| U11 | Available PostgreSQL version on the chosen host | Feature compatibility |
| U12 | Domain name: free subdomain acceptable for the pilot? | Cost and trust |

Candidate hosting categories to examine in T-002 (no claims made here): free web-app platforms, free managed PostgreSQL, a free cloud VM, or the owner's own machine exposed through a free tunnel (lowest cost, lowest reliability).
