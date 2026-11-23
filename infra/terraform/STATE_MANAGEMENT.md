
# Terraform State Management

## Overview

Hotel AI Copilot uses Amazon S3 for remote Terraform state
storage in the ap-southeast-2 AWS region.

## Current Infrastructure

The dedicated Terraform state bucket has been deployed.

Verified security controls:
- S3 Block Public Access enabled
- AES-256 server-side encryption
- S3 bucket versioning enabled
- HTTPS-only bucket policy
- S3-native state locking configured

## State Organization

Two Terraform projects use separate state keys:

Bootstrap:
bootstrap/terraform.tfstate

Application:
hotel-ai-copilot/dev/terraform.tfstate

## Deployment Status

### Terraform Bootstrap

- S3 state bucket deployed successfully
- Five AWS resources created
- Bootstrap state migrated to S3
- Remote state object verified
- Terraform plan confirmed zero changes

### Application Infrastructure

- Remote S3 backend configured locally
- Terraform initialization successful
- Infrastructure plan generated successfully
- Application resources have not been applied yet

## Developer Setup

1. Configure the AWS CLI with an authorized profile.
2. Copy backend.tf.example to backend.tf.
3. Replace the placeholder with the correct S3 bucket name.
4. Run terraform init.
5. Review terraform plan before applying infrastructure.

If migrating existing local state, back it up and use
terraform init -migrate-state instead.

## Security Guidelines

- Never commit Terraform state or AWS credentials.
- Keep backend.tf excluded from Git.
- Keep state locking enabled.
- Review all infrastructure changes before applying.
- Use restricted IAM permissions for ongoing access.
- Preserve state version history for recovery.

## Bootstrap Recovery

The bootstrap project manages the bucket containing its own
remote state.

Avoid destroying or renaming the state bucket.

Maintain a secure, encrypted recovery backup and verify remote
state before deleting any older local backup.

## Cost Management

S3 storage and requests may incur charges.

Use AWS Budgets and monitor usage regularly.
