# Code Style

- Prefer readable, explicit, maintainable code.
- Keep functions focused and modules cohesive.
- Avoid `any`, silent catch blocks, dead code, magic values, and unnecessary dependencies.
- Validate external data at runtime; TypeScript types alone do not validate network input.
- Keep business rules out of UI components and Telegram handlers.
- Use strict TypeScript and meaningful domain types.
- Keep API request/response types distinct from database rows where their shapes differ.
- Prefer server components unless browser interaction requires client components.
- Never expose server secrets in client-side code.
- Use type hints in Python.
- Separate Telegram presentation, API communication, and business logic.
- Use PascalCase for components and types.
- Use camelCase for TypeScript variables/functions.
- Use snake_case for Python and database identifiers.
- Use product, variant, seller, offer, and order consistently.
- Inspect project configuration before choosing formatter, lint, or test commands.
