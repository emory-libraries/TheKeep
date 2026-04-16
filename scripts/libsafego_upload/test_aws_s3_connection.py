#!/usr/bin/env python3
"""
Test connection to AWS S3 using endpoint and credentials.
Credentials can be set via environment variables or a local config file.

Environment variables:
  AWS_S3_ENDPOINT   (optional, default: s3.us-east-1.amazonaws.com)
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_DEFAULT_REGION (optional, default: us-east-1)

Or create aws_s3_credentials.env (gitignored) with:
  AWS_ACCESS_KEY_ID=your_key
  AWS_SECRET_ACCESS_KEY=your_secret
  AWS_S3_ENDPOINT=s3.us-east-1.amazonaws.com
  AWS_DEFAULT_REGION=us-east-1

For S3-compatible services (e.g. LibSafe Go S3 gateway), set AWS_S3_ENDPOINT
to that service's URL (e.g. https://s3.libsafe.example.com) instead of AWS.
"""

import os
import sys

def load_env_file(path='aws_s3_credentials.env'):
    """Load key=value pairs from a file into os.environ."""
    if not os.path.exists(path):
        return False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip()
    return True

def main():
    # Try loading from local env file first (don't commit this file!)
    if load_env_file():
        print("Loaded credentials from aws_s3_credentials.env")
    else:
        print("Using environment variables for AWS credentials")

    endpoint = os.environ.get('AWS_S3_ENDPOINT', 's3.us-east-1.amazonaws.com')
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

    if not access_key or not secret_key:
        print("\nERROR: AWS credentials not set.")
        print("Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, or create aws_s3_credentials.env")
        print("\nExample aws_s3_credentials.env:")
        print("  AWS_ACCESS_KEY_ID=your_access_key")
        print("  AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("  AWS_S3_ENDPOINT=s3.us-east-1.amazonaws.com")
        print("  AWS_DEFAULT_REGION=us-east-1")
        sys.exit(1)

    print(f"\nEndpoint:  {endpoint}")
    print(f"Region:    {region}")
    print(f"AccessKey: {access_key[:8]}...{access_key[-4:] if len(access_key) > 12 else '***'}")

    try:
        import boto3
        from botocore.config import Config

        # S3 client with custom endpoint if needed (for S3-compatible services)
        # Standard AWS S3 uses the default endpoint per region
        if 'amazonaws.com' in endpoint:
            # Standard AWS S3
            client = boto3.client(
                's3',
                region_name=region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=Config(signature_version='s3v4')
            )
        else:
            # Custom S3-compatible endpoint
            client = boto3.client(
                's3',
                region_name=region,
                endpoint_url=f'https://{endpoint}' if not endpoint.startswith('http') else endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                config=Config(signature_version='s3v4')
            )

        print("\n--- Testing connection: list buckets ---")
        response = client.list_buckets()
        buckets = response.get('Buckets', [])
        print(f"SUCCESS: Connected to S3. Found {len(buckets)} bucket(s).")

        if buckets:
            print("\nBuckets:")
            for b in buckets[:20]:
                print(f"  - {b['Name']} (created: {b.get('CreationDate', 'N/A')})")
            if len(buckets) > 20:
                print(f"  ... and {len(buckets) - 20} more")
        else:
            print("  (No buckets yet)")

        # Optional: test HEAD bucket on first bucket if any
        if buckets:
            name = buckets[0]['Name']
            try:
                client.head_bucket(Bucket=name)
                print(f"\n--- HeadBucket({name}) ---")
                print("SUCCESS: Bucket is accessible.")
            except Exception as e:
                print(f"\nHeadBucket warning: {e}")

        print("\n=== AWS S3 connection test PASSED ===")
        return 0

    except Exception as e:
        print(f"\n=== Connection FAILED ===")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
