import json
import re
import os
import boto3
import botocore

# Import custom stuff
from standard_functions import find_date_in_str, get_aws_creds


# Credentials
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = get_aws_creds()

# Bucket info
aws_bucket_path = "../secret/aws_bucket_info.json"

try:
    # Try loading secret file
    bucket_info = json.loads(open(aws_bucket_path).read())
    # Get the bucket name
    BUCKET_NAME = bucket_info["BUCKET_NAME"]

except FileNotFoundError:
    print(f"** uh oh **\nthe file `{aws_bucket_path}` cannot be found... (make sure the local route works?\n**")
    raise  SystemExit('Exiting execution...')

# Load the s3 session
session = boto3.Session(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)
s3 = session.resource('s3')

# Load the bucket
bucket = s3.Bucket(BUCKET_NAME)

# Download the most recent file
csv_keys = [x.key for x in bucket.objects.all() if x.key.endswith(".csv")]
csv_keys = {find_date_in_str(x):x for x in csv_keys}

# Get the newest file
newest_key = max(csv_keys.keys())
newest_csv = csv_keys[newest_key]

# Print
newest_key = newest_key.strftime('%m-%d-%Y')
print(f"Newest file was added on {newest_key}.")

# Save the file
os.makedirs("data",exist_ok=True)
file_name = f"covid-user-reports {newest_key}.csv"

# Download
save_path = os.path.join("data",file_name)
try:
    s3.Bucket(BUCKET_NAME).download_file(newest_csv, save_path)
    print(f"data was downloaded succesfully and can be found at `{save_path}`")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise #"cannot download and save file"
