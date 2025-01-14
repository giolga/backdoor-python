#!/usr/bin/python
import socket

sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 15555)) #connect to server
print("Connection established to Server")

while True:
	message = sock.recv(1024) #bytes
	print(message.decode())
	if message == "q": # if server stops communicating, break the loop
		print('Server closed the connection')
		break
	else:
		message_back = input('Send message to the Server ')
		sock.send(message_back.encode())
sock.close()
