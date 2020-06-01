# PURPOSE: This program preprocesses existing data for machine learning training.
# NOTE: This program is not fit for production and has not been tested on "live" data
#       meaning, it will cause errors if used on new observations for the purpose
#       of fitting a prediction. (YB 05/10/2020)

import re
import os
import json
import datetime
import pandas as pd

# View everything:
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100


# Import custom functions
from utils.path import get_newest_file
from utils.datetime import find_date_in_str

# ==============================================================================
# Define additional functions
# ==============================================================================


def extract_from_dict(my_dict):
    """Extracts data from a nested structure"""
    if type(my_dict)!=dict:
        my_dict = json.loads(my_dict)
    # Begin extracting values
    new_dict = {}
    for key, value in my_dict.items():
        if type(value)==dict:
            new_dict[key] = list(value.values())[0]
        else:
            new_dict[key] = value
    return new_dict


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# There may be others...

# ==============================================================================
# Begin loading content
# ==============================================================================


# Load the newest file
def load_newest_data():
    newest_csv = get_newest_file("data", ".csv")
    print(f"* Loading data from `{newest_csv}`")
    df = pd.read_csv(newest_csv)
    return df

def pre_process_data(df):
    # Clean up column names
    df.columns = df.columns.str.replace(" \([A-Z]\)","").str.lower()

    df.drop(columns=["surveryid","userid"],inplace=True, errors="ignore")

    # rename any columns necessary:
    rename_dict = {"postcode":"postalcode", "country_code":"countrycode"}
    df.rename(columns=rename_dict, inplace=True)

    # Nested dictionaries:
    #   The columns contain dictionaries with key value pairs as additional columns.
    #   Ex. {"color":"red","shape":"circle"}
    nested_cols = ["calendar","diagnosis"]
    for col in nested_cols:
        df_temp = df[col].apply(extract_from_dict).apply(pd.Series).add_prefix(f"{col}_")
        df = df.merge(df_temp, left_index=True, right_index=True)
        df.drop(columns=col,inplace=True) #dynamically drop them

    del df_temp # stay neat


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Flat dictionary – with decoding
    #   These are very similar to above, except
    #   single quotation mark \' must be substituted for double \"
    nested_cols_decoded = ["symptoms"]
    for col in nested_cols_decoded:
        df_temp = df[col].replace({'\'': '"',"True":"true","False":"false"}, regex=True).apply(json.loads).apply(pd.Series).add_prefix(f"{col}_")
        df_temp.fillna(False,inplace=True)
        df = df.merge(df_temp, left_index=True, right_index=True)
        df.drop(columns=col,inplace=True) #dynamically drop them

    del df_temp # stay neat

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    # ==============================================================================
    # Convert dtypes:
    # ==============================================================================

    # Q: Should we include the time of day the user filled out the survey?
    #   Current method localizes datetime, so is not available without modifying code 1st.

    # ------------------------------------------------------------------------------

    # Date columns contain "Date" or "Calendar"
    dt_columns = [x for x in df.columns if any(y in x for y in ["date","calendar"])]
    for col in dt_columns:
        df[col] = pd.to_datetime(df[col]).dt.tz_localize(None) # We don't want timezones...

    del dt_columns # stay neat

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Converting to categorical data lessens the disk space of the dataframe.
    categorical_columns = ["age","gender","country","postalcode"]
    for col in categorical_columns:
        df[col] = pd.Categorical(df[col])

    del categorical_columns # stay neat

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Convert diagnosis.
    #   Map this dictionary to all relevant columns
    d_map = {
        "yes":True,
        "no":False,
        "positive":True,
        "negative":False,
        "waiting for results":None,
        "waiting":None,
        }
    # Get the columns
    diagnosies_cols = [x for x in df.columns if "diagnosis" in x]
    df[diagnosies_cols] = df[diagnosies_cols].replace(d_map )

    # * NOTE: * Eventually, write a test to determine if diagnosis cols were correctly formatted

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Additional columns to ignore? (Manual process...)
    drop_cols = ["countrycode"]
    df.drop(columns=drop_cols,inplace=True)

    del drop_cols #stay neat


    # ==============================================================================
    # Encode Data
    # ==============================================================================

    # GENDER
    #   Q: Do we convert gender to numerically encoded values? or boolean as cols...
    #   df['Gender'] = df['Gender'].map({"Male":0,"Female":1, "Non-binary":2, "Others":3})


    # DATETIME
    #   Create the following new fields:
    #       * N_days_Onset_to_Test: Clinical term: onset. (This is the most important for contact tracing)
    #       * N_days_Onset_to_Subside: Clinical term: resolution
    #       * N_days_Onset_to_Now: Symptoms subsiding, you might still be infectious


    # ZIP CODES
    #   SKIP Postal Codes for now...
    #       * Consider mapping to Lat Long using GMaps API – Geoencoding
    #       * Could eventually infer or lookup important demographic data such as population density etc.

    # ------------------------------------------------------------------------------

    # Encode Categorical Data
    cat_cols = [
        "age", # Is buckets, good.
        "country", # Mostly North America
        "gender", # Male / Female / Non-Binary / Others --> Improper encoding can cause errors
        "reportsource", # Should be uniform
    ]

    # Use Dummy variables. (Include na – for now)
    for col in cat_cols:
        # If not a column, carry on...
        if col not in df.columns:
            continue

        df_temp = pd.get_dummies(df[col], prefix=col, dtype=bool,dummy_na=True)
        df = df.merge(df_temp, left_index=True, right_index=True)
        df.drop(columns=col, inplace=True) #dynamically drop them

    del df_temp # stay neat

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Date Diffs
    # There should be 3 columns for calendar:
    #   * ['Calendar_onset', 'Calendar_subsided', 'Calendar_tested']
    #   * Let's asssume these columns aren't renamed at any point
    #   * Also, assume there are only 3 columns... (and not more)

    dt_columns = [x for x in df.columns if any(y in x for y in ["date","calendar"])]


    # Create the new dt columns here
    dt_dict = {
        # Format is x[0] - x[1]
        #   ex: N_days_Onset_to_Test = Calendar_tested - Calendar_onset
        "n_days_onset_to_test": ["calendar_tested","calendar_onset"],
        "n_days_onset_to_subside": ["calendar_subsided","calendar_onset"],
        "n_days_onset_to_now": ["reportdate","calendar_onset"]
        }

    for key, value in dt_dict.items():
        if all([x in value for x in df.columns]):
            df[key] = (df[value[0]] - df[value[1]]).dt.days


    # Done with the datetime columns – drop them
    df.drop(columns=dt_columns, errors="ignore", inplace=True)
    del dt_columns #needed_dt_columns, custom_dt_columns # stay neat


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Also, soon drop all entries whose zip code is death valley
    # (Used for testing...)
    # df = df[df["PostalCode"]!="92328"] #Make sure to omit soon!

    # Postal codes!
    # SKIP FOR NOW
    df.drop(columns="postalcode", errors="ignore", inplace=True)

    # Finally
    return df

# ==============================================================================
# Done!
# ==============================================================================

# One option would be to save the file locally and allow another program to load.
# There might be some issues with encoding & decoding.
# As an alternative, create a function which returns the pandas df

def double_check_conversion_of_booleans(df):
    """will run through and return all string booleans to proper booleans"""
    for col, dtype in df.dtypes.items():
        if dtype=="object":
            col_values = df[col].values
            # If a number
            if all([re.search("[0-9]+",x) for x in col_values]):
                df[col] = df[col].astype(int)
            # Otherwise...
            if all([re.search("false|true",x) for x in col_values]):
                df[col] = df[col].astype(bool)

    #Done!
    return df

# ------------------------------------------------------------------------------

def get_preprocessed_df():
    """Loads the dataframe directly from call of function"""
    df = load_newest_data()
    df = pre_process_data(df)
    return df

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':

    # Only save if the actual program is run through the .py file.
    df = get_preprocessed_df()

    # Get the name of the newest file etc.
    newest_csv = get_newest_file("data", ".csv")
    newest_file_dt = find_date_in_str(newest_csv).strftime("%m-%d-%Y")
    output_file_name = f"preprocessed data {newest_file_dt}.csv"
    os.makedirs("data/preprocessed", exist_ok=True) # Make the directory
    output_file_name = os.path.join("data/preprocessed",output_file_name)

    print(f"* Saving preprocessed data to `{output_file_name}`")
    df.to_csv(output_file_name, index=False) # save!
