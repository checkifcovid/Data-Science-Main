"""
This app functions as a REST api endpoint

Have the ability to utilize API keys -- or use VPN to limit to internal traffic
"""

import subprocess
import requests
import pandas as pd
from flask import Flask, request, jsonify

# ==============================================================================
# Begin
# ==============================================================================


app = Flask(__name__)

# add a rule for the index page.
header_text = '''
    <html><head>
    <title>CheckIfCovid ML API</title>
    </head><body>'''
body_text = '''
    <h1>Welcome to this API!</h1>
    <p>Lot's of cool things are happening here.</p>
    '''

home_link = """<a href="/"><button>Back</button></a><br>"""
train_model_link = """<a href="/train_model/"><button>Train Model</button></a><br>"""
footer_text = '</body>\n</html>'


# ------------------------------------------------------------------------------


# A welcome message to test our server
@app.route('/')
def index():
    my_content = [
        header_text,
        body_text,
        train_model_link,
        home_link,
        footer_text
        ]
    my_content = "".join(my_content)
    return my_content


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
    app.run()
