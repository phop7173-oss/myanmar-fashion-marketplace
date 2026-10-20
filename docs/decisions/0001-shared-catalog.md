# ADR-0001: Shared canonical catalog with seller offers
- Status: Accepted (carried over from the original project charter)
- Date: 2026-10-20 (recorded)
- Decision owner: Project owner

## Context
Several sellers may sell the same item. Separate listings per seller would duplicate products and prevent price comparison.

## Decision
- A **product** is one canonical item, approved by admin.
- A **product variant** is a size/color combination of that product.
- A **seller offer** is one seller's offer to sell one product.
- An **offer variant** is the seller-specific price, stock and availability for one product variant.
- Orders copy purchase-time data into order items (snapshots).

## Alternatives considered
- Seller-owned listings only: simpler, but duplicates and no comparison. Rejected.

## Consequences
- Admin must decide whether two submissions are the same product (duplicate-review work).
- Unbranded or tailor-made items may not fit "same product" cleanly.

## Revisit triggers
During the pilot, if a large share of submitted items cannot be matched to a canonical product, or admin duplicate review becomes the bottleneck.
