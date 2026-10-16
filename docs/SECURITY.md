# Security Requirements

## Authentication and authorization
- Use a maintained authentication solution.
- Authorize every protected operation on the server.
- Admin actions require an explicit admin role.
- Sellers can access only their own resources.
- Telegram numeric user ID must map to an approved account.
- Telegram usernames and callback buttons are not proof of authorization.
- Check ownership for every supplied resource ID to prevent IDOR/BOLA vulnerabilities.

## Secrets
- Never commit credentials, bot tokens, session secrets, or production environment files.
- Keep only safe placeholders in .env.example.
- Never paste real secrets into AI prompts.
- Rotate leaked secrets immediately.
- Never expose server secrets to client bundles.

## Input and data protection
- Validate request bodies, query parameters, callback data, and uploads.
- Use safe parameterized database operations.
- Apply payload limits, rate limits, and timeouts where appropriate.
- Do not log tokens, full customer contact details, or unnecessary personal data.
- Validate image content, dimensions, and size; use generated storage names.
- Use only images with permission or an authorized source.

## Orders and operations
- Calculate totals on the server.
- Use transactions and idempotency for critical writes.
- Audit sensitive changes without storing secrets.
- Use HTTPS, least privilege, patched dependencies, separate environments, and tested backups.
- User-facing errors must not expose internal diagnostics.
