# ADR-0006: MVP order model
- Status: **Accepted** (Owner, 2026-10-20; all seven defaults accepted without changes)
- Date: 2026-10-20
- Decision owner: Project owner

## Context
The original docs say "orders contain one or more items" and "manual confirmation" but do not define who the customer is, whether a cart may mix sellers, when stock is reserved, how price changes during ordering are handled, or who sets the delivery fee.

## Decision (accepted)
1. **One seller per order.** All items in an order belong to the same seller's offer(s). (A multi-seller cart would need separate confirmation and delivery per seller.)
2. **Guest checkout.** No customer accounts. No customer order-lookup page in the MVP; admin contacts the customer. The customer sees an order reference on the confirmation page.
3. **Prices:** whole-kyat integer MMK only. The order form carries the price the customer saw; if the current price differs, the server rejects with a conflict and shows the new price (customer must re-submit).
4. **Stock is not reserved at submission.** Submission checks availability and, if stock is known, quantity <= stock. Stock is **deducted when admin confirms** the order, inside a locked transaction. Overselling is possible between submission and confirmation and is resolved manually.
5. **Delivery fee** is entered by admin at confirmation (nullable until then). Items total is calculated by the server and never edited after submission.
6. **Payment** happens outside the platform; the platform records nothing about it.
7. **No automatic notifications** to customers or sellers in the MVP. Customer personal data is never sent through Telegram.

## Alternatives considered
Reserve stock at submission (needs expiry jobs; free hosts may not run schedulers). Multi-seller carts (more states, no pilot benefit). Customer accounts (SMS OTP costs money; more privacy exposure).

## Consequences
Simple, safe, achievable at zero cost; admin carries manual work. Details: [ORDER-WORKFLOW](../ORDER-WORKFLOW.md).

## Revisit triggers
Overselling or cancellations from stale stock exceed what admin can handle; customers demand order tracking.
