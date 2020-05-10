import re
import os
import datetime
import pandas as pd

# Import custom functions
from standard_functions.path import get_newest_file

# Load the newest file
newest_csv = get_newest_file("data", ".csv")
df = pd.read_csv(newest_csv)


# Clean up column names
df.columns = df.columns.str.replace(" \([A-Z]\)","")
df.drop(columns=["SurveyID","UserID"],inplace=True, errors="ignore")

# # Nested dictionaries
# for col in ["Calendar","Diagnosis"]:
#     df_temp = df[col].apply(extract_from_dict).apply(pd.Series).add_prefix(f"{col}_")
#     df = df.merge(df_temp, left_index=True, right_index=True)
#     df.drop(columns=col,inplace=True)
#
# #Flat dictionary – with decoding
# for col in ["Symptoms"]:
#     df_temp = df[col].replace({'\'': '"',"True":"true"}, regex=True).apply(json.loads).apply(pd.Series).add_prefix(f"{col}_")
#     df_temp.fillna(False,inplace=True)
#     df = df.merge(df_temp, left_index=True, right_index=True)
#     df.drop(columns=col,inplace=True)
#
# del df_temp
#
# # Convert dtypes:
# date_cols = [col for col in df.columns if any(x in col for x in ["Date","Calendar"])]
# for col in date_cols:
#     df[col] = pd.to_datetime(df[col])
#
# # Convert diagnosis
# df["Diagnosis_tested"] = df["Diagnosis_tested"].map({"yes":True,"no":False})
# df['Diagnosis_positive'] = df['Diagnosis_result'].map({"negative":False,"positive":True, "waiting for results":None})
# df.drop(columns=["Diagnosis_result","CountryCode"],inplace=True)
#
# # Convert Gender – Eventually
# # df['Gender'] = df['Gender'].map({"Male":0,"Female":1, "Non-binary":2, "Others":3})
#
# for col in ["Age","Gender","Country","PostalCode"]:
#     df[col] = pd.Categorical(df[col])


# Done!
print(df.head(10))
