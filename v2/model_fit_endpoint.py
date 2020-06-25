"""This file applies the most recent model to incoming data."""
import re
import os
import sys
import json
import datetime
import pandas as pd
import boto3
import pickle

# View everything:
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# Machine Learning externals
import joblib

# Load custom functions
from user_reports_preprocessor import pre_process_data, double_check_conversion_of_booleans
from utils.get_creds import get_ML_aws_creds

# Store data in this temp folder
os.makedirs("data/tmp",exist_ok=True)

# ==============================================================================
# Load the s3 Bucket
# ==============================================================================

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

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Get the most recent file
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
    bucket.download_file(file_name, f"data/tmp/{x}")

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Now load the data from these files
model_raw = pickle.load(open("data/tmp/best_model.pkl", "rb"))

# This model is the training model
model = model_raw["model"]

# WE WANT THIS SECOND ONE FOR NOW – GIVEN THE SPARSENESS OF DATA...
# This model is the training model refit to oversampled data – all as x_train
model = model_raw["model (refit)"]

# Load the model info
model_info = model_raw["model_info"]


# ==============================================================================

# HERE IS WHERE THE JSON FROM THE REQUEST ENTERS
# Load the json input
with open("test/incoming_data.json","r") as f:
    my_data = json.load(f)

# Convert to naive json format
for key,value in my_data.items():
    if type(value)==dict:
        my_data.update({key:json.dumps(value)})

# Load to a pandas dataframe
df = pd.DataFrame.from_dict([my_data])

# ==============================================================================
# Preprocess your input data
df = pre_process_data(df)
df = double_check_conversion_of_booleans(df)


# Match the columns
curr_columns = model_info["feature_importance"].keys()
new_cols = [x for x in curr_columns if x not in df.columns]
for col in new_cols:
    if "N_days" in col:
        df[col] = 0 # How do we fill these in?
    else:
        df[col] = False

drop_cols = [x for x in df.columns if x not in curr_columns]
df.drop(columns = drop_cols, inplace=True)

# ==============================================================================

# Fit to the model
prediction = model.predict(df)

predict_prob = model.predict_proba(df)

# ==============================================================================

# HERE IS WHERE THE JSON FOR THE RESPONSE EXITS
# Export to json format
my_prediction = {
    "diagnosis_positive": bool(prediction),
    "pred_spread": [abs(x[0]-x[1])/2 for x in predict_prob][0],
    "model_name": model_info["model_name"],
    "model_training_info":model_info["meta"],
    "model_metrics":model_info["metrics"],
    "feature_importance":model_info["feature_importance"]
}

print("prediction is complete.")
# Return this as a json response to the application
with open("test/my_prediction.json","w") as f:
    json.dump(my_prediction,f)
