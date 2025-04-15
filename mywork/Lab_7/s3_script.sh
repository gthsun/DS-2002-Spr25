#!/bin/bash

# check if correct number of arguments are provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 <local_file_path> <bucket_name> <expiration_time_in_seconds>"
    echo "Example: $0 document.pdf my-private-bucket 604800"
    exit 1
fi

FILE="$1"
BUCKET="$2"
EXPIRATION="$3"

# Get the filename from path
FILENAME=$(basename "$FILE")

# upload file to S3
echo "Uploading $FILE to s3://$BUCKET/$FILENAME..."
aws s3 cp "$FILE" "s3://$BUCKET/$FILENAME"

# generate the presigned URL
echo "Generating presigned URL with expiration of $EXPIRATION seconds..."
PRESIGNED_URL=$(aws s3 presign --expires-in "$EXPIRATION" "s3://$BUCKET/$FILENAME")

echo "File uploaded successfully!!!"
echo "Presigned URL (expires in $EXPIRATION seconds):"
echo "$PRESIGNED_URL"