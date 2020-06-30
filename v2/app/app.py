"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""

import subprocess
import requests
import pandas as pd
from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect

# Import forms
from forms import symptomForm

# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)
# ------------------------------------------------------------------------------


# Home
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------

@app.route('/submit-data/',  methods=['GET', 'POST'])
def submit_data():

    form = symptomForm(request.form)

    if request.method == 'POST':
        if form.validate():
            my_data = {}
            for key, value in form.allFields.data.items():
                if type(value)==dict:
                    my_data.update(value)
            # get rid of the csrf token
            del my_data["csrf_token"]
            return render_template('submit-data-success.html', title="Success", data=my_data)
    else:
        return render_template('submit-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------


# Convert to post...
@app.route('/train_model/', methods=['GET'])
def train_model():
    """
    If API key is given, will train the model
    """
    # api_key = request.args.get('api_key')
    #
    # if not api_key:
    #     return jsonify({
    #         "ERROR": "api_key not found."
    #     })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # otherwise

    # Create the model
    subprocess.call("python model_create.py", shell=True);


    # Add this option to distinct the POST request
    return jsonify({
        "Message": "Finished training the model",
        "METHOD" : "POST"
    })


# ------------------------------------------------------------------------------

@app.route('/fit_data/', methods=['POST'])
def respond():

    # Retrieve the api_key
    # api_key = request.form.get("api_key", None)
    # if not api_key:
    #     return jsonify({
    #         "ERROR": "api_key not found."
    #     })

    # Retrieve the data from  parameter
    data = request.form.get("data", None)
    # data = request.get_json(force=True)

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # Proceed
    response = {}

    # Return the response in json format
    return jsonify(response)



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0")
