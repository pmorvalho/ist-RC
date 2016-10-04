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

	def contact(self, languages):
		msg, addr = self.server.recvfrom(1024)

		message = msg.split(" ")

		print msg

		if (msg[:3] == "ULQ"):
			#TODO: correr ficheiro com as linguagens e manda-las ao user
			self.server.sendto('ULR 2 Puta Coco\n', addr)

		if (msg[:3] == "UNQ"):
			#TODO: com o nome da linguagem, ir ao fich buscar ip e port do TRS respetivo
			print "UNR"
			self.server.sendto('UNR ipTRS portTRS\n', addr)

		if (msg[:3] == "SRG"):
			#TODO: registar no fich TRS novo de uma nova linguagem
			if(len(message) != 4): #verificar mensagens corruptas
				print "error in SRG format from TRS"
				self.server.sendto("SRR ERR\n", addr)

			for i in range(len(languages)):
				if languages[i][0] == message[1]:
					print "NOK"
					self.server.sendto('SRR NOK\n', addr)
					return
			languages += [(message[1],message[2],eval(message[3]))]
			print "OK"
			self.server.sendto('SRR OK\n', addr)

		if (msg[:3] == "SUN"):
			#TODO: remove do fich um TRS de uma certa linguagem
			status_SUN = ""
			if(len(message) != 4): #verificar mensagens corruptas
				print "error in message SUN from TRS"
			TRS_lang = (message[1], message[2], eval(message[3]))
			if(TRS_lang in languages):
				languages.remove(TRS_lang)
				status_SUN = "OK\n"
				print "OK\n"
			else:
				status_SUN = "NOK\n"
				print "ONK\n"

			self.server.sendto('SUR ' + status_SUN, addr)

		print "Vai printar addr"
		print addr

	def terminateConnection(self):
		self.server.close()

lang_f = open("languages.txt", "a+")

langs = []

if (len(sys.argv) == 3):
	s = socketServer(eval(sys.argv[2]))

else:
	s = socketServer(58052)

#estar a prova de erros!!

print socket.gethostname()

while(1):
	s.contact(langs)

s.terminateConnection()