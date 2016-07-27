from __future__ import division
from __future__ import print_function
import warnings

from flask import Flask
import os.path

APP = Flask(__name__.split('.')[0])

@APP.route("/")
def home_page():
    with open("eyes_example.html") as fh:
        return fh.read()

@APP.route("/css/<file_name>")
def static_css(file_name):
    basename = file_name.rsplit('..', 1)[0]
    safe_file_name = os.path.join("css", basename)
    if os.path.isfile(safe_file_name):
        with open(safe_file_name) as safe_fh:
            return safe_fh.read()
    else:
        msg = "File " + safe_file_name + " not found"
        print(msg)
        return(msg)
    
@APP.route("/<file_name>")
def static_page(file_name):
    safe_file_name = file_name.rsplit('..', 1)[0]
    if os.path.isfile(safe_file_name):
        with open(safe_file_name) as fh:
            return fh.read()
    else:
        msg = "File " + safe_file_name + " not found"
        print(msg)
        return(msg)

if __name__ == "__main__":
    # Run on port 8003, allow connections from all IP addresses
    APP.run(port=8003, host='0.0.0.0', debug=True)
