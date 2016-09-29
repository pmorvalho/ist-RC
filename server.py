#!bin/usr/python

#Server


import socket




class socketServer:
	
	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def listen(self, n):
		(self.server).listen(n)

	def contact(self):
		c, addr = self.server.accept()

		print 'Got connection from', addr

		print c.recv(400)

		c.send('Thank you for connecting')

		c.close()

	def terminateConnection(self):
		self.server.close()




s = socketServer(50000)

print socket.gethostname()
s.listen(5)


s.contact()

s.terminateConnection()