#!bin/usr/python

#Client 

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 50000

print host

address = (host, port)

s.connect(address)

ip = socket.gethostbyname(host)

print "Got connection to server ->  IPaddress", address[0], " port:", ip

msg = raw_input("Please enter the message you wish to send: ")

s.sendto(msg, address)

print s.recv(200)


s.close()




	