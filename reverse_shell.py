#!/usr/bin/python
import socket

sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 15555)) #connect to server
print("Connection established to Server")
message = sock.recv(1024) #bytes
print(message.decode())
answer = "Hello too"
sock.send(answer.encode())
sock.close()
