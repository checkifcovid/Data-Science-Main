# This file contains the main execution file for the model instantiation etc.

import re
import os
import json
import datetime
import pandas as pd

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
from sklearn.externals import joblib

# Load custom functions
from user_reports_preprocessor import get_preprocessed_df
from utils.split_to_train_test import split_and_balance_with_SMOTE
from utils.ml_stats import get_true_positives_etc


# ==============================================================================
# Begin
# ==============================================================================
def load_data():
    """Loads the newest data into the current file"""
    # Load the newest dataframe!
    df = get_preprocessed_df()
    y_col = "Diagnosis_result"

    # Consider dropping all those who haven't been tested:
    discrimator_col = "Diagnosis_tested"
    df.drop(df[df[discrimator_col]!=True].index, inplace=True) # dropping when not true

    # Make sure your data has the y_col
    assert y_col in df.columns
    return df


def split_to_train_test(df):
    """Splits and balances the dataframe"""
    # Load the newest dataframe!
    df = get_preprocessed_df()
    y_col = "Diagnosis_result"

    # Consider dropping all those who haven't been tested:
    discrimator_col = "Diagnosis_tested"
    df.drop(df[df[discrimator_col]!=True].index, inplace=True) # dropping when not true

    # Make sure your data has the y_col
    assert y_col in df.columns

    # Split
    X = df.drop(columns=y_col).astype(int).fillna(0)
    y = df[y_col].fillna(0).astype(int)


    # Balance with SMOTE
    print("* Balancing data with smote")
    X_train, X_test, y_train, y_test = split_and_balance_with_SMOTE(X,y, test_size=0.3, min_v=2)

    # Now Machine learning can be executed!
    # print(f"Completed!\n\nValue counts for y_train:\n{y_train.y.value_counts()};\n\ny_test:\n{pd.Series(y_test).value_counts()}")
    return X_train, X_test, y_train, y_test

def build_model():
    """Build a model and make available to the rest of application."""

    # Instantiate
    model = RandomForestClassifier(max_depth=1, random_state=0)

    return model


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
                "pred_spread": [abs(x[0]-x[1])/2 for x in y_predict_prob]
            }
        }
    }




    # Get feature importance
    feature_importance = {col:val for col,val in zip(X_train.columns, model.feature_importances_)}
    my_model["model_info"].update({"feature_importance":feature_importance})

    return my_model


# ==============================================================================
# On execution:
# ==============================================================================

if __name__ == '__main__':

    # Load the data
    df = load_data()

    # Split the data appropriately
    X_train, X_test, y_train, y_test = split_to_train_test(df)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Begin building models:
    all_models = []

    # Build a model
    model = build_model() # Soon, add params here for smart building. Perhaps loop through as well
    my_model = measure_model_performance(model, X_train, X_test, y_train, y_test)
    all_models.append(my_model)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # save model metrics
    os.makedirs("models",exist_ok=True)
    today = datetime.datetime.today().strftime("%m-%d-%Y")

    all_models_save = [x["model_info"] for x in all_models]
    file_path = f"models/models_info_{today}.json" # fix for proper today

    with open(file_path, "w") as f:
        json.dump(all_models_save,f)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Choose best model here
    best_model = all_models[0]

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Save model
    model_path = f"models/best_model_{today}.joblib"
    print(f"Saving model to {model_path}")
    joblib.dump(best_model, model_path)
