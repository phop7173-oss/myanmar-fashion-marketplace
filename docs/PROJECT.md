# Project Charter

Build a mobile-first, low-bandwidth Myanmar fashion marketplace.

## Product decisions
- Initial category: clothing and fashion.
- Shared canonical product catalog with seller-specific offers.
- Customer orders use a platform form and manual confirmation.
- Admin manages products, images, sellers, offers, and orders.
- Sellers manage approved offers through a guided Telegram bot.
- English-first interface; support localization later.
- No payment gateway or built-in chat in the MVP.
- Curated seller onboarding; no unrestricted public seller registration.
- Use only authorized product images.
- Start with a near-zero budget; verify free-tier limits before deployment.

## Roles
- Anonymous customer: browse published products.
- Customer: submit orders.
- Approved seller: manage permitted fields of their own offers.
- Admin: approve canonical products and manage the marketplace.
- Bot/worker: perform explicitly authorized operations.

## Goals
Validate customer demand, seller participation, order completion, stale-price rates, cancellation rates, and performance on weak mobile connections.

## Out of scope
Automated payments, wallets, real-time delivery tracking, built-in chat, AI recommendations, and automated supplier procurement.
