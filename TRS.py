#!bin/usr/python

#Server


import socket

class socketTCP:
	
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

		print c.recv(400)

		c.send('Thank you for connecting')

		c.close()

	def terminateConnection(self):
		self.server.close()


class socketUDP:
	
	def __init__(self, host, port, language):
		self.hostTCS = host
		self.port = port
		self.language = language
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def register(self, portTCP):
		msg = "SRG " + self.language + " " + socket.gethostbyname(socket.gethostname()) + " " + str(portTCP) + "\n"

		self.server.sendto(msg, (socket.gethostname(),self.port))

	def contact(self):
		msg, addr = self.server.recvfrom(1024)

		print msg

		#ALTERAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



		print "Vai printar addr"
		print addr

	def terminateConnection(self):
		self.server.close()




s = socketUDP(socket.gethostname(),58052,"Frances")

s.register(80000);

print socket.gethostname()

s.contact()

s.terminateConnection()