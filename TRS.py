#!bin/usr/python

#Server


import socket
import sys

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
		addressTCS = (socket.gethostbyname(socket.gethostname()), self.port)
		print "Registation on TCS being sent: "
		print addressTCS

		self.server.sendto(msg, addressTCS)

	def contact(self):
		msg, addr = self.server.recvfrom(1024)

		print msg

		#ALTERAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



		print "Vai printar addr"
		print addr

	def terminateConnection(self):
		self.server.close()

	def getServer(self):
		return self.server

print "Inicio"

if (len(sys.argv) == 7):
	port = sys.argv[2]
	hostTCS = sys.argv[4]
	portTCS = sys.argv[6]
elif (len(sys.argv) == 5):
	if (sys.argv[1] == "-p"):
		port = sys.argv[2]
		if (sys.argv[3] == "-n"):
			hostTCS = sys.argv[4]
			portTCS = 58052
		elif (sys.argv[3] == "-e"):
			portTCS = sys.argv[4]
			hostTCS = 'localhost'
	elif (sys.argv[1] == "-n"):
		hostTCS = sys.argv[2]
		portTCS = sys.argv[4]
		port = 59000
elif (len(sys.argv) == 3):
	if (sys.argv[1] == "-p"):
		print "puta"
		hostTCS = 'localhost'
		portTCS = 58052
		port = eval(sys.argv[2])
	elif (sys.argv[1] == "-n"):
		hostTCS = sys.argv[2]
		port = 59000
		portTCS = 58052
	elif (sys.argv[1] == "-e"):
		portTCS = sys.argv[2]
		port = 59000
		hostTCS = 'localhost'
else:
	port = 59000
	hostTCS = 'localhost'
	portTCS = 58052

sockUdp = socketUDP(socket.gethostname(), port, sys.argv[0])

# sockTCP = socketTCP(port)

sockUdp.register(portTCS);


while(1):

	command = raw_input("Command: ")
	# 
	# if (command == "SRG"):
	#
	# 	msg = "SRG Frances 100.00.02.3 59000\n"
	#
	# 	sockUdp.getServer().sendto(msg, (hostTCS, portTCS))
	#
	# 	print sockUdp.getServer().recvfrom(1024)

	if (command == "SUN"):

		msg = "SUN Frances 100.00.02.3 59000\n"

    	sockUdp.getServer().sendto(msg, (hostTCS, portTCS))

    	print sockUdp.getServer().recvfrom(1024)

  	if (command == "exit"):

		sys.exit("Volte em breve!")


# sockUdp.contact()

sockUdp.terminateConnection()
