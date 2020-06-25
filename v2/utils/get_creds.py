import os
import json
# from pathlib import Path


# Loads aws credentials
def get_aws_creds(aws_creds_path='../secret/aws_credentials.json'):
    """
    returns (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    Note: Tries to find as os variables, else, from secret path
    """

    # Try to get them as environment variables
    if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
        print("loading aws creds from local")
        AWS_ACCESS_KEY_ID =  os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    elif os.path.isfile(aws_creds_path):
        # Try loading secret file
        with open(aws_creds_path,"r") as f:
            aws_creds = json.load(f)

        print("loading aws creds from `secret`")
        # Set variables
        AWS_ACCESS_KEY_ID = aws_creds["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = aws_creds["AWS_SECRET_ACCESS_KEY"]
    else:
        # Alternatively, use environmental variables
        print("Not found....")
        return None

    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY



# Load AWS Credentials, but for ML – same code, but different function name
def get_ML_aws_creds(aws_creds_path='../secret/ml_aws_credentials.json'):
    """
    returns (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    Note: Tries to find as os variables, else, from secret path
    """

    # Try to get them as environment variables
    if os.environ.get('ML_AWS_ACCESS_KEY_ID') and os.environ.get('ML_AWS_SECRET_ACCESS_KEY'):
        print("loading aws creds from local")
        AWS_ACCESS_KEY_ID =  os.environ.get('ML_AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('ML_AWS_SECRET_ACCESS_KEY')

    elif os.path.isfile(aws_creds_path):
        # Try loading secret file
        with open(aws_creds_path,"r") as f:
            aws_creds = json.load(f)

        print("loading aws creds from `secret`")
        # Set variables
        AWS_ACCESS_KEY_ID = aws_creds["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = aws_creds["AWS_SECRET_ACCESS_KEY"]
    else:
        # Alternatively, use environmental variables
        print("Not found....")
        return None

    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
