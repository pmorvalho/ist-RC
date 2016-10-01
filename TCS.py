#!bin/usr/python

#Server

import socket
import sys

class socketServer:
	
	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def contact(self):
		msg, addr = self.server.recvfrom(1024)

		print msg

		if (msg[:3] == "ULQ"):
			#TODO: correr ficheiro com as linguagens
			self.server.sendto('ULR 2 Puta Coco\n', addr)

		if (msg[:3] == "UNQ"):
			#TODO: com o nome da linguagem, ir ao fich buscar ip e port do TRS respetivo
			print "UNR"
			self.server.sendto('UNR ipTRS portTRS\n', addr)

		if (msg[:3] == "SRG"):
			#TODO: registar no fich TRS novo de uma nova linguagem
			self.server.sendto('SRR status\n', addr)

		if (msg[:3] == "SUN"):
			#TODO: remove do fich um TRS de uma certa linguagem
			self.server.sendto('SUR status\n', addr)

		print "Vai printar addr"
		print addr

	def terminateConnection(self):
		self.server.close()

if (len(sys.argv) == 3):
	s = socketServer(eval(sys.argv[2]))

else:
	s = socketServer(58052)

print socket.gethostname()

while(1):
	s.contact()

s.terminateConnection()