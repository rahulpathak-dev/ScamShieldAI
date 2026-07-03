# AWS Deployment Blueprint

This directory documents the production AWS target for ScamShieldAI.

## Recommended Services

- Amazon ECS Fargate for API and web containers
- Amazon RDS PostgreSQL for durable relational data
- Amazon ElastiCache Redis for queues, rate limiting, and cache
- Amazon S3 for backups, model artifacts, and deployment packages
- Amazon ECR or GHCR for container images
- AWS Secrets Manager for API keys, JWT secrets, SMTP credentials, and database credentials
- AWS CloudWatch for logs and alarms
- AWS WAF in front of the public load balancer

## Deployment Flow

1. CI builds and pushes API and web images.
2. The deployment workflow assumes an AWS role through GitHub OIDC.
3. ECS services are refreshed with the new image tags.
4. RDS automated backups and the application backup job protect PostgreSQL.
5. CloudWatch alarms monitor service health, CPU, memory, 5xx rates, and database storage.

## Required GitHub Secrets

- `AWS_DEPLOY_ROLE_ARN`

## Required GitHub Variables

- `AWS_REGION`
- `DEPLOYMENT_BUCKET`
- `ECS_CLUSTER`
- `ECS_SERVICE`
- `NEXT_PUBLIC_API_BASE_URL`