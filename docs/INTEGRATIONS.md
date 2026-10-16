# Integrations

## Telegram seller bot
- Run as a separate worker.
- Call the shared authenticated backend API.
- Store the bot token in a protected environment variable.
- Map Telegram numeric user IDs to approved seller accounts.
- Verify seller authorization on every operation.
- Begin with Add product, My products, Update price, and Update stock.
- New canonical products and canonical changes become admin-review drafts.
- Offer updates must identify the chosen offer and exact field being changed.
- Provide preview, confirm, cancel, and draft-resume behavior.
- Handle duplicate updates and retries idempotently.
- Use network timeouts and bounded retries.
- Do not report a write as successful if its result is unknown.

## Provider changes
Before choosing or changing an external service, document its cost, limits, backup/export path, runtime support, reliability, and migration plan.
