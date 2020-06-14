"""This app functions as a REST api endpoint"""

import subprocess
import pandas as pd
from flask import Flask, request, jsonify

# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)


# ------------------------------------------------------------------------------


# A welcome message to test our server
@app.route('/hello/')
def index():
    return "<h1>Yaakov Bressler is so cool!!</h1>"


# ------------------------------------------------------------------------------

# Convert to post...
@app.route('/train_model/', methods=['GET'])
def train_model():
    """
    If API key is given, will train the model
    """
    api_key = request.args.get('api_key')

    if not api_key:
        return jsonify({
            "ERROR": "api_key not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # otherwise

    # Create the model
    subprocess.call("python model_create.py", shell=True)


    return jsonify({
        "Message": f"Finished training the model.",
        # Add this option to distinct the POST request
        "METHOD" : "POST"
    })


# ------------------------------------------------------------------------------

@app.route('/fit_data/', methods=['POST'])
def respond():

    # Retrieve the api_key
    api_key = request.form.get("api_key", None)
    if not api_key:
        return jsonify({
            "ERROR": "api_key not found."
        })

    # Retrieve the data from  parameter
    data = request.form.get("data", None)
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
    app.run(threaded=True, port=5000)
