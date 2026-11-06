# Myanmar Fashion Marketplace

A mobile-first, low-bandwidth marketplace for clothing and fashion in Myanmar, built as a **zero-budget pilot** with a small group of curated sellers. Customers order through a platform form; admin confirms orders manually; sellers update prices and stock through a guided Telegram bot.

## Current status
- **Phase 1 started.** The documentation baseline and decisions are in place; the only application code is a placeholder skeleton (one home page). No features are built and nothing is deployed.
- T-000, T-001, T-010 and T-011 are Done: D-01 (Django), D-03 (order model), D-06, D-07 and D-08 (webhook) are accepted. Hosting (D-02) is still open (T-002, proposal in ADR-0007). T-012 (local database and migrations) is **Ready for review**; current task: [tasks/CURRENT.md](tasks/CURRENT.md).

## Where to look (single source of truth per topic)
| Topic | Document |
|-------|----------|
| Goals, scope, roles, pilot metrics | [docs/PROJECT.md](docs/PROJECT.md) |
| Decision status (accepted / open) | [docs/decisions/README.md](docs/decisions/README.md) |
| System shape, layers, MVP vs later vs rejected | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Technologies, dependency policy, UNVERIFIED facts | [docs/TECH-STACK.md](docs/TECH-STACK.md) |
| Tables, constraints, visibility rules | [docs/DATA-MODEL.md](docs/DATA-MODEL.md) |
| Operations, errors, idempotency | [docs/API-CONTRACT.md](docs/API-CONTRACT.md) |
| Order states and submission/confirmation rules | [docs/ORDER-WORKFLOW.md](docs/ORDER-WORKFLOW.md) |
| Security, privacy, permissions | [docs/SECURITY.md](docs/SECURITY.md) |
| Telegram bot behavior | [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) |
| Performance budgets | [docs/PERFORMANCE.md](docs/PERFORMANCE.md) |
| What must be true (testable criteria) | [docs/ACCEPTANCE-TESTS.md](docs/ACCEPTANCE-TESTS.md) |
| How we test; evidence | [docs/TESTING.md](docs/TESTING.md) |
| Environments, backups, runbooks | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| Code style | [docs/CODE-STYLE.md](docs/CODE-STYLE.md) |
| AI workflow, templates, Definition of Done | [docs/AI-WORKFLOW.md](docs/AI-WORKFLOW.md) |
| Rules for AI agents | [AGENTS.md](AGENTS.md) |
| Task order and task cards | [tasks/ROADMAP.md](tasks/ROADMAP.md), [tasks/CURRENT.md](tasks/CURRENT.md) |

Each rule is stated in one place; other documents link to it.

## Decisions
- **Final:** shared canonical catalog; manual orders with no payments or chat; Telegram seller bot with admin review; one server-side rule layer; English-first; clothing first; curated sellers; zero budget; authorized images only; Django baseline (D-01); MVP order model (D-03); admin-only image uploads (D-06); tunable defaults (D-07); Telegram webhook mode (D-08).
- **Need Owner approval:** hosting (D-02), business operations (D-04), privacy retention (D-05), legal check (D-09). Details and blocking relationships: [decisions/README.md](docs/decisions/README.md).

## How to start a development task (human or AI)
1. Open [tasks/CURRENT.md](tasks/CURRENT.md) and read the task card it names.
2. Check the card's prerequisites are complete (with evidence) and its blocking decisions are Accepted.
3. Give your AI tool the **Planner** prompt from [docs/AI-WORKFLOW.md](docs/AI-WORKFLOW.md). Approve or correct the plan.
4. Give the **Coder** prompt. Review the report and diff using the beginner review guide.
5. Run the tests yourself, then commit with `T-NNN: description` and update the task status.

## Glossary
- **Product:** one canonical item (admin-approved). **Product variant:** a size/color of a product.
- **Seller offer:** one seller's offer to sell one product. **Offer variant:** that seller's price, stock and availability for one variant.
- **Order item:** a purchased line with a snapshot of product, seller, variant and price at purchase time.
- **Draft:** a seller's proposed new product or change, waiting for admin review.
- **UNVERIFIED:** an external fact (price, limit, behavior) that must be checked in official sources before use.

