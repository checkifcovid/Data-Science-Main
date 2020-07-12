"""
Downloads the latest model from s3 to the server.

* This program needs to run after a new model has been trained.

"""

import re
import os
import sys
sys.path.append(".")
import json
import datetime
import boto3
import pickle
# Machine Learning externals
import joblib

# Load custom functions
from utils.get_creds import get_ML_aws_creds

# Store data in this temp folder
os.makedirs("data/tmp",exist_ok=True)

# ==============================================================================
# Load the s3 Bucket
# ==============================================================================

def get_most_recent_model():
    """
    Downloads the latest model from s3 to the server.
    """
    # Credentials
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = get_ML_aws_creds()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Bucket Name
    if os.environ.get("ML_BUCKET_NAME"):
        BUCKET_NAME = os.environ.get("ML_BUCKET_NAME")

    else:
        aws_bucket_path = "../secret/ml_aws_bucket_info.json"
        bucket_info = json.loads(open(aws_bucket_path).read())
        BUCKET_NAME = bucket_info["BUCKET_NAME"]

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Load the s3 session
    session = boto3.Session(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)


    # ==============================================================================
    # Get the most recent file
    # ==============================================================================

    all_files = [x.key for x in bucket.objects.all()]
    all_dates = [re.search("[0-9]{2}-[0-9]{2}-[0-9]{4}",x).group() for x in all_files]
    most_recent_dates = max(all_dates, key=lambda d: datetime.datetime.strptime(d, '%m-%d-%Y'))

    # Get the most recent files
    most_recent = [x for x in all_files if most_recent_dates in x]
    most_recent = {x.split("/")[-1]:x for x in most_recent}


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


    # download content to a temp folder
    for x in ["best_model.pkl", "model_info.json"]:
        file_name = most_recent[x]
        print(f"downloading f{file_name}")
        bucket.download_file(file_name, f"data/tmp/{x}")



# ------------------------------------------------------------------------------


if __name__ == '__main__':
    get_most_recent_model()
