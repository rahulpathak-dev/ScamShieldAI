# Production Deployment Checklist

## Before Deploy

- Rotate `SCAMSHIELD_JWT_SECRET_KEY` to a 32+ character secret.
- Store database, SMTP, LLM, and enterprise API keys in Secrets Manager.
- Restrict CORS to production web origins.
- Configure WAF managed rules and request-size limits.
- Enable RDS automated backups and deletion protection.
- Enable HTTPS on the load balancer.
- Confirm `/health` responds behind the load balancer.

## After Deploy

- Create the first admin user.
- Run smoke tests for auth, text analysis, alerts, assistant, and enterprise batch API.
- Confirm logs appear in CloudWatch.
- Confirm backups are produced and restore procedure is tested.
- Confirm alert routing for API downtime and database storage thresholds.