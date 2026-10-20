# ADR-0005: Platform baseline (technology, hosting, bot mode)
- Status: **Proposed** (needs owner approval: covers D-01, D-02, D-08)
- Date: 2026-10-20
- Decision owner: Project owner

## Context
The original docs proposed Next.js + TypeScript + Tailwind + Supabase (candidate) + a separate Python bot worker + Sharp. The owner is a beginner using AI tools, has a zero budget, and serves low-bandwidth users.

Concerns with the original proposal:
1. **Two languages** (TypeScript and Python) for a beginner to learn and review.
2. The bot as a **separate always-on worker** is hard to host for free and adds a second deployable.
3. `NEXT_PUBLIC_SUPABASE_ANON_KEY` in `.env.example` implies browser-to-database access, which contradicts ADR-0004.
4. The admin interface, authentication and CSRF protection would all be hand-built.
5. Tailwind and Sharp add a Node build toolchain; client-side React adds JavaScript weight for slow networks.
6. Free-tier terms (commercial use, inactivity pausing, backups) of the candidate hosts are not verified.

## Decision (recommended; Option B)
**Option B (recommended): one Python web application using Django**
- PostgreSQL database.
- Server-rendered HTML templates, one small hand-written CSS file, almost no JavaScript.
- Django's built-in admin for the admin website (customized as needed), built-in authentication, CSRF protection, ORM (parameterized queries) and migrations.
- Telegram bot as a **webhook endpoint inside the same application**, calling the same service layer (no second process, no duplicated rules).
- Pillow for image processing.
- pytest for tests; ruff for lint/format.
- Hosting: not chosen. See T-002 and [TECH-STACK](../TECH-STACK.md).

**Option A (original proposal): Next.js + TypeScript + Tailwind + PostgreSQL + separate Python bot.** Still viable. If the owner prefers A: keep Option B's rules on data, security and workflow; replace the stack-specific parts of TECH-STACK.md, CODE-STYLE.md and the tool names in task cards; the bot calls authenticated HTTP endpoints; drop the Supabase anon key unless Row Level Security is deliberately designed.

## Alternatives considered
- Other Python/Node frameworks: no advantage over Django for this scope; Django has the most built-in security and admin functionality.
- Separate frontend (SPA) + API: more code, more JavaScript, more duplication. Rejected for the MVP.
- Polling bot: needs an always-on process. Webhook preferred (D-08); polling only if the chosen host cannot receive HTTPS webhooks.

## Consequences
- One language, one deployable, one test runner. The admin site and login come mostly for free.
- Django admin is less flexible than a custom UI; acceptable for a few admins.
- Webhook mode requires the app to be publicly reachable over HTTPS (UNVERIFIED on each candidate host).
- Reversing this decision after T-010 is expensive.

## Revisit triggers
Chosen host cannot run Django or receive webhooks; admin workflows outgrow Django admin; the owner's learning goals favor JavaScript.
