# Main script for executing the action, used the AWS SDK for python a lot
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
print("Running main action script...")
import boto3
import docker
import os
import re
from base64 import b64decode

# FOR TESTING
from dotenv import load_dotenv

load_dotenv("dev.env")

# Number of 'steps' in this script
N = 1

# Initialise a new boto3 session with the given credentials
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

print(f"Session initialised for {session.profile_name}")

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

# Record created repo arn and uri for later use
ecr_repo_arn = ecr_res["repository"]["repositoryArn"]
ecr_repo_uri = ecr_res["repository"]["repositoryUri"]
print(f"[1/{N}] Created new ECR Repo ({ecr_repo_arn})")

"""
Build and upload the boilerplate image to the ecr
(required to be able to initialise the Lambda function)
"""
# Initialise docker client
docker_client = docker.DockerClient()
print(f"[2/{N}] Initialised Docker Client ")

# Build the boilerplate image
boilerplate_img_tag = ecr_repo_uri + ":latest"
docker_client.images.build(path=".", tag=boilerplate_img_tag)
print(f"[3/{N}] Successfully Built boilerplate image")

# Get an authorisation token (to be able to push with docker to AWS ECR)
ecr_res = ecr_client.get_authorization_token(registryIds=[ecr_repo_uri.split(".")[0]])
ecr_auth = b64decode(ecr_res["authorizationData"][0]["authorizationToken"]).split(b":")
print(
    f"[4/{N}] ECR Auth Token Acquired for user ({ecr_auth[0]}) expiresAt {ecr_res['authorizationData'][0]['expiresAt']}"
)

# Apply acquired token credentials to docker client
docker_res = docker_client.login(
    username=ecr_auth[0].decode("utf-8"),
    password=ecr_auth[1].decode("utf-8"),
    registry=ecr_repo_uri.split("/")[0],
)
print(f"[5/{N}] Authenticated Docker Client (Status: {docker_res['Status']})")

# Push boilerplate image to ECR
for line in docker_client.images.push(
    repository=boilerplate_img_tag, stream=True, decode=True
):
    print("\t" + str(line))

print(f"[6/{N}] Pushed Boilerplate image to new ECR Repo")
