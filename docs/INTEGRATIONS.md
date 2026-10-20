# Integrations

**Authoritative for:** Telegram seller bot behavior and external services. Rationale: [ADR-0003](decisions/0003-telegram-seller-operations.md), [ADR-0005](decisions/0005-platform-baseline.md). Operations: [API-CONTRACT](API-CONTRACT.md) (SEL-*, TG-1). Security: [SECURITY](SECURITY.md).

## External services in the MVP
Telegram Bot API only. No email, SMS, payment, analytics, chat, CDN, or map services. Before adding or changing any external service, document cost, limits, export path, runtime support, reliability, and migration plan in an ADR.

## Telegram bot

### Delivery mode (D-08, recommended: webhook)
- Telegram sends updates to an HTTPS URL of the application. Each request must carry the configured secret token header; otherwise respond 403 and do nothing.
- Polling requires an always-on process and is used only if the chosen host cannot receive webhooks.
- Verify the Bot API facts used here (secret-token header, button data size limit, rate limits) against Telegram's official documentation when implementing (UNVERIFIED, TECH-STACK U7).

### Identity and linking
1. Admin issues a single-use link code for an approved seller (expires, default 24 hours).
2. The seller opens a **private chat** with the bot and sends the code.
3. The server takes the numeric Telegram user ID from the update itself (never from message text) and links it to the seller; the code is consumed atomically.
4. Authorization on every later message/button press: look up the numeric ID -> active `telegram_accounts` row -> active seller. No match: generic reply ("This account is not linked. Ask the marketplace admin."), no data, no details.
5. Username changes have no effect. Admin can revoke a link at any time; revocation applies immediately.
6. Groups and channels are ignored; only private chats are served.

### MVP commands and flows
| Command | Behavior |
|---------|----------|
| `/start`, `/help` | Explain linking or list commands |
| My offers | Paginated list of the seller's own offer variants with price, stock, confirmed dates |
| Update price | Choose offer variant -> enter new price (whole MMK) -> **preview** (old -> new, large-change warning) -> **Confirm** or **Cancel** |
| Update stock | Same flow; allows "sold out" (0), a number, or "unknown" |
| Add product | Guided text steps -> preview -> confirm -> creates a **draft** for admin review (no images in the MVP) |
| `/cancel` | Abort the current flow |

Rules:
- Each change identifies the exact offer variant and exact field being changed in the preview.
- Buttons carry only an opaque token; the token maps to a server-side pending action ([DATA-MODEL](DATA-MODEL.md#bot_pending_actions-t-052)) bound to that seller, single use, expiring (default 15 minutes).
- Changes use absolute values and the `row_version` read at preview; if data changed since the preview, the confirm is rejected and the seller sees current values.
- Conversation state is stored in the database, not memory (webhook handlers are stateless).
- Replies are plain text, English-first, short (low data use). Seller-supplied text is never interpreted as formatting or commands.
- Never include customer personal data in any bot message.

### Reliability
- Duplicate `update_id` ignored; replays of a used token do nothing.
- Outbound calls to Telegram use a timeout (default 10 s) and bounded retries with backoff (max 2).
- If the outcome of a write is unknown (timeout, crash), the bot must **not** say it succeeded; it tells the seller to check "My offers".
- Handler code stays thin; no business rules in handlers ([ADR-0004](decisions/0004-single-trust-boundary.md)).

### Bot token handling
Token and webhook secret only in environment variables. Rotating the token or secret is a documented runbook ([DEPLOYMENT](DEPLOYMENT.md#runbooks)). Never log them or include them in prompts.
