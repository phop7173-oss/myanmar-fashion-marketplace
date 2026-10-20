# Myanmar Fashion Marketplace

A mobile-first, low-bandwidth marketplace for clothing and fashion in Myanmar, built as a **zero-budget pilot** with a small group of curated sellers. Customers order through a platform form; admin confirms orders manually; sellers update prices and stock through a guided Telegram bot.

## Current status
- **Phase 0: documentation and decisions. No application code exists yet.** Nothing has been built, tested or deployed.
- Documentation baseline v2 is written and **awaiting Owner review** (task T-000, see [tasks/CURRENT.md](tasks/CURRENT.md)).
- T-001 (blocking decisions) is **Ready for review**: D-01 (Django), D-03 (order model), D-06, D-07 and D-08 (webhook) are accepted. Hosting (D-02) is still open (T-002). Scaffolding (T-010) starts only after the Owner marks T-000 and T-001 Done.

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
Implementation happens on the Owner's Ubuntu laptop. Termux is used only for Markdown and Git synchronization. GitHub is the shared source of truth. Run/setup instructions will be added here by task T-010.
