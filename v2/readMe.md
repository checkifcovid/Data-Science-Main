# Data Science – V2
_Find the Cluster – Data Science Workflow_

**05/05/2020:** Operate as if you're at the root of working project.

## Getting started:
1. set working directory to `v2`:
```
cd v2
```
2. create a virtual environment _(only do 1st time)_
```
python3 -m venv venv
```
3. activate the virtual environment
```
source venv/bin/activate
```
4. install requirements _(only do 1st time)_
```
pip install -r requirements.txt
```
5. run the code!
```
python3 main.py
```

**Note:** Make sure you have `aws credentials` either as environmental variables _or_ in a `secret` directory. Additionally, your bucket name should be stored in a file `aws_bucket_path.json` in the `secret` dir and should contain the key `"BUCKET_NAME"`. _(modification to this will be forthcoming)_

----
## Payloads

Incoming payload will have the following structure:
```
{"survey_id": "002",
 "user_id": "12098789",
 "report_date": "2020-03-27 12:00:00",
 "report_source": "report_diagnosis",
 "gender": "Female",
 "age": "54",
 "calendar": {"onset" : "03/16/2020", "tested" : "04/24/2020"},
 "postcode": "07093",
 "country": "United States of America",
 "country_code" : "USA",
 "diagnosis": {"tested" : "no" },
 "symptoms": {"fever": "False", "cough": "True", "runny_nose": "false"}
}
```

Model Apply will return a payload with the following structure:
```
{
  "diagnosis_positive": False,
  "pred_spread": 0.05628499278499299,
  "model_name": "RandomForestClassifier",
  "model_training_info": {
    "n_samples_train": 16,
    "n_samples_test": 6,
    "SMOTE": True
    },
  "model_metrics": {
    "accuracy": 0.6666666666666666,
    "balanced_accuracy": 0.6666666666666666,
    "log_loss": 11.513058731208593,
    "precision_score": 0.6666666666666666,
    "recall_score": 0.6666666666666666,
    "f1_score": 0.6666666666666666,
    "granular_prediction_metrics": {
      "TP": 2,
      "TN": 2,
      "FP": 1,
      "FN": 1
      },
    "pred_spread": [0.10070676545676543, 0.18233183483183474, 0.0013420190920192254, 0.08071201021201044, 0.12000277500277484, 0.06469674769674791]
    },
    "feature_importance": {
      "Diagnosis_tested": 0.0,
      "Symptoms_cough": 0.05,
      "Symptoms_body_pain": 0.0,
      "Symptoms_headache": 0.03,
      "Symptoms_sore_throat": 0.05,
      "Symptoms_fever": 0.04,
      "Symptoms_sinus_pressure": 0.0,
      "Symptoms_diarrhea": 0.02,
      "Symptoms_chills": 0.06,
      "Symptoms_runny_nose": 0.01,
      "Symptoms_fatigue": 0.21,
      "Symptoms_reduced_smell_taste": 0.0,
      "Symptoms_asthma": 0.0,
      "Symptoms_rash": 0.03,
      "Symptoms_shortness_breath": 0.04,
      "Symptoms_sneezing": 0.0,
      "Symptoms_chest_pain": 0.06,
      "Symptoms_nausea": 0.03,
      "Age_11-30": 0.02,
      "Age_31-50": 0.04,
      "Age_51-70": 0.01,
      "Age_nan": 0.0,
      "Country_Canada": 0.02,
      "Country_United States of America": 0.0,
      "Country_nan": 0.0,
      "Gender_female": 0.03,
      "Gender_male": 0.03,
      "Gender_nan": 0.0,
      "ReportSource_report_diagnosis": 0.0,
      "ReportSource_nan": 0.0,
      "N_days_Onset_to_Test": 0.05,
      "N_days_Onset_to_Subside": 0.1,
      "N_days_Onset_to_Now": 0.07
    }
  }
```
