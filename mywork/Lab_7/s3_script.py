#!/opt/homebrew/bin/python3

import argparse
import boto3
import requests
import sys
from pathlib import Path
from botocore.exceptions import ClientError

# Argument parser setup
parser = argparse.ArgumentParser(
    description="Fetch a file from a URL, upload it to an S3 bucket, and return a presigned URL."
)
parser.add_argument("url", help="Direct URL to download file from")
parser.add_argument("bucket", help="S3 bucket to upload file to")
parser.add_argument("expiration", type=int, help="Expiration time (in seconds) for the presigned URL")
parser.add_argument("--filename", help="Custom name for saved/uploaded file")
parser.add_argument("--keep", action="store_true", help="Keep the file locally after upload")
args = parser.parse_args()

# determine filename
filename = args.filename if args.filename else Path(args.url).name
filepath = Path(filename)

# download the file
try:
    print(f"Downloading from {args.url}...")
    response = requests.get(args.url)
    response.raise_for_status()
    filepath.write_bytes(response.content)
    print(f"File was saved as '{filename}'")
except Exception as e:
    print(f"Error downloading the file: {e}")
    sys.exit(1)

# upload to the S3 bucket
s3 = boto3.client("s3")
try:
    print(f"Uploading '{filename}' to bucket '{args.bucket}'...")
    s3.upload_file(str(filepath), args.bucket, filename)
    print("Upload was successful!!!")
except ClientError as e:
    print(f"Upload failed: {e}")
    sys.exit(1)

# generate the presigned URL
try:
    print(f"Creating a presigned URL that's valid for {args.expiration} seconds...")
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": args.bucket,
            "Key": filename,
            "ResponseContentDisposition": "inline",
            "ResponseContentType": "image/jpeg"
        },
        ExpiresIn=args.expiration
    )
    print("Presigned URL:")
    print(url)
except ClientError as e:
    print(f"Failed to generate a presigned URL: {e}")
    sys.exit(1)

# Cleanup by getting rid of local files
if not args.keep:
    try:
        filepath.unlink()
        print(f"Removed local file: {filename}")
    except Exception as e:
        print(f"Could not delete local file: {e}")
