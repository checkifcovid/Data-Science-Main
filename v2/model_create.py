"""This file instantiates the model – primarily sklearn library"""
import re
import os
import json
import datetime
import pandas as pd
import boto3
import pickle

# View everything:
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100

# Machine Learning models
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression, BayesianRidge
from sklearn.ensemble import RandomForestClassifier

# Machine Learning metrics
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss, precision_score, recall_score, f1_score

# Machine Learning externals
import joblib

# Load custom functions
from utils.get_creds import get_ML_aws_creds
from user_reports_preprocessor import get_preprocessed_df
from utils.smote import split_to_train_test_with_SMOTE, balance_X_y_actual_with_SMOTE
from utils.ml_stats import get_true_positives_etc


# ==============================================================================
# Begin
# ==============================================================================
def load_data():
    """Loads the newest data into the current file"""
    # Load the newest dataframe!
    df = get_preprocessed_df()
    y_col = "diagnosis_result"

    # Consider dropping all those who haven't been tested:
    discrimator_col = "diagnosis_tested"
    df.drop(df[df[discrimator_col]!=True].index, inplace=True) # dropping when not true

    # Make sure your data has the y_col
    assert y_col in df.columns
    return df

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def split_to_train_test(df, y_col = "diagnosis_result", train_or_actual="train"):
    """Splits and balances the dataframe"""


    # Consider dropping all those who haven't been tested:
    discrimator_col = "diagnosis_tested"
    df.drop(df[df[discrimator_col]!=True].index, inplace=True) # dropping when not true

    # Make sure your data has the y_col
    assert y_col in df.columns

    # Split
    X = df.drop(columns=y_col).astype(int).fillna(0)
    y = df[y_col].fillna(0).astype(int)


    # Balance with SMOTE
    print("* Balancing data with smote")

    # If splitting for train test
    if train_or_actual=="train":
        X_train, X_test, y_train, y_test = split_to_train_test_with_SMOTE(X,y, test_size=0.3, min_v=2)
        return X_train, X_test, y_train, y_test

    # If splitting all data
    elif train_or_actual =="actual":
        X_actual, y_actual = balance_X_y_actual_with_SMOTE(X,y)
        return X_actual, y_actual

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def build_model():
    """Build a model and make available to the rest of application."""

    # Instantiate
    model = RandomForestClassifier(max_depth=1, random_state=0)

    return model

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def measure_model_performance(model, X_train, X_test, y_train, y_test):

    # Fit – without cross validating
    model.fit(X_train, y_train.values.ravel())

    # Predict
    y_predict = model.predict(X_test)
    y_predict_prob = model.predict_proba(X_test)


    # Save model
    my_model = {
        "model":model,
        "model_info":{
            "date_instantiated":datetime.datetime.now(),
            "model_name":model.__class__.__name__,
            "params":model.get_params(),

            # meta stuf
            "meta":{
                # "n_samples_original":len(df),
                "n_samples_train":len(y_train),
                "n_samples_test":len(y_test),
                "SMOTE":True, #Toggle manually for now
            },

            # Save metrics
            "metrics":{
                "accuracy": accuracy_score(y_test, y_predict),
                "balanced_accuracy": balanced_accuracy_score(y_test, y_predict),
                "log_loss": log_loss(y_test, y_predict),
                "precision_score":precision_score(y_test,y_predict),
                "recall_score":recall_score(y_test,y_predict),
                "f1_score": f1_score(y_test, y_predict),
                "granular_prediction_metrics":get_true_positives_etc(y_test, y_predict, True),
                "pred_spread_of_test_data": [abs(x[0]-x[1])/2 for x in y_predict_prob]
            }
        }
    }




    # Get feature importance
    feature_importance = {col:val for col,val in zip(X_train.columns, model.feature_importances_)}
    my_model["model_info"].update({"feature_importance":feature_importance})

    return my_model

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -



# ==============================================================================
# On execution:
# ==============================================================================

if __name__ == '__main__':

    # Load the data
    df = load_data()

    # Split the data appropriately
    X_train, X_test, y_train, y_test = split_to_train_test(df, y_col = "diagnosis_result", train_or_actual="train")

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Begin building models:
    all_models = []

    # Build a model
    model = build_model() # Soon, add params here for smart building. Perhaps loop through as well
    my_model = measure_model_performance(model, X_train, X_test, y_train, y_test)
    all_models.append(my_model)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Score + Evaluate best model
    for model in all_models:
        if model: # Is the best
            model["model_info"].update({"is_best":True})

        else:
            model["model_info"].update({"is_best":False})

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Select best model + Refit to all data

    # --------------------------------------------------------------------------
    # REVIEW NEEDED: Is this appropriate for the time being?
    # --------------------------------------------------------------------------

    # Resplit
    X_actual,y_actual = split_to_train_test(df, y_col = "diagnosis_result", train_or_actual="actual")

    #   FUTURE: There has to be a neater one-line for this...
    for x in all_models:
        if x["model_info"]["is_best"]==True:

            # refit
            model_refit = x["model"].fit(X_actual, y_actual.values.ravel())
            x.update({"model (refit)": model_refit})

            # Save the best model with all of its metadata
            best_model = x


    # ==========================================================================
    # Save the model to s3
    # ==========================================================================

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

    # save model metrics
    today = datetime.datetime.today().strftime("%m-%d-%Y")

    # os.makedirs(os.path.join("models",today),exist_ok=True)

    all_models_save = [x["model_info"] for x in all_models]
    model_metrics_path = os.path.join("models",today, "model_info.json")

    # Model metrics
    bucket.put_object(
        Body = bytes(json.dumps(all_models_save).encode('UTF-8')),
        Key=model_metrics_path
        )

    # Save model
    model_path =  os.path.join("models",today, "best_model.pkl")
    bucket.put_object(
        Body = pickle.dumps(best_model),
        Key=model_path
        )

    # Alternatively
    # joblib.dump(best_model, model_path)
    # bucket.upload_file(model_path, model_path)
    # os.remove(model_path)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -






    # --------------------------------------------------------------------------
    # Save the model to s3
    # --------------------------------------------------------------------------


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # First model metrics
    #

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
