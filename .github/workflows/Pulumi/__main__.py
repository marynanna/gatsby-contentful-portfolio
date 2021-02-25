import pulumi
from pulumi_aws import s3

import json

# Create S3 Bucket
bucket = s3.Bucket('my-bucket',
	acl="public-read",
	website=s3.BucketWebsiteArgs(
		index_document="index.html",
		error_document="error.html",
		))

# Outputs
# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)