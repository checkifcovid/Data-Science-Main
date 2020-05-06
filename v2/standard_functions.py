"""These functions are standard as per v2"""

import os
import json
import re
import datetime

# the following functions searches for a datetime in a string
def find_date_in_str(string):
    """
    Returns the date from a given string

    Note: datetime format is either ``%Y-%m-%d` or ``%m-%d-%Y`
    """
    pattern = re.compile(
        "[0-9]{4}-[0-9]{2}-[0-9]{2}" +
        "|" + #Or
        "[0-9]{2}-[0-9]{2}-[0-9]{4}"
    )
    dt = pattern.search(string).group()

    if re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dt):
        dt = datetime.datetime.strptime(dt,"%Y-%m-%d")
    else:
        dt = datetime.datetime.strptime(dt,"%m-%d-%Y")
    return dt

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