## Development environment
Implementation happens on the Owner's Ubuntu laptop. Termux is used only for Markdown and Git synchronization. GitHub is the shared source of truth. 

### First-time setup (Ubuntu)
```bash
python3 --version                      # expect 3.12 or newer
sudo apt install python3-venv          # only if the next line says ensurepip is not available
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### Configuration (environment variables)
The app reads its settings from environment variables and **refuses to start** with a clear message if one is missing or unsafe. The message names the variable, never its value. Names are documented in [.env.example](.env.example).

| Variable | Development | Production |
|----------|-------------|------------|
| `APP_ENV` | required: `development` | required: `production` |
| `SECRET_KEY` | optional (a local placeholder is used) | required, at least 50 characters, unique to the site |
| `ALLOWED_HOSTS` | optional (defaults to `localhost,127.0.0.1`) | required, comma-separated, no `*` |
| `DATABASE_URL` | required: `postgresql://USER:PASSWORD@HOST:5432/DATABASE_NAME` | required, with a password; a database on another machine must end with `?sslmode=require` |

Set them once per terminal session (Git ignores your `.env`; never commit it or paste its contents into chats):
```bash
cp .env.example .env                   # first time only, then edit .env
set -a; . ./.env; set +a            # load the variables
python -c "import secrets; print(secrets.token_urlsafe(64))"   # to generate a SECRET_KEY
```
`pytest` ignores `APP_ENV`, `SECRET_KEY` and `ALLOWED_HOSTS` from your shell and always runs in development mode, but it **needs `DATABASE_URL`** and a running PostgreSQL, so load `.env` first.

### Local database (PostgreSQL)
Ubuntu 26.04 already provides PostgreSQL (18 when this was written). Install it only if missing: `sudo apt install postgresql`. Then, once:
```bash
systemctl is-active postgresql                                   # expect: active
sudo -u postgres createuser --createdb --pwprompt marketplace    # asks for a NEW password (typing is hidden)
sudo -u postgres createdb --owner=marketplace marketplace_dev
```
Edit `.env` and replace `CHANGE_ME` in `DATABASE_URL` with that password (letters and digits only). Check the login (it asks for the password and should print a table containing `1`):
```bash
psql "postgresql://marketplace@localhost:5432/marketplace_dev" -c "SELECT 1"
```
Then create the migration bookkeeping and apply the baseline migration:
```bash
python manage.py migrate     # first run: "Applying storefront.0001_initial... OK"; second run: "No migrations to apply."
```
The `marketplace` role may create databases only so the tests can build their own throwaway `test_marketplace_dev` database; your development data is never touched. **Never put production credentials in your local `.env`.**

| If you see | It usually means | Fix |
|------------|------------------|-----|
| `connection refused` | PostgreSQL is not running | `sudo systemctl start postgresql` |
| `password authentication failed` | wrong password in `DATABASE_URL` | `sudo -u postgres psql`, then `\password marketplace`, then update `.env` |
| `role "marketplace" already exists` or `database ... already exists` | already created earlier | skip that command |
| `password authentication failed` (from `pytest` or `migrate`) | `.env` still has `CHANGE_ME` (check: `grep -c CHANGE_ME .env` must print `0`), or the role does not exist (`sudo -u postgres psql -c "\du"` lists roles) | edit `.env` with `nano .env` (not `sed`, which stores the password in your shell history), reload it, then test: `psql "$DATABASE_URL" -c "SELECT 1"` |
| `permission denied to create database` (from `pytest`) | the role lacks permission | `sudo -u postgres psql -c "ALTER ROLE marketplace CREATEDB"` |
| `DATABASE_URL is required` | `.env` not loaded in this terminal | `set -a; . ./.env; set +a` |

### Every time
```bash
source .venv/bin/activate
set -a; . ./.env; set +a            # loads APP_ENV=development and the rest
python manage.py migrate               # applies any new database migrations (does nothing if none)
python manage.py runserver             # then open http://127.0.0.1:8000/
```

### Check your work
```bash
ruff format .          # format code
ruff check .           # lint
pytest                 # tests
```
More detail: [docs/TESTING.md](docs/TESTING.md). Without `APP_ENV` set, commands such as `runserver` stop with a clear message. Debug is on only when `APP_ENV=development`.
