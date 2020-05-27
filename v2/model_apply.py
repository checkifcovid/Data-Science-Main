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
from user_reports_preprocessor import get_preprocessed_df

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

# ==============================================================================

# Load the json input
my_data = {}

# ==============================================================================

# Preprocess your input data
None

# ==============================================================================

# Fit to the model
None

# ==============================================================================

# Export to json format
None
