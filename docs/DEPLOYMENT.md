# Deployment, Backup and Recovery

**Authoritative for:** environments, configuration, release checks, backups, runbooks. Hosting is **not chosen** (D-02; proposal in [ADR-0007](decisions/0007-hosting.md)); nothing here claims any provider's terms ([TECH-STACK](TECH-STACK.md#unverified-items-must-be-checked-from-official-sources-before-relying-on-them)).

## Environments
- **Local (Ubuntu laptop):** development with synthetic data, local PostgreSQL, separate credentials.
- **Production:** real data only after the pre-production checklist ([SECURITY](SECURITY.md#pre-production-security-checklist)) passes.
- Optional preview environment only if free and verified.
- Termux is for documentation and Git synchronization only; application work happens on the laptop.

## Configuration
Environment variables only; names documented in `.env.example` with empty or placeholder values. The application validates required variables at startup and fails with a clear message that does not print secret values. Debug mode off, unique secret key, allowed hosts set, HTTPS enforced in production.

## Hosting selection (T-002)
Before choosing, record evidence for each UNVERIFIED item U1-U12 (source link + date) and answer: Does it allow a commercial pilot? Does it receive HTTPS webhooks? Can we run `pg_dump` and keep an off-site copy? Does the database pause or expire? Is signup possible from Myanmar? What happens when quotas are exceeded (stop vs bill)? Prefer options that **stop** rather than **bill**.

## Release checklist (human approves)
- [ ] CI checks pass (evidence in report).
- [ ] Migrations reviewed; tested on a fresh database and on a copy of production-like data.
- [ ] Backup taken immediately before release.
- [ ] Environment variables verified; no secrets in repository.
- [ ] Authorization tests pass.
- [ ] Critical flows exercised on the deployed site (browse, order, admin confirm, bot price update) with synthetic or test data.
- [ ] Rollback steps known.
- [ ] Owner approves.

## Backup and restore
- **Pilot targets (PROVISIONAL):** lose at most 24 hours of data; restore within 48 hours.
- Daily database dump (`pg_dump`), encrypted before leaving the server, stored off-site, plus a copy of uploaded images. Keep at least 7 daily and 4 weekly copies (adjust to storage limits). Encryption key stored separately from the backups.
- **Restore drill (T-062, then monthly during the pilot):** restore the latest backup into a scratch database, run row-count and sample-query checks, record results. A backup never restored is not a backup.
- Backups are personal data; apply SECURITY rules and retention.

## Rollback
- Keep the previous release deployable (tag releases in Git).
- Migrations follow expand-then-contract: add columns/tables first, remove old ones in a later release, so the previous code still works with the new schema.
- If a bad migration shipped: restore from the pre-release backup (accepting data loss since then) or ship a forward fix; the owner decides.

## Runbooks
Each runbook is written step by step and rehearsed once in T-063.

1. **Rotate a leaked secret:** revoke/regenerate at the source (e.g. bot token via Telegram's official bot tools), update the environment variable, redeploy, verify, search history for exposure, record the incident.
2. **Disable a compromised seller or bot access:** suspend the seller; revoke the Telegram link; rotate the bot token/webhook secret if the token is suspect; review audit logs for the period.
3. **Compromised admin account:** disable the account, rotate the secret key (invalidates sessions), review audit logs, reset credentials.
4. **Restore the database** (see above).
5. **Order reconciliation after a partial failure:** orders are created atomically, so a partial order should not exist; check recent audit logs and orders against admin's manual records, confirm stock values with sellers, correct through admin screens (audited).
6. **Site down:** check host status, application logs, database availability; roll back if a release caused it.

## Monitoring (minimum)
A free external uptime check on a health URL (UNVERIFIED availability), error logs reviewed daily during the pilot, and a weekly check that backups ran.
