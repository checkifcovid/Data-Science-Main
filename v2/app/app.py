"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""

import sys
sys.path.append(".")
from pathlib import Path
import subprocess
import requests
import pandas as pd

# Flask stuff
from flask import Flask, request, jsonify, render_template, flash, redirect
from flask_wtf.csrf import CSRFProtect

# Import the cache
from extensions import cache

# Import forms
from forms import symptomForm

# Model stuff
from model.fit import fit_to_model

# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
csrf = CSRFProtect(app)
# Initialize the cache
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})
# ------------------------------------------------------------------------------


# Home
@app.route('/')
def index():
    return render_template('index.html', title='Home')

# ------------------------------------------------------------------------------

# User submits data manually
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

            # save data to cache
            cache.set("my_data", my_data)
            return redirect('/submit-data-success/')
    else:
        return render_template('submit-data.html', title='Submit Data', form=form)


# ------------------------------------------------------------------------------

# Submitted data is fitted to model
@app.route('/submit-data-success/',  methods=['GET'])
def fit_my_data():

    data = cache.get("my_data")

    # Success vs. Failure
    if data:
        #  *  *  *  *  *  *  *  *  *  *  *  *
        #  This is where the magic happens
        # Error in way data is current structured on the page.
        # Need to reorganize it to meet the correct structure...
        # prediction = fit_to_model(data)
        #  *  *  *  *  *  *  *  *  *  *  *  *

        # return jsonify(prediction)
        return render_template('submit-data-success.html', title="Success", data=data)
    else:
        return render_template('submit-data-failure.html', title="Failure")

# ------------------------------------------------------------------------------


# Convert to post...
@app.route('/train_model/', methods=['GET'])
def train_model():
    """
    Will train the model
    """

    # Consider mandating api key
    # api_key = request.args.get('api_key')
    #
    # if not api_key:
    #     return jsonify({
    #         "ERROR": "api_key not found."
    #     })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # otherwise
    file_path = Path("model/batch_commands/new_model.py")
    command = f"python3 {file_path}"
    subprocess.call(command, shell=True)

    # Add this option to distinct the POST request
    return jsonify({
        "Message": "Finished training the model",
        "METHOD" : "POST"
    })


# ------------------------------------------------------------------------------

# TO DO: Not used yet....
@app.route('/fit_data/', methods=['POST'])
def respond():

    # Retrieve the data from  parameter
    data = request.form.get("data", None)
    # data = request.get_json(force=True)

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    #  *  *  *  *  *  *  *  *  *  *  *  *
    #  This is where the magic happens
    prediction = fit_to_model(data)
    #  *  *  *  *  *  *  *  *  *  *  *  *

    # Proceed
    response = prediction

    # Return the response in json format
    return jsonify(response)



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(host="0.0.0.0", debug=True)
