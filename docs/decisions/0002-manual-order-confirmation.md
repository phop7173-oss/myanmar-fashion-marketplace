# ADR-0002: Manual order confirmation, no payments, no built-in chat
- Status: Accepted (carried over from the original project charter)
- Date: 2026-10-20 (recorded)
- Decision owner: Project owner

## Context
The pilot has no budget and no payment partner. Payment, chat and delivery tracking add cost, legal exposure and security surface.

## Decision
Customers submit an order through a platform form. Admin contacts the customer and seller outside the platform and confirms the order manually. The platform does not process payment and has no chat.

## Alternatives considered
Payment gateway, wallet integration, built-in chat: rejected for the MVP (cost, compliance, complexity).

## Consequences
Admin workload is the pilot's bottleneck. Order states and rules: [ORDER-WORKFLOW](../ORDER-WORKFLOW.md).

## Revisit triggers
Admin cannot keep up with order volume, or the owner secures a payment/logistics partner.
