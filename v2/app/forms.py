from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import FormField, FieldList, SelectMultipleField
from wtforms.validators import DataRequired


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
