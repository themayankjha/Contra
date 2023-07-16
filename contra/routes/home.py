# Import Flask and Blueprint classes from the Flask module
from flask import Flask, Blueprint,render_template

# Create a blueprint object for the home route with a URL prefix
home_bp = Blueprint("/", __name__, url_prefix="/")

# Define a function to display the root path of the home route
@home_bp.route('', methods=['GET'])
def displayRoot():
    return render_template('index.html')
