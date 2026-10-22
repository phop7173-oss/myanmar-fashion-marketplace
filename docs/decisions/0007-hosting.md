# ADR-0007: Hosting and database (D-02)
- Status: **Proposed** (needs Owner approval and Owner-side checks listed below)
- Date: 2026-10-20 (facts below were read on this date and can change; re-check in T-063)
- Decision owner: Project owner

## Context
ADR-0005 fixed the stack (Django, PostgreSQL, Telegram webhook in the same app) but left hosting open (D-02). Requirements from [DEPLOYMENT](../DEPLOYMENT.md): zero cost, commercial pilot allowed, public HTTPS URL for the Telegram webhook, persistent database and uploaded images, `pg_dump` plus an off-site copy, and a provider that **stops** rather than **bills** when a quota is exceeded.

Evidence for every candidate is in the U1-U12 table in [TECH-STACK](../TECH-STACK.md#unverified-items-must-be-checked-from-official-sources-before-relying-on-them). This ADR only summarizes it.

## Findings in one paragraph
**No candidate was verified to satisfy every requirement.** Two cannot be used at all (terms), several fail on persistence or cost, and the two best technical fits each depend on something only the Owner can check (signup from Myanmar).

## Candidate assessment
| Candidate | Result | Main reason (source in TECH-STACK) |
|-----------|--------|------------------------------------|
| Vercel Hobby | **Rejected** | Official fair-use guidelines restrict Hobby to non-commercial personal use |
| Fly.io | **Rejected** | No free tier for new organizations; credit card required after a short trial (third-party sources; official page not retrieved) |
| PythonAnywhere free | **Rejected** | Outbound internet limited to an allowlist; `api.telegram.org` is not in the official list retrieved, so the bot cannot reply; paid plan needed |
| Cloudflare quick tunnel / own laptop | **Rejected for pilot** | Cloudflare says quick tunnels are for testing only (random URL, no uptime guarantee); a stable named tunnel needs a domain the Owner owns (cost) |
| Koyeb free | **Rejected** | Sources conflict on the card requirement; free instance is 0.1 vCPU and the free database allows only a few compute-hours per month |
| Render free web service | **Fallback, demo only** | Spins down after 15 minutes idle; filesystem is wiped on restart (uploaded images lost); free Postgres expires after 30 days and has no backups |
| Neon free Postgres | **Usable as database** | Does not expire; 0.5 GB cap; writes fail at the cap instead of billing; compute sleeps after 5 minutes (cold start). Commercial-use terms UNVERIFIED |
| Oracle Cloud Always Free VM | **Primary candidate (conditional)** | Always-on VM that can run Django and PostgreSQL together, so no external database and a real disk for images. Needs a credit/debit card (virtual and prepaid not accepted); Myanmar eligibility UNVERIFIED; idle-reclaim policy sources conflict; ARM capacity may be unavailable |

## Proposed decision
1. **Primary: one Oracle Cloud Always Free VM** running the Django app, PostgreSQL, and a reverse proxy with HTTPS, with encrypted backups copied off the VM. **Conditional on the Owner confirming checks A-D below.** Without a domain name there is no certificate; a free DNS name has not been verified (U6, U12).
2. **Fallback (pre-pilot demo and webhook testing only, not real customers): Render free web service + Neon free Postgres.** Known gaps: ~1 minute wake-up after idle (effect on Telegram webhook delivery UNVERIFIED), images are lost on restart so product photos need a separate decision (for example object storage, whose free tier needs a payment method and may bill on overage, or a size-limited approach reviewed in a new ADR), and Render's commercial-use terms are UNVERIFIED.
3. **If neither can be used from Myanmar:** a zero-budget pilot with real customers is **not currently supported by verified evidence**. The Owner then chooses between (a) a small paid plan (cost to be verified at that time), (b) an always-on machine plus a domain, or (c) delaying the pilot. AI cannot make this choice.

## Owner-side checks (AI cannot do these)
- **A.** Open the Oracle signup page, select Myanmar, and see whether signup proceeds and which cards are accepted. Do not enter payment details until you decide to proceed (T-002 non-goal: no payment signups).
- **B.** Confirm you hold an accepted card, and read Oracle's current Always Free idle-reclaim rule.
- **C.** From the phones and networks the pilot sellers will use, confirm Telegram works and that `https://api.telegram.org` is reachable.
- **D.** Check that Burmese (Unicode) text displays correctly on a low-end Android phone (U10).

## Alternatives considered
See the table above. Moving the database to Neon while keeping the app on Oracle was not recommended because it adds a second provider and a cold-start delay for no benefit when the VM can host PostgreSQL.

## Consequences
- Running your own VM means you are responsible for operating system updates, firewall, HTTPS renewal and backups (see [SECURITY](../SECURITY.md), [DEPLOYMENT](../DEPLOYMENT.md)). This is more work than a managed platform.
- Webhook mode (ADR-0005) is feasible on a VM or on Render, subject to U6.
- If this ADR is accepted, T-063 and T-013 will be written for the chosen host.

## Revisit triggers
Any provider changes its free terms; the Owner cannot complete checks A-D; the pilot needs more than one VM; real customer data is about to be stored (re-verify all terms, per T-063).
