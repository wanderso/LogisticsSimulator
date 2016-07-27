from __future__ import division
from __future__ import print_function
import warnings

from flask import Flask
import os.path

APP = Flask(__name__.split('.')[0])


@APP.route("/")
def home_page():
    return "Hello world"


if __name__ == "__main__":
    # Run on port 8003, allow connections from all IP addresses
    APP.run(port=8003, host='0.0.0.0', debug=True)