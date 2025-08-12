#!/usr/bin/env bash
# Create a minimal Glue service role with S3 full access policy attached (for demo only)
# Run from a privileged account / AWS CLI configured with sufficient rights

ROLE_NAME="GlueDemoRole"
TRUST_POLICY='{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "glue.amazonaws.com"},"Action": "sts:AssumeRole"}]}'

aws iam create-role --role-name ${ROLE_NAME} --assume-role-policy-document "${TRUST_POLICY}"
aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name ${ROLE_NAME} --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole

echo "Created role: ${ROLE_NAME}"
