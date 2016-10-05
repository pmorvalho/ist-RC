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

		print "Waiting for registration confirmation from TCS..."

		reply = self.server.recvfrom(1024)

		if (reply[0] == "SRR NOK\n"):
			print "Cannot register. Exiting..."
			sys.exit()

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


# Input

if (len(sys.argv) == 8):
	port = sys.argv[3]
	hostTCS = sys.argv[5]
	portTCS = sys.argv[7]
elif (len(sys.argv) == 6):
	if (sys.argv[2] == "-p"):
		port = sys.argv[3]
		if (sys.argv[4] == "-n"):
			hostTCS = sys.argv[5]
			portTCS = 58052
		elif (sys.argv[4] == "-e"):
			portTCS = sys.argv[5]
			hostTCS = socket.gethostname()
	elif (sys.argv[2] == "-n"):
		hostTCS = sys.argv[3]
		portTCS = sys.argv[5]
		port = 59000
elif (len(sys.argv) == 4):
	if (sys.argv[2] == "-p"):
		hostTCS = socket.gethostname()
		portTCS = 58052
		port = eval(sys.argv[3])
	elif (sys.argv[2] == "-n"):
		hostTCS = sys.argv[3]
		port = 59000
		portTCS = 58052
	elif (sys.argv[2] == "-e"):
		portTCS = sys.argv[3]
		port = 59000
		hostTCS = socket.gethostname()
else:
	port = 59000
	hostTCS = socket.gethostname()
	portTCS = 58052

sockUdp = socketUDP(socket.gethostname(), portTCS, sys.argv[1])

sockTCP = socketTCP(port)

sockUdp.register(portTCS);


while(1):

	command = raw_input("Command: ")

	print command

	# if (command == "SRG"):
	#
	# 	msg = "SRG Frances 100.00.02.3 59000\n"
	#
	# 	sockUdp.getServer().sendto(msg, (hostTCS, portTCS))
	#
	# 	print sockUdp.getServer().recvfrom(1024)

	if (command == "SUN"): #SUN language IP port
		msg = "SUN Frances 100.00.02.3 59000\n"

		sockUdp.getServer().sendto(msg, (socket.gethostname(), portTCS))

		print "Enviou"

		print sockUdp.getServer().recvfrom(1024)

  	if (command == "exit"):

		sys.exit("Volte em breve!")


# sockUdp.contact()

sockUdp.terminateConnection()
