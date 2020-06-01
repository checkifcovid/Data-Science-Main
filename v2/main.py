# This file contains the main execution file for the model instantiation etc.

import re
import os
import json
import datetime
import pandas as pd

# View everything:
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100



# Load custom functions
from user_reports_preprocessor import get_preprocessed_df
from utils.split_to_train_test import split_and_balance_with_SMOTE


# ==============================================================================
# Begin
# ==============================================================================

def split_to_train_test():
    """Placeholder for now"""
    # Load the newest dataframe!
    df = get_preprocessed_df()
    y_col = "Diagnosis_result"

    # Consider dropping all those who haven't been tested:
    discrimator_col = "Diagnosis_tested"
    df = df[~df[discrimator_col]!=True] # dropping when not true

    # Make sure your data has the y_col
    assert y_col in df.columns

    # Split
    X = df.drop(columns=y_col).astype(int).fillna(0)
    y = df[y_col].fillna(0).astype(int)


    # Balance with SMOTE
    print("* Balancing data with smote")
    X_train, X_test, y_train, y_test = split_and_balance_with_SMOTE(X,y, test_size=0.5, min_v=2)

    # Now Machine learning can be executed!
    print(f"Completed!\n\nValue counts for y_train:\n{y_train.y.value_counts()};\n\ny_test:\n{pd.Series(y_test).value_counts()}")

# ==============================================================================
# On execution:
# ==============================================================================

if __name__ == '__main__':
    # Do this
    split_to_train_test()
