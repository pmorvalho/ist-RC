#!bin/usr/python

#Server

import socket
import errno
import sys


class socketServer:
	
	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def contact(self, languages, lnames):
		print "Waiting for contact from someone"


		try:
			self.server.settimeout(20.0)
			msg, addr = self.server.recvfrom(1024)
		except Exception:
			print "CONN_TIMEOUT: Just waited 20.0 seconds for a connection and didn't get one"
			print "CONN_RETRY: Retrying to get connection"
			return


		message = msg.split(" ")
		print "Just received messaged: from IP:" + addr[0] + ' from Port:' + str(addr[1])
		print "Message received: " + msg

		if (msg[:3] == "ULQ"):
			if(len(languages) == 0):
				try:
					self.server.sendto("ULR EOF\n", addr)
					print "ERROR_ULR: there are no TRS services available"
					return
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: ULR EOF"
					print senderror
					return



			if(len(message) > 1):
				try:
					self.server.sendto("ULR ERR\n", addr)
					print "ERROR_ULR: messsage format corrupted"
					return
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: ULR ERR"
					print senderror
					return

			msg_lang = "ULR " + str(len(languages))

			for i in range(len(languages)):
				msg_lang += " " + lnames[i]

			print "Message sent to user: " + msg_lang + "\n"

			try:
				self.server.sendto(msg_lang + "\n", addr)

			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to client: LIST OF LANGUAGES"
				print senderror
				return


		#UNQ request for TRS address
		elif (msg[:3] == "UNQ"):
			if(len(message) != 2):
				print "ERROR_UNQ: message sent from user is corrupted"
				try:
					self.server.sendto('UNR ERR\n', addr)
					return
				except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to client: UNR ERR"
						print senderror
						return

			TRS_lang = message[1][:-1]
			
			try:
				TRS_info = languages[TRS_lang]
			except:
				print "ERROR_UNQ: invalid language name"
				try:
					self.server.sendto('UNR EOF\n', addr)

				except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to client: UNR EOF"
						print senderror
						return

			TRS_ip = TRS_info[0]
			TRS_port = TRS_info[1]

			print "User app wants to connect to the following TRS - Language: " , TRS_lang , " IP: " , TRS_ip , " Port: " , TRS_port
			try:
				self.server.sendto('UNR ' + TRS_ip + ' ' + str(TRS_port) + '\n', addr)

			except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: UNR"
					print senderror
					return

		elif (msg[:3] == "SRG"):
			#TODO: registar no fich TRS novo de uma nova linguagem
				if(len(message) != 4): #verificar mensagens corruptas
					try:
						print "error in SRG format from TRS"
						self.server.sendto("SRR ERR\n", addr)
						return
					except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: SRR ERR"
						print senderror
						return

				if (message[1] in lnames):
					try:
						print "SRG_ERROR: error registrating TRS service"
						self.server.sendto('SRR NOK\n', addr)
						return
					except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: SRR NOK"
						print senderror
						return

				#adds the TRS that wants to register to the list of languages active
				languages[message[1]] = (message[2],eval(message[3]))
				lnames += [message[1]]
				print languages[message[1]]
				print "Successfully registrated TRS service: " + message[1] + "\n"
				try:
					self.server.sendto('SRR OK\n', addr)
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: SRR OK"
					print senderror
					return



		elif (msg[:3] == "SUN"):
			# remove do fich um TRS de uma certa linguagem
			TRS_lang = message[1]
			if(len(message) != 4): #verificar mensagens corruptas
				print "SUN_ERROR: message sent is corrupted"
				return
			try:
				if (languages[TRS_lang] == (message[2], eval(message[3]))):
					lnames.remove(TRS_lang)
					languages.pop(TRS_lang)
					status_SUN = "OK\n"
					print "Successfully removed TRS service: " + message[1]
				else:
					status_SUN = "NOK\n"
					print "SUN_WARNING: TRS service not removed: " + message[1]

				self.server.sendto('SUR ' + status_SUN, addr)


			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message SUR to TRS server"
				print senderror
				return

		else:
			print "CONN_ERROR: Received message with worng format"
			return 




	#Updates the file languages.txt as the execution may have changed the languages registred
	def updateLanguages(self, file, languages, lnames):
		lang_f = open("languages.txt", "w")
		print "Languages being added to languages.txt"
		print "Number of languages being written to the languages.txt file: " + str(len(languages))
		for i in range(len(languages)):
			lang = lnames[i]
			print "Adding language: " + lang
			lang_f.write(lang + ' ' + languages[lang][0] + ' ' + str(languages[lang][1]) + '\n')
		lang_f.close()
	
	def terminateConnection(self):
		self.server.close()

lang_f = open("languages.txt", "a+")

fileLang_lines = lang_f.readlines()

langs = []
lang_names = []

for i in range(len(fileLang_lines)):
	file_line = fileLang_lines[i].split(" ")
	lang_names += [file_line[0]]
	langs += [(file_line[0], (file_line[1], eval(file_line[2])))]

langs = dict(langs)

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
		s.contact(langs, lang_names)

	s.updateLanguages(lang_f, langs, lang_names)
	s.terminateConnection()




except KeyboardInterrupt:
	print '\n'
	print 'KeyboardInterrupt found --- treating Control-C interruption'
	s.updateLanguages(lang_f, langs, lang_names)
	s.terminateConnection()

except ValueError:
	print "VALUE_ERROR: Invalid port given"
	print "PORT_INT: Port must be an integer"

except Exception:
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python TCS.py -p 50000"

except socket.gaierror:
	print "SOCKET_ERROR: Failed to get host name"


finally:
	print "TCS Turning off -- System Exit"
	sys.exit(0)




# Italiano 123.345.566. 50000
# Alemao 123.345.566. 50000
# Ingles 123.345.566. 50000
# Frances 123.345.566. 50000