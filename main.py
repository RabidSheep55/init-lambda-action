# Main script for executing the action, used the AWS SDK for python a lot
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
import boto3
import os

print("Running action python script")

# Inputs to the function are supplied through env variables
print(f"::set-output name=test::{dict(os.environ)}")
