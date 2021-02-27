import pulumi
import pulumi_aws as aws

import json
import mimetypes
import os
# Create S3 Bucket
bucket = aws.s3.Bucket('my-bucket-github-actions-marynenko',
	acl="public-read",
	website= aws.s3.BucketWebsiteArgs(
		index_document="index.html",
		error_document="404.html",
		))

# Outputs
# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

content_dir = "public"

for file in os.listdir(content_dir):
    filepath = os.path.join(content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    obj = s3.BucketObject(file,
        bucket=bucket.id,
        source=FileAsset(filepath),
        content_type=mime_type)

# Create Cloudfront
s3_origin_id = "myS3Origin-github-actions-marynenko"
s3_distribution = aws.cloudfront.Distribution("s3Distribution-test",
    origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=bucket.bucket_regional_domain_name,
        origin_id=s3_origin_id,
    )],
    enabled=True,
    default_root_object="index.html",

    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=[
            "GET",
            "HEAD",
        ],
        cached_methods=[
            "GET",
            "HEAD",
        ],
        target_origin_id=s3_origin_id,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none",
            ),
        ),
        viewer_protocol_policy="allow-all",
        min_ttl=0,
        default_ttl=3600,
        max_ttl=86400,
    ),
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="whitelist",
            locations=[
                "US",
                "CA",
                "GB",
                "DE",
            ],
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        cloudfront_default_certificate=True,
    ))

pulumi.export('cloudfrontid', s3_origin_id)