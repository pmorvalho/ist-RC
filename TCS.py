#!bin/usr/python

#Server

import socket
import sys

class socketServer:
	
	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def listen(self, n):
		(self.server).listen(n)

	def contact(self):
		c, addr = self.server.accept()

		print 'Got connection from', addr

		msg = c.recv(400)

		print msg

		c.send('Thank you for connecting')

		c.close()

	def terminateConnection(self):
		self.server.close()

if (len(sys.argv) == 3):
	s = socketServer(eval(sys.argv[2]))

else:
	s = socketServer(58052)

print socket.gethostname()
s.listen(5)


s.contact()

s.terminateConnection()