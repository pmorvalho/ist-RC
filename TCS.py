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
		print "Waiting for contact from someone"
		msg, addr = self.server.recvfrom(1024)

		message = msg.split(" ")
		print "Just received messaged: from IP:" + addr[0] + ' from Port:' + str(addr[1])
		print "Message received: " + msg

		if (msg[:3] == "ULQ"):
			if(len(languages) == 0):
				self.server.sendto("ULR EOF\n", addr)
				print "ERROR_ULR: there are no TRS services available"
				return



			if(len(message) > 1):
				self.server.sendto("ULR ERR\n", addr)
				print "ERROR_ULR: messsage format corrupted"
				return

			msg_lang = "ULR " + str(len(languages))

			for i in range(len(languages)):
				msg_lang += " " + languages[i][0]

			print "Message sent to user: " + msg_lang + "\n"
			self.server.sendto(msg_lang + "\n", addr)


		#UNQ request for TRS address
		if (msg[:3] == "UNQ"):
			#TODO: com o nome da linguagem, ir ao fich buscar ip e port do TRS respetivo
			if(len(message) != 2):
				print "ERROR_UNQ: message sent from user is corrupted"
				self.server.sendto('UNR ERR\n', addr)
				return

			TRS_lang = message[1]
			for i in range(len(languages)):
				if(languages[i][0] == TRS_lang):
					break;
			if(i == len(languages)):
				print "ERROR_UNQ: invalid language name"
				self.server.sendto('UNR EOF\n', addr)
			else:
				TRS_ip = languages[i][1]
				TRS_port = languages[i][2]

				print "User app wants to connect to the following TRS: " + languages[i][0]
				self.server.sendto('UNR ' + TRS_ip + ' ' + str(TRS_port) + '\n', addr)

		if (msg[:3] == "SRG"):
			#TODO: registar no fich TRS novo de uma nova linguagem
			if(len(message) != 4): #verificar mensagens corruptas
				print "error in SRG format from TRS"
				self.server.sendto("SRR ERR\n", addr)
				return

			for i in range(len(languages)):
				if languages[i][0] == message[1]:
					print "SRG_ERROR: error registrating TRS service"
					self.server.sendto('SRR NOK\n', addr)
					return
			#adds the TRS that wants to register to the list of languages active
			languages += [(message[1],message[2],eval(message[3]))]
			print "Successfully registrated TRS service: " + message[1] + "\n"
			self.server.sendto('SRR OK\n', addr)

		if (msg[:3] == "SUN"):
			#TODO: remove do fich um TRS de uma certa linguagem
			status_SUN = ""
			if(len(message) != 4): #verificar mensagens corruptas
				print "SUN_ERROR: message sent is corrupted"
				return
			TRS_lang = (message[1], message[2], eval(message[3]))
			if(TRS_lang in languages):
				languages.remove(TRS_lang)
				status_SUN = "OK\n"
				print "Successfully removed TRS service: " + message[1]
			else:
				status_SUN = "NOK\n"
				print "SUN_WARNING: TRS service not removed: " + message[1]

			self.server.sendto('SUR ' + status_SUN, addr)


	def updateLanguages(self, file, languages):
		lang_f = open("languages.txt", "w")
		print "Languages being added to languages.txt"
		print "Number of languages being written to the languages.txt file: " + str(len(languages))
		for i in range(len(languages)):
			print "Adding language: " + languages[i][0]
			lang_f.write(languages[i][0] + ' ' + languages[i][1] + ' ' + str(languages[i][2]) + '\n')
		lang_f.close()
	
	def terminateConnection(self):
		self.server.close()

lang_f = open("languages.txt", "a+")

fileLang_lines = lang_f.readlines()

langs = []

for i in range(len(fileLang_lines)):
	file_line = fileLang_lines[i].split(" ")
	langs += [(file_line[0], file_line[1], eval(file_line[2]))]

print "Number of languages: " + str(len(langs))


try:
	if (len(sys.argv) == 3):
		if(sys.argv[1] == '-p'):
			s = socketServer(int(sys.argv[2]))
		else:
			raise Exception

	else:
		s = socketServer(58052)

	#estar a prova de erros!!

	print socket.gethostname()

	while(1):
		s.contact(langs)

	s.updateLanguages(lang_f, langs)
	s.terminateConnection()


except KeyboardInterrupt:
	print '\n'
	print 'KeyboardInterrupt found --- treating Control-C interruption'
	s.updateLanguages(lang_f, langs)
	s.terminateConnection()

except ValueError:
	print "VALUE_ERROR: Invalid port given"
	print "PORT_INT: Port must be an integer"

except Exception:
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python TCS.py -p 50000"


finally:
	print "TCS Turning off -- System Exit"
	sys.exit(0)




#Italiano 123.345.566. 50000
#Alemao 123.345.566. 50000
#Ingles 123.345.566. 50000
#Frances 123.345.566. 50000