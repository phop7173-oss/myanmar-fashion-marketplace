# Testing Strategy

## Layers
- Unit: validation, pricing, permissions, and status transitions.
- Integration: database constraints, transactions, authentication, and API contracts.
- End-to-end: critical customer and admin flows.
- Bot: unapproved users, malformed callbacks, duplicate updates, timeouts, and retries.
- Security: cross-seller access, admin-only operations, upload validation, and order tampering.

## Critical scenarios
1. Public users see only approved catalog items.
2. Seller A cannot read or modify Seller B's offers.
3. Unapproved Telegram users cannot change data.
4. Sellers can modify only permitted fields of their own offers.
5. New canonical products require admin approval.
6. Order totals are calculated server-side.
7. Order items preserve snapshots after later edits.
8. Duplicate order submissions do not create duplicate orders.
9. Invalid uploads are rejected safely.
10. Sensitive admin changes are audited.
11. List endpoints enforce pagination limits.

Use synthetic test data. Add regression tests for bugs. Never claim tests passed unless they were actually run. If tests cannot run, identify what remains unverified.
