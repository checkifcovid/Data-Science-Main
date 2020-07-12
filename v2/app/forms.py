from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields import FormField, FieldList, SelectMultipleField
from wtforms.validators import DataRequired, Regexp
import json

# Make a form
class userInfo(FlaskForm):
    name = StringField('survey_id', validators=[DataRequired()], default="002")
    user_id = StringField('user_id', validators=[DataRequired()], default="12098789")
    report_date = StringField('report_date', validators=[DataRequired()], default="2020-03-27 12:00:00")
    report_source = StringField('report_source', validators=[DataRequired()], default = "report_diagnosis")

class demographicInfo(FlaskForm):
    gender = StringField('gender', validators=[DataRequired()], default="female")
    age = StringField('age', validators=[DataRequired()], default="55")

class symptomsInfo(FlaskForm):
    all_symptoms = ["fever", "running_nose", "cough"]
    symptoms = SelectMultipleField("Select all your symptoms", choices=[(x,x) for x in all_symptoms ])

class diagnosticInfo(FlaskForm):
    calendar_onset = StringField('onset', default="03/16/2020")
    calendar_tested = StringField('tested', default="04/24/2020")
    postcode = StringField('postcode', validators=[DataRequired()], default="07093")
    country = StringField('country', default="United States of America")
    country_code = StringField('country_code', default="USA")
    diagnosis_tested = StringField('tested', default="no")


class symptomFields(FlaskForm):
    userInfo = FormField(userInfo)
    demographicInfo = FormField(demographicInfo)
    symptomsInfo = FormField(symptomsInfo)
    diagnosticInfo = FormField(diagnosticInfo)

# The acrtual form!
class symptomForm(FlaskForm):
    allFields = FormField(symptomFields)


# ==============================================================================

# Make a form to submit json data

# default data
default_data = {
    "survey_id": "002",
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

# Make a form
class jsonData(FlaskForm):
    jsonData = TextAreaField('jsonData', validators=[DataRequired(), Regexp("^\{.*\}$", message="Username must contain only letters numbers or underscore")], default=json.dumps(default_data))

# The acrtual form!
class jsonForm(FlaskForm):
    allFields = FormField(jsonData)
