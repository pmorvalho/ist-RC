#!bin/usr/python

#Client

import socket
import sys
import os
import errno
import time


def shutApp(sock): 
	sock.close()
	sys.exit("Thank you! Come again")

def list_languages(sock,lang):
	try:
		d = sock.recvfrom(2048)
	except:
		print "Error receiving message from TCS. Exiting..."
		shutApp(s)

	reply = d[0]
	addr = d[1]

	rep = reply.split(" ")

	if (len(rep) < 2):
		return
	if (rep[0] != "ULR"):
		print "TCS reply does not comply with protocol\n"
	elif ( rep[1] == "EOF\n" ): #caso nao haja linguagens disponiveis
		print "No languages available\n"
	elif (rep[1] == "ERR\n"):
		print "ULQ request wrongly formatted\n"
	else:
		for i in range(eval(rep[1])):
			print str(i+1) + " - " + rep[i+2]
			
		lang += rep[2:-1] + [rep[-1][:-1]]

def request_command():
	#TODO: isto^
	return

def text_trslt():
	#TODO: isto^
	return

def file_trslt():
	#TODO: isto^
	return

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if (len(sys.argv) == 3):
	if (sys.argv[1] == "-n"):
		host = sys.argv[2]
		port = 58052
	elif (sys.argv[1] == "-p"):
		port = eval(sys.argv[2])
		host = socket.gethostname()

elif (len(sys.argv) == 5):
	if (sys.argv[1] == "-n"):
		host = sys.argv[2]
		if(sys.argv[3] == "-p"):
			port = eval(sys.argv[4])
	elif (sys.argv[1] == "-p"):
		port = eval(sys.argv[2])
		if(sys.argv[3] == "-n"):
			host = sys.argv[4]

else:
	host = socket.gethostname()
	port = 58052

address = (host, port)

print(address)

languages = []

