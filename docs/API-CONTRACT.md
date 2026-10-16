# API Contract

The backend is the trusted boundary for the storefront, admin interface, and Telegram bot.

Every protected operation must define:
- Request and response schemas.
- Authentication requirements.
- Resource-level authorization.
- Validation and normalization.
- Error codes and status behavior.
- Pagination and idempotency requirements.
- Audit requirements.
- Tests for permitted and denied access.

## Endpoint families
1. Public catalog search, listing, and product details.
2. Order submission and authorized order access.
3. Admin catalog, seller, offer, draft, and order management.
4. Seller/bot offer listing and permitted price/stock changes.

## Mandatory rules
- Never trust a client-supplied seller_id as proof of identity.
- Recalculate prices and totals on the server.
- Paginate lists and cap page sizes.
- Use stable errors for validation, unauthenticated, forbidden, not found, conflict, rate limit, and unexpected failure.
- Never expose stack traces, secrets, SQL details, or another seller's private data.
- Update this contract and tests whenever API behavior changes.
