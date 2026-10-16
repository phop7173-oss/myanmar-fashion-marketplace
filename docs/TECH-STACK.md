# Technology Stack

Proposed baseline:
- Next.js App Router
- TypeScript strict mode
- Tailwind CSS
- PostgreSQL; Supabase is a candidate
- Python Telegram bot as a separate worker
- Sharp for image processing
- Vitest for unit tests
- Playwright for browser tests
- Git and GitHub for source control

Inspect the repository before installing dependencies.
Do not invent package versions. Use compatible supported releases and commit the lockfile.

Before choosing hosting, verify current costs, quotas, backups, inactivity rules, storage limits, and persistent-worker support.

A Telegram polling bot needs a persistent process or a deliberately designed webhook architecture. Do not assume a short-lived serverless function can poll continuously.
