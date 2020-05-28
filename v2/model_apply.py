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
model_raw = joblib.load(most_recent_model)[0]
model = model_raw["model"]

# Load the model info
model_info = model_raw["model_info"]


# ==============================================================================

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
