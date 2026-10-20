# Order Workflow

**Authoritative for:** order submission, states, transitions, stock behavior. Depends on [ADR-0006](decisions/0006-mvp-order-model.md) (**Proposed**, D-03). Table fields: [DATA-MODEL](DATA-MODEL.md). Operations: [API-CONTRACT](API-CONTRACT.md).

## States
`submitted` -> `confirmed` -> `completed`; `submitted` or `confirmed` -> `cancelled`. No other transitions. `completed` and `cancelled` are final.

| Transition | Who | Rules |
|------------|-----|-------|
| (new) -> submitted | Customer (guest) | Submission steps below |
| submitted -> confirmed | Admin | Locked stock check/deduction; optional delivery fee; confirmed_by and time recorded; audited |
| confirmed -> completed | Admin | Records completed_at; audited |
| submitted/confirmed -> cancelled | Admin | Reason required (`customer_request`, `seller_unavailable`, `price_or_stock_changed`, `unreachable`, `duplicate`, `other`); stock restored if it was deducted; audited |

Illegal transitions are rejected by one function in the service layer and covered by tests for every state pair.

## Submission (all on the server, one database transaction)
1. Validate and normalize input (name, phone, address, township, region, items, quantities, idempotency key, displayed prices). Reject unknown fields.
2. Apply rate limits and the honeypot check ([SECURITY](SECURITY.md#rate-limiting-and-abuse)).
3. **Idempotency:** if an order with this idempotency key exists, return that order if the request content matches, else a conflict. Never create a second order.
4. Load each requested offer variant. Reject if the product is not published, the seller or offer is not active, the product variant is archived, or the offer variant is unavailable.
5. All items must belong to one seller's offers (one order, one seller).
6. Quantity must be 1..max (default 10, D-07). If stock is known (not NULL) and quantity exceeds it, reject (`insufficient_stock`).
7. Compare each displayed price sent by the form with the current price. If any differs, reject with `price_changed` and show current prices. The customer must submit again.
8. Compute line totals and items total (integers) from **database prices**, never from the request.
9. Insert order and order items with snapshots (product title, seller name, size, color, unit price, quantity, line total, currency). Stock is **not** changed.
10. Commit. Show the confirmation page with the order's public reference.

## Confirmation (admin)
In one transaction: lock the affected offer variant rows in a fixed order (by id), re-check availability and stock, deduct stock for items whose stock is known (mark each item `stock_deducted`), set status, record confirmer/time and optional delivery fee. If stock is insufficient the whole confirmation fails with a conflict and nothing changes. If the current price differs from the snapshot, the admin screen warns; the order total is **never** changed silently, so the admin either honors the snapshot price (explicit action) or cancels.

## Cancellation
If any item has `stock_deducted`, restore that quantity in the same transaction.

## Customer data
Name, phone, optional contact channel, delivery address, township, region, optional note. Collected only for fulfillment. Visible to admins only. Retention and erasure: [SECURITY](SECURITY.md#personal-data).

## Not in the MVP
Customer accounts and order lookup, automatic notifications, payment records, multi-seller orders, stock reservation at submission, refunds and returns tracking.
