# Acceptance Criteria

## Catalog
- Public users see only published canonical products and active offers.
- Canonical product and seller offer are distinct entities.
- Variants, seller-specific prices, stock, and freshness are explicit.
- Search results are paginated.
- Image source and permission are recorded.

## Seller management
- Identity comes from verified authentication.
- Sellers can manage only their own permitted offers.
- New canonical products await admin review.
- Price and stock changes are validated and audited.

## Orders
- Server validates offer, variant, quantity, price, and total.
- Duplicate submissions are prevented.
- Order items preserve purchase-time snapshots.
- Customer data is restricted to authorized roles.

## Security and performance
- Admin operations reject non-admin users.
- Invalid and oversized uploads are rejected.
- Secrets are absent from tracked files and client bundles.
- Errors do not expose internals.
- Core flows work on mobile.
- Lists are bounded and images optimized.
