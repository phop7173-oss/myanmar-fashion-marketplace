# Code Style

**Authoritative for:** how code is written so a beginner can read, review and maintain it. Python/Django rules apply to the recommended baseline ([ADR-0005](decisions/0005-platform-baseline.md)); if Option A is chosen, replace the Python-specific lines with strict-TypeScript equivalents.

## Readability for a beginner (most important)
1. Prefer plain, explicit code over clever code. No metaprogramming, dynamic attribute tricks, or deep inheritance.
2. A function does one thing and fits on one screen (guideline: <= 40 lines; longer needs a reason in the plan).
3. Every service function has a short docstring stating: what it does, who may call it, what it validates, and what it guarantees (invariants).
4. Comments explain **why**, not what. Each new file starts with a one-line purpose comment.
5. No magic numbers or strings: named constants/settings (e.g. page size, stale days, quantity limit) defined once.
6. Descriptive names; domain vocabulary only: product, variant, seller, offer, offer variant, order, order item, draft.

## Structure
7. Business rules only in the service layer ([ARCHITECTURE](ARCHITECTURE.md)). Views, admin classes, templates and bot handlers contain none.
8. Request/response shapes are separate from database models where they differ.
9. Validate external data at runtime at the boundary (forms/serializers/schemas). Types alone do not validate input.
10. Keep modules cohesive; do not create abstractions until a second real use exists.

## Safety
11. No bare `except`, no silent catch; handle errors by returning the documented error code and logging safely.
12. No dead code, commented-out code, or TODOs without a task ID.
13. No raw SQL, shell calls, `eval`, unsafe deserialization, or "mark safe" HTML without owner approval ([SECURITY](SECURITY.md#input-injection-xss-csrf)).
14. Money is an integer number of MMK. Times are timezone-aware UTC.
15. Never log secrets or personal data; never place server secrets in templates or client code.

## Python specifics
16. Type hints on all function signatures; pass the project's type/lint checks.
17. Formatting and linting with the single configured tool; do not hand-format or argue style.
18. Prefer server-rendered templates; add JavaScript only with plan approval and within the [PERFORMANCE](PERFORMANCE.md) budget.

## Naming
Python and database identifiers `snake_case`; classes `PascalCase`; constants `UPPER_SNAKE_CASE`; test names describe behavior (`test_seller_cannot_change_other_sellers_price`).

## Tooling
Do not choose formatter/linter/test commands from memory: inspect project configuration; T-010 defines them and [TESTING](TESTING.md) records them.
