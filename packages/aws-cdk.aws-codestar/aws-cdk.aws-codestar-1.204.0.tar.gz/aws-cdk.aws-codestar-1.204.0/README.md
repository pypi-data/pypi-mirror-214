# AWS::CodeStar Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

## GitHub Repository

To create a new GitHub Repository and commit the assets from S3 bucket into the repository after it is created:

```python
import aws_cdk.aws_codestar as codestar
import aws_cdk.aws_s3 as s3


codestar.GitHubRepository(self, "GitHubRepo",
    owner="aws",
    repository_name="aws-cdk",
    access_token=SecretValue.secrets_manager("my-github-token",
        json_field="token"
    ),
    contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "bucket-name"),
    contents_key="import.zip"
)
```

## Update or Delete the GitHubRepository

At this moment, updates to the `GitHubRepository` are not supported and the repository will not be deleted upon the deletion of the CloudFormation stack. You will need to update or delete the GitHub repository manually.
