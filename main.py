# Main script for executing the action, used the AWS SDK for python a lot
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
print("[MAIN] Running main action script...")
import boto3
import os
import re

# Number of 'steps' in this script
N = 1

# Initialise a new boto3 session with the given credentials
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

print(f"[MAIN] Session initialised for {session.profile_name}")

# Get the name of the function to initialise
new_function_name = os.getenv("NEW_FUNCTION_NAME")

# ECR Repo names need to be in kebab-case
new_ecr_repo_name = re.sub(r"(?<!^)(?=[A-Z])", "-", new_function_name).lower()

"""
Create a new ECR Repository
"""
ecr_client = session.client("ecr")

ecr_res = ecr_client.create_repository(
    repositoryName=new_ecr_repo_name,
    imageTagMutability="MUTABLE",
    imageScanningConfiguration={"scanOnPush": False},
)

# Record created repo arn for later use
ecr_repo_arn = ecr_res["repository"]["respositoryArn"]
print(f"[MAIN 1/{N}] Created new ECR Repo ({ecr_repo_arn})")
