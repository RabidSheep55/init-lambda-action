# Containerised Lambda function init action

This action provisions and initialises a new containerised lambda function on AWS. It will automatically create and link the following services:

- A new ECR Repository
  - Initialised with a placeholder image (built by the action using the docker apk for python)
- A new Lambda Function
  - A new execution for the function
- A new IAM Policy strictly for the CI/CD Pipeline of this new function with the following permissions:
  - Upload new image to the newly created ECR Repo
  - UpdateFunctionCode for the newly create Lambda function
- A new IAM User, given the newly created policy, and it's appropriate AWS Access key ID and SECRET, to be assumed by the CI/CD Pipeline

## Inputs

## `new-function-name`

**Required** Name of the lambda function to be created. This should be given in PascalCase. _Note: AWS ECR only allows repositories to be named in kebab-case, which is why this action will automatically convert it_.

## `aws-access-key-id` and `aws-secret-access-key`

**Required** AWS Access key for a user with the necessary permissions

<details>
<summary>Required IAM User Permissions</summary>
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:CreatePolicy",
                "lambda:CreateFunction",
                "ecr:CreateRepository",
                "iam:AttachUserPolicy",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:DescribeRegistry",
                "ecr:GetRepositoryPolicy",
                "ecr:SetRepositoryPolicy",
                "ecr:UploadLayerPart",,
                "ecr:CompleteLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "iam:CreateRole",
                "iam:CreateUser",
                "iam:CreateAccessKey",
                "iam:GetUser",
                "iam:AttachRolePolicy"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "lambda.amazonaws.com"
                }
            }
        }
    ]
}
```
</details>

## Outputs

TODO

## Example usage

```yaml
- name: Initialise Lambda function and associated resources
  uses: actions/init-lambda-function@v1
  id: initialise-lambda
  with:
    new-function-name: ${{ github.event.repository.name }}
    aws-access-key-id: ${{ secrets.INIT_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.INIT_SECRET_ACCESS_KEY }}
    aws-region: eu-west-2
```

## Resources (for me)

- [Python Container Action Template](https://github.com/jacobtomlinson/python-container-action)
- [Boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Creating a docker container action](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
