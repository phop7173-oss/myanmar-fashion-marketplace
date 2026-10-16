# Deployment and Recovery

Keep development, preview, and production environments separate.
Use synthetic development data and separate credentials.

Maintain .env.example with variable names and safe placeholders only. Validate required environment variables at startup.

Before selecting hosting, verify current quotas, inactivity rules, persistent worker support, backups, retention, connection limits, storage costs, and data export options.

## Release checklist
- Automated checks pass.
- Environment variables are verified.
- Database migrations are reviewed and tested.
- Backup and restore procedures are documented.
- Authentication and authorization tests pass.
- Logs avoid secrets and unnecessary personal data.
- Critical flows work in the deployed environment.
- Rollback/recovery steps are known.
- Human owner approves release.

Document credential rotation, disabling compromised seller/bot access, database restoration, rollback, and order reconciliation after partial failures. Test restoring backups periodically.
