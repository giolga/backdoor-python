#!/usr/bin/python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 15555))
print('Connection esablished to Server')

while True:
    message = sock.recv(1024).decode()
    print(f'Message: {message}')

    if message == 'q':
        break
    else:
        message_back = input('Type message to send to Server: ')
        sock.send(message_back.encode())

sock.close()