"""This file applies the most recent model to incoming data."""
import re
import os
import sys
sys.path.append(".")
from pathlib import Path
import json
import datetime
import pandas as pd
import boto3
import pickle

# Machine Learning externals
import joblib

# Load custom functions
from utils.user_reports_preprocessor import pre_process_data, double_check_conversion_of_booleans


# # View everything:
# pd.options.display.max_rows = 100
# pd.options.display.max_columns = 100


# ==============================================================================
# 1. Load the newest model
# ==============================================================================

def load_model(model_path = Path("data/tmp/best_model.pkl"), refitted=True):
    """
    Load the newest model.

    ----
    : param model_path : the path to the newest model (.pkl format)
    : param refitted : bool, choose the refited model (instead of standard practice – best performing train model)

    : return : model (sickit learn), model_info (dictionary)
    """
    # Load into a "raw" object which will be used to access further components
    model_raw = pickle.load(open(model_path, "rb"))

    # This model is the one used for training
    model = model_raw["model"]

    # When the best performing model is chosen, it is re-fitted to an oversampled representation
    # of ALL the data. (Not best practice...) Given the sparseness of our data, this is a suitable
    # working solution.
    model = model_raw["model (refit)"] # WE WANT THIS SECOND ONE FOR NOW – GIVEN THE SPARSENESS OF DATA...

    # Load the model info (model metadata)
    model_info = model_raw["model_info"]

    # return both...
    return model, model_info


# ==============================================================================
# 2. Load incoming data
# ==============================================================================

def prepare_incoming_data(data, curr_columns):
    """
    Incoming data must match schema of model.
    ----
    :param data: dictionary
    :returns: a df suitable to fit a model prediction
    ----
    Want: Ideally, this function accepts a model's schema (json format) as input. Data could be fit to that schema...
    ----
    """

    # If incoming data contains dictionaries as values... Convert to naive json format
    # TO DO: replace with pandas unpacking nested json method...
    for key,value in data.items():
        if type(value)==dict:
            data.update({key:json.dumps(value)})

    # Load to a pandas dataframe
    df = pd.DataFrame.from_dict([data])

    # ==============================================================================
    # Preprocess your input data
    df = pre_process_data(df)
    df = double_check_conversion_of_booleans(df)

    # Match the columns

    new_cols = [x for x in curr_columns if x not in df.columns]
    for col in new_cols:
        if "N_days" in col:
            df[col] = 0 # How do we fill these in?
        else:
            df[col] = False

    drop_cols = [x for x in df.columns if x not in curr_columns]
    df.drop(columns = drop_cols, inplace=True)

    return df

# ==============================================================================
# 3. Put it all together
# ==============================================================================

def fit_to_model(my_data=None):
    """
    Input data -- get a prediction.

    ----

    Note: If no data is loaded, program will load prepopulated data (good for testing)
    """

    # 1. Load the model & model info
    model, model_info = load_model()

    # 2. Get the current columns from the model
    curr_columns = model_info["feature_importance"].keys()

    # 3. Prepare incoming data

    # 3A. If no data, load some prepopulated data for testing
    if not my_data:
        load_path = Path("test/incoming_data.json")
        print(f" * loading prepopulated data from {load_path}")

        with open(load_path,"r") as f:
            my_data = json.load(f)

    # 3B. Make sure your data is correct
    assert type(my_data) == dict

    # 3C. Actually prepare
    df = prepare_incoming_data(my_data, curr_columns)

    # 4. Fit to model
    prediction = model.predict(df)
    predict_prob = model.predict_proba(df)

    # print...
    print(predict_prob)
    # 5. Export predictions to json format
    # NOTE: This needs better documentation
    my_prediction = {
        "diagnosis_positive": bool(prediction),
        "probability_diagnosis_positive": predict_prob[0][1], # prob class 1 – True
        "pred_spread": [abs(x[0]-x[1])/2 for x in predict_prob][0],
        "model_name": model_info["model_name"],
        "model_training_info":model_info["meta"],
        "model_metrics":model_info["metrics"],
        "feature_importance":model_info["feature_importance"]
    }

    # 6. Done!
    # Return this as a json response to the application
    return my_prediction


# ==============================================================================

if __name__ == "__main__":

    # Run with blank data
    my_prediction = fit_to_model()

    # Save locally
    save_path = Path("test/my_prediction.json")
    print(f" * saving model predictions locally to {save_path}")

    with open(save_path,"w") as f:
        json.dump(my_prediction,f)
