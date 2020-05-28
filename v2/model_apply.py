"""This file applies the most recent model to incoming data."""
import re
import os
import json
import datetime
import pandas as pd

# View everything:
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# Machine Learning externals
import joblib

# Load custom functions
from user_reports_preprocessor import pre_process_data

# ==============================================================================
# Begin
# ==============================================================================

# Get newest model
all_dirs = os.listdir("models")
most_recent = max(all_dirs, key=lambda d: datetime.datetime.strptime(d, '%m-%d-%Y'))
most_recent = os.path.join("models",most_recent)

# get actual content
most_recent_model = os.path.join(most_recent, "best_model.joblib")
most_recent_model_info = os.path.join(most_recent, "model_info.json")

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

# Load the actual model
model = joblib.load(most_recent_model)

# Load the model info
model_info = json.loads(open(most_recent_model_info).read())
my_model_info = [x for x in model_info if x["is_best"]==True][0]


# ==============================================================================

# Load the json input
with open("test/incoming_data_2.json","r") as f:
    my_data = json.load(f)

# Convert to naive json format
for key,value in my_data.items():
    if type(value)==dict:
        my_data.update({key:json.dumps(value)})

# Load to a pandas dataframe
df = pd.DataFrame.from_dict([my_data])
df = pre_process_data(df)

# Match the columns
# print(model_info[0]["feature_importance"].keys())
# ==============================================================================

# Preprocess your input data
None

# ==============================================================================

# Fit to the model
None

# ==============================================================================

# Export to json format
None
