# Implementation Roadmap

## Phase 0: Repository and contracts
- [ ] Inspect current repository.
- [ ] Review project rules and approve technical assumptions.
- [ ] Establish formatting, linting, type checking, tests, and CI.
- [ ] Define one small vertical slice.

## Phase 1: Foundation
- [ ] Initialize approved web app.
- [ ] Validate environment configuration.
- [ ] Add database migrations and CI checks.

## Phase 2: Catalog
- [ ] Seed synthetic products, variants, offers.
- [ ] Build mobile listing, search, and product detail.
- [ ] Test visibility, pagination, and performance.

## Phase 3: Admin
- [ ] Add admin authentication and authorization.
- [ ] Implement catalog editing and draft review.
- [ ] Manage sellers, offers, and audit events.

## Phase 4: Orders
- [ ] Define manual confirmation states.
- [ ] Implement order form and server-side pricing.
- [ ] Save order snapshots transactionally.
- [ ] Test duplicates, stale prices, and denied access.

## Phase 5: Telegram
- [ ] Create separate worker and API client.
- [ ] Verify approved numeric Telegram identity.
- [ ] Implement commands incrementally.
- [ ] Test permissions, duplicates, and network failures.

## Phase 6: Pilot
- [ ] Test mobile/weak-network experience.
- [ ] Verify image permissions.
- [ ] Test backups and restore.
- [ ] Document deployment, monitoring, and rollback.
- [ ] Review pilot results and actual costs.

Do not mark phases complete without evidence. Prefer one working vertical slice over many incomplete features.