while(1):
	try:
		command = raw_input("Command: ")
	except IOError:
		print "INPUT_ERROR: error reading input"
		shutApp(s)

	if (command == "list"):
		msg = "ULQ\n"

		try:
			s.sendto(msg, address)
		except socket.error as senderror:
			if(senderror.errno != errno.ECONNREFUSED):
				raise senderror
			print "SOCKET_ERROR: Error sending message to TCS server: ULQ"
			print senderror
			print "Exiting..."
			shutApp(s)

		list_languages(s,languages)

	elif (command[:8] == "request "):
		
		comm = command.split(" ") #lista com os varios argumentos do comando
		
		try: 
			lang = eval(comm[1]) - 1
		except:
			print "You did not specify a valid language index\n"
			continue
		
		if (len(languages) == 0):
			print "No languages. Try using 'list' first\n"
			
		elif (lang >= len(languages) or lang < 0):
			print "Language index out of bounds\n"
			
		else: #Envia mensagem ao TCS
			
			msg = "UNQ " + languages[lang] + "\n"
			
			try:
				s.sendto(msg, address)
			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to TCS: UNQ"
				print senderror
				print "Exiting..."
				shutApp(s)

			try:
				d = s.recvfrom(1024)
			except:
				print "SOCKET_ERROR: Error receiving message from TCS: UNR expected. Exiting..."
				shutApp(s)

			reply = d[0]

			rep = reply.split(" ")

			if (len(rep) != 3):
				print "Protocol error in message received from TCS. Exiting...\n"
				shutApp(s)

			if (rep[0] != "UNR"):
				print "Wrong message received from TCS\n"
				shutApp(s)

			if (rep[1] == "EOF"):
				print "Translation request could not be completed\n"
				continue

			elif (rep[1] == "ERR"):
				print "Pedido mal formulado\n"
				continue

			#TODO: mandar try aqui
			ipTRS = rep[1]
			portTRS = eval(rep[2])
			hostTRS = socket.gethostbyaddr(ipTRS)[0]
			addressTRS = (hostTRS,portTRS)
			
			socketTRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				socketTRS.connect(addressTRS)
			except socket.error as err:
				print "SOCKET_ERROR: Failed connecting. Exiting..."
				socketTRS.close()
				shutApp(s)

			try:
				translation_type = comm[2]
			except:
				print "Command wrongly formatted\n"
				socketTRS.close()
				continue

			if (comm[2] == "t"):
				nWords = len(comm[3:])
				if (nWords == 0):
					print "No words to translate\n"
					socketTRS.close()
					continue
				msg = "TRQ t " + str(nWords)
				for i in range(nWords):
					msg += " " + comm[3:][i]
				msg += "\n"
				#print "Sent to TRS: " + msg

				try:
					socketTRS.send(msg)

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: ", msg
					print senderror
					print "Exiting..."
					socketTRS.close()
					shutApp(s)

				try:
					msg = socketTRS.recv(1024)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting...\n"
					socketTRS.close()
					shutApp(s)

				if (msg[:3] != "TRR"):
					print "Message received does not comply with protocol. TRS is probably corrupted\n"
					socketTRS.close()
					shutApp(s)

				if (msg[:7] == "TRR NTA"):
					print "No translation available. Try typing a different text\n"
					socketTRS.close()
					continue

				if (msg[:7] == "TRR ERR"):
					print "Error in message format\n"
					socketTRS.close()
					continue

				msg = msg.split(" ")

				translation = ""

				for i in range(len(msg[3:])):
					translation += " " + msg[3:][i]

				print "\nTranslation:" , translation

			elif (comm[2] == "f"):

				if (len(comm) > 4):
					print "Incorrect way to translate file. Try translating one file at a time\n"
					socketTRS.close()
					continue
				
				try:
					msg = "TRQ f " + comm[3] + " " + str(os.stat(comm[3]).st_size) + " "
				except:
					print "File does not exist. Try a different file\n"
					socketTRS.close()
					continue

				try:
					socketTRS.send(msg)
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: msg"
					print senderror
					print "Exiting..."
					socketTRS.close()
					shutApp(s)
				
				file_to_trl = open(comm[3],"rb")

				#enviar ficheiro
				print "Uploading file to server..."
				
				data = file_to_trl.read(256)

				while (data):
					try:
						socketTRS.send(data)

					except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: (BINARY DATA)"
						print senderror
						print "Exiting..."
						socketTRS.close()
						shutApp(s)

					data = file_to_trl.read(256)

				file_to_trl.close()
				
				try:
					socketTRS.send("\n")
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: (EXTRA FORMAT)"
					print senderror
					socketTRS.close()
					shutApp(s)

				print "File uploaded\n"

				#recepcao do ficheiro

				try:
					translated = socketTRS.recv(3)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				if ( translated != "TRR"):
					print "Protocol error. Expecting file translation. Exiting..."
					socketTRS.close()
					shutApp(s)
				
				try:
					translated = socketTRS.recv(3)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				if (translated == " NT"):
					
					try:
						translated = socketTRS.recv(1)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

					if (translated == "A"):
						print "No translation available for file. Try uploading a different file\n"
						socketTRS.close()
						continue
					else:
						print "Message received does not comply with protocol. Exiting..."
						socketTRS.close()
						shutApp(s)

				if (translated == " ER"):
					
					try:
						translated = socketTRS.recv(1)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

					if (translated == "R"):
						print "Error in message format\n"
						socketTRS.close()
						continue
					else:
						print "Message received does not comply with protocol. Exiting..."
						socketTRS.close()
						shutApp(s)

				if (translated != " f "):
					print "Message received does not comply with protocol. Exiting..."
					socketTRS.close()
					shutApp(s)

				#####################################################################
				try:
					byte = socketTRS.recv(1)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				filename = ""

				while (byte != " "):
					filename += byte
					try:
						byte = socketTRS.recv(1)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

				print "Filename: " , filename

				try:
					byte = socketTRS.recv(1)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				filesize = ""

				while (byte != " "):
					filesize += byte
					try:
						byte = socketTRS.recv(1)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

				print "File size: " , filesize, " bytes"

				print "Downloading file..."

				################################################################
				filesize = eval(filesize)

				try:
					os.remove("translation_" + filename)
					print "File on directory overwritten"
				except:
					print "Translation file created"

				recv_file = open("translation_" + filename,"wb+")

				while (filesize > 0):
					try:
						data = socketTRS.recv(256)
					except:
						print "SOCKET_ERROR: Error receiving file from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)
					filesize -= len(data)
					if (filesize <= 0 and data[-1] == "\n"): #remover \n do ficheiro enviado
						data = data[:-1]
					recv_file.write(data)

				recv_file.close()

				print "Download complete\n"

			else:
				print "Command wrongly formatted\n"
				socketTRS.close()
				continue


			socketTRS.close()
		
	elif (command == "exit"):
		shutApp(s)

	else:
		print "Command not found\n"


