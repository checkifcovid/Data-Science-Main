import os
import json

# Loads aws credentials
def get_aws_creds(aws_creds_path='../secret/aws_credentials.json'):
    """
    returns (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    Note: tries to find from aws_creds_path - otherwise, os variables
    """
    if os.path.isfile(aws_creds_path):
        # Try loading secret file
        with open(aws_creds_path,"r") as f:
            aws_creds = json.load(f)
        print("loading aws creds from `secret`")
        # Set variables
        AWS_ACCESS_KEY_ID = aws_creds["aws_access_key_id"]
        AWS_SECRET_ACCESS_KEY = aws_creds["aws_secret_access_key"]
    else:
        # Alternatively, use environmental variables
        print("loading aws creds from `environmental vars`")
        AWS_ACCESS_KEY_ID = os.environ.get("aws_access_key_id")
        AWS_SECRET_ACCESS_KEY = os.environ.get("aws_secret_access_key")

    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
