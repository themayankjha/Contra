# Import Flask and Blueprint classes from the Flask module
from flask import Flask, request,redirect,url_for , Blueprint
from contra.dbhelper import *

# Create a blueprint object for the connections route with a URL prefix
conn_bp = Blueprint("connections", __name__, url_prefix="/connections")

# Define a function to display the connections page
@conn_bp.route('', methods=['GET'])
def displayConnections():
    return read_connections()

# Define a function to access a specific connection ID
@conn_bp.route('/<id>', methods=['GET'])
def access_conn_id(id):
    return read_connection_data(id)

@conn_bp.route('/<id>/tasks', methods=['GET'])
def access_tasks(id):
    return  read_tasks(id)

@conn_bp.route('/<id>/tasks/new', methods=['POST'])
def addnew_task(id):
    cmd= request.form.get('cmd')
    write_tasks(id,cmd)
    return redirect(url_for('access_tasks',id=id))