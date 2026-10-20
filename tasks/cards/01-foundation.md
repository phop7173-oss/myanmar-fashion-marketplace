# Cards: Phase 0-1 Foundation

"Standard DoD" = the Definition of Done in [docs/AI-WORKFLOW.md](../../docs/AI-WORKFLOW.md#definition-of-done-standard-task-cards-add-to-it).

### T-000 Documentation baseline v2
- **Objective:** A consistent, implementation-ready documentation set.
- **Prerequisites:** none.
- **Scope:** Markdown files only.
- **Non-goals:** any application code, scaffolding, dependency installation.
- **Docs:** all.
- **Expected files:** README, AGENTS, docs/*, docs/decisions/*, tasks/*, `.env.example`, `.gitignore`.
- **Acceptance:** all cross-references resolve; every decision has one authoritative location; no secrets; no claim that code exists.
- **Required tests:** automated link/ID check (done); Owner read-through.
- **Risks:** Proposed ADRs mistaken for final decisions.
- **Done when:** Owner reviews and marks Done.

### T-001 Resolve blocking decisions
- **Objective:** Owner accepts, edits, or rejects ADR-0005 (D-01, D-08) and ADR-0006 (D-03); notes defaults for D-06 and D-07.
- **Prerequisites:** T-000 Done.
- **Scope:** Owner decision session; AI may prepare comparison notes and update docs to match decisions.
- **Non-goals:** code, installs, hosting choice (T-002).
- **Docs:** decisions/README.md, ADR-0005, ADR-0006.
- **Expected files:** ADR status lines; TECH-STACK/CODE-STYLE adjusted if Option A chosen.
- **Acceptance:** ADR-0005 and ADR-0006 have status Accepted with date, or a Superseding ADR exists; docs match; D-01, D-03, D-06, D-07, D-08 marked resolved in the register.
- **Required tests:** link check after edits.
- **Risks:** deciding D-01 without understanding the trade-off; Owner may ask the AI to explain each option in plain language first.
- **Done when:** Owner marks Done.

### T-002 Verify hosting and free-tier facts
- **Objective:** Evidence-based hosting/database shortlist for a zero-budget pilot (D-02).
- **Prerequisites:** T-001.
- **Scope:** Research from official sources; fill the U1-U12 table with source link, date, finding; propose one primary and one fallback option in an ADR (`Proposed`).
- **Non-goals:** creating accounts that need payment details, deploying anything.
- **Docs:** TECH-STACK (UNVERIFIED items), DEPLOYMENT.
- **Expected files:** new ADR `0007-hosting.md`; TECH-STACK updated with findings.
- **Acceptance:** each U-item is marked Verified (with source/date) or still UNVERIFIED with the reason; no number or term is written without a source.
- **Required tests:** none (documentation); Owner spot-checks sources.
- **Risks:** stale or marketing-page claims; terms change. Re-check at T-063.
- **Done when:** Owner accepts the ADR.

### T-010 Project skeleton and tooling
- **Objective:** A minimal runnable application with formatting, linting and test commands.
- **Prerequisites:** T-001 (D-01 Accepted).
- **Scope:** Create the project with the approved stack; one placeholder home page; one trivial passing test; commit the lockfile; document run/test commands in README and TESTING; record repository layout in ARCHITECTURE.
- **Non-goals:** database models, authentication, styling beyond a minimal CSS file, CI.
- **Docs:** TECH-STACK, CODE-STYLE, TESTING, ARCHITECTURE.
- **Expected components:** project configuration, application package, test configuration, lockfile.
- **Acceptance:** app starts locally; format/lint, unit-test commands run and pass; `.gitignore` covers local files; no secrets; versions chosen are current supported releases and stated in the report.
- **Required tests:** the trivial test; run lint and tests.
- **Risks:** installing unapproved packages; version choices from memory (verify against official release information).
- **Done when:** Standard DoD; commands documented and run by the Owner.

### T-011 Configuration and secrets handling
- **Objective:** Settings come from environment variables and fail clearly when missing.
- **Prerequisites:** T-010.
- **Scope:** environment-based settings; startup validation; `.env.example` finalized (names only); safe defaults (debug off unless explicitly development).
- **Non-goals:** real secrets, hosting configuration.
- **Docs:** SECURITY (Secrets), DEPLOYMENT (Configuration).
- **Expected components:** settings module, `.env.example`.
- **Acceptance:** missing required variable stops startup with a message that does not print secret values; AC-SEC-01 foundations (no secrets tracked; `.env` ignored).
- **Required tests:** startup test with missing/invalid variables; a check that `.env` is untracked.
- **Risks:** accidentally printing settings in errors; committing a local `.env`.
- **Done when:** Standard DoD.

### T-012 Local database and migration baseline
- **Objective:** Local PostgreSQL connection and a working migration process.
- **Prerequisites:** T-011.
- **Scope:** documented local database setup (simplest method for Ubuntu); connection via environment; migration tool running; empty initial migration; test database used by tests.
- **Non-goals:** business tables.
- **Docs:** DATA-MODEL (Migrations), TESTING, DEPLOYMENT.
- **Expected components:** database settings, migration folder, test configuration.
- **Acceptance:** migrations apply to a fresh database; tests run against a real PostgreSQL database; steps documented and reproducible.
- **Required tests:** migrate-from-scratch test run; database connectivity test.
- **Risks:** local setup friction for a beginner (AI should give exact, minimal steps).
- **Done when:** Standard DoD; Owner reproduces setup from the docs.

### T-013 Continuous integration
- **Objective:** Automatic lint + tests on every push/pull request.
- **Prerequisites:** T-012; GitHub Actions availability verified (U9).
- **Scope:** one workflow running lint, tests with a PostgreSQL service, and a dependency vulnerability audit step; pinned action versions; no secrets.
- **Non-goals:** deployment, paid runners.
- **Docs:** TESTING, SECURITY (Dependencies).
- **Expected components:** one workflow file.
- **Acceptance:** workflow passes on a branch (evidence: link or log excerpt); fails when a test is broken (demonstrated once on a throwaway branch).
- **Required tests:** the workflow itself.
- **Risks:** free-minute limits (UNVERIFIED); third-party actions are dependencies and need approval (R8).
- **Done when:** Standard DoD.
