# Cards: Phase 6 Pilot Readiness

"Standard DoD" = [Definition of Done](../../docs/AI-WORKFLOW.md#definition-of-done-standard-task-cards-add-to-it). Tasks here involve the Owner directly; AI helps with checklists, scripts and documentation but cannot verify the real world.

### T-060 Security review and hardening
- **Objective:** Independent review of the whole system against SECURITY.
- **Prerequisites:** T-043, T-053, T-054.
- **Scope:** walk the pre-production checklist; run dependency audit; secret scan of full history; headers; authorization matrix tests; review by a fresh AI session plus Owner reading of findings; fix critical/high issues in small follow-up tasks.
- **Non-goals:** new features, penetration testing by third parties.
- **Docs:** SECURITY, ACCEPTANCE-TESTS (AC-SEC).
- **Components:** tests, configuration fixes.
- **Acceptance:** AC-SEC-01..06 with evidence; checklist items each marked with evidence or open issue.
- **Required tests:** full suite; header check; secret-scan output; dependency audit output.
- **Risks:** checklist ticked without evidence (not allowed).
- **Done when:** Standard DoD; Owner reviews findings list.

### T-061 Performance measurement
- **Objective:** Replace provisional budgets with measured numbers.
- **Prerequisites:** T-026, T-042.
- **Scope:** throttled-network and CPU-throttled measurements of listing, detail, order form; query plans at about 1,000 synthetic products; real low-end phone test if available; update PERFORMANCE.md.
- **Non-goals:** infrastructure changes beyond what findings require.
- **Docs:** PERFORMANCE, TESTING (manual checklist).
- **Components:** measurement notes, fixes.
- **Acceptance:** AC-PERF-01, AC-PERF-02; deviations explained or fixed.
- **Required tests:** query-count assertions; recorded measurements.
- **Risks:** local measurements differ from production host (repeat after T-063).
- **Done when:** Standard DoD.

### T-062 Backup and restore drill
- **Objective:** Prove backups restore.
- **Prerequisites:** T-054.
- **Scope:** documented backup script/procedure (dump, encrypt, copy off-site), restore to a scratch database, verification checks, records.
- **Non-goals:** automation on production (T-063).
- **Docs:** DEPLOYMENT (Backup and restore), SECURITY (Backups).
- **Components:** backup/restore scripts or documented commands.
- **Acceptance:** AC-OPS-01 with recorded commands, outputs, row counts.
- **Required tests:** restore verification (row counts, sample queries, constraint sanity).
- **Risks:** unencrypted backups; key lost with the backup.
- **Done when:** Standard DoD; Owner repeats the restore once.

### T-063 Production deployment and runbooks
- **Objective:** Deploy to the verified host and rehearse recovery.
- **Prerequisites:** T-060, T-061, T-062, T-002.
- **Scope:** production environment per DEPLOYMENT; HTTPS; environment variables set by the Owner; migrations; webhook registration with the real bot (Owner); health URL and uptime check; scheduled backups; rehearse rollback and the runbooks.
- **Non-goals:** real customer data before T-064.
- **Docs:** DEPLOYMENT, INTEGRATIONS, SECURITY.
- **Components:** deployment configuration, runbook documents.
- **Acceptance:** AC-OPS-02, AC-OPS-03, AC-SEC-03 on the deployed site; critical flows work with test data.
- **Required tests:** post-deploy smoke checks performed by a human, evidence recorded.
- **Risks:** free-tier changes since T-002 (re-verify); AI cannot confirm deployment success without evidence (R23).
- **Done when:** Standard DoD; Owner approves release.

### T-064 Pilot readiness and protocol
- **Objective:** Go/no-go for a small real pilot.
- **Prerequisites:** T-063; D-04, D-05, D-09 resolved.
- **Scope:** privacy notice and retention procedure; seller guide for the Telegram bot (English, step by step); verify each pilot seller can use Telegram (U8); image permissions for every real product image; admin order-handling procedure; metrics collection method from PROJECT.md; stop criteria and rollback; go/no-go checklist.
- **Non-goals:** new features, marketing.
- **Docs:** PROJECT, SECURITY (Personal data), DEPLOYMENT, INTEGRATIONS.
- **Components:** documents and checklists.
- **Acceptance:** every checklist line has evidence; Owner signs go/no-go.
- **Required tests:** a dry-run of the full order flow with a pilot seller and a test customer.
- **Risks:** unresolved legal/regulatory questions (D-09); over-collecting personal data.
- **Done when:** Owner signs the go/no-go.
