#!bin/usr/python

# Este projeto foi desenvolvido por:
# Grupo 52:
# - David Calhas, no. 80980, Curso: LEIC-A
# - Joao Silveira, no. 80789, Curso: LEIC-A
# - Pedro Orvalho, no. 81151, Curso: LEIC-A

#Client

import socket
import sys
import os
import errno
import time
import argparse

#Fechar a aplicacao fechando o socket
def shutApp(sock):
	sock.close()
	sys.exit("Thank you! Come again")

#Trata do comando list
def list_languages(sock):
	lang = []
	try:
		sock.settimeout(5)
		d = sock.recvfrom(2048) #recebe mensagem do TCS
	except socket.timeout:
		print "Socket timed out. TCS is probably down. Exiting..."
		shutApp(s)
	except:
		print "Error receiving message from TCS. Exiting..."
		shutApp(s)

	reply = d[0]

	rep = reply.split(" ") # divide a mensagem pelos espacos

	if (len(rep) < 2):
		return

	try:
		lang_no = eval(rep[1])
	except:
		print "TCS message wrongly formatted. TCS is probably corrupted. Exiting..."
		shutApp(sock)

	if (rep[0] != "ULR"):
		print "TCS reply does not comply with protocol\n"
	elif ( rep[1] == "EOF\n" ): #caso nao haja linguagens disponiveis
		print "No languages available\n"
	elif (rep[1] == "ERR\n" or lang_no != len(rep[2:])):
		print "ULQ request wrongly formatted\n"
	else: # Lista as linguagens disponives
		
		for i in range(lang_no):
			print str(i+1) + " - " + rep[i+2]

		lang += rep[2:-1] + [rep[-1][:-1]]

	return lang


#Parse dos comandos do terminal###########################
parser = argparse.ArgumentParser()

parser.add_argument("-p", help="TCS port", type=int)
parser.add_argument("-n", help="TCS host")

try:
	args = parser.parse_args()
except:
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python userApp.py -p 58052 -n tejo.ist.utl.pt"
	print "user Turning off -- System Exit"
	sys.exit(0)

host = socket.gethostname()
port = 58052

if args.p:
	port = args.p

if args.n:
	host = args.n
##########################################################

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = (host, port)

print(address)

languages = [] # Lista que guarda todas as linguagens disponiveis. E atualizada com o comando 'list'

while(1):
	try:
		command = raw_input("Command: ")
	except IOError:
		print "INPUT_ERROR: error reading input"
		shutApp(s)

	if (command == "list"): # Comando 'list' que pedir ao TCS e depois listar as linguagens disponiveis
		msg = "ULQ\n" # mensagem a enviar ao TCS

		try:
			s.sendto(msg, address)
		except socket.error as senderror:
			if(senderror.errno != errno.ECONNREFUSED):
				raise senderror
			print "SOCKET_ERROR: Error sending message to TCS server: ULQ"
			print senderror
			print "Exiting..."
			shutApp(s)

		languages = list_languages(s) # atualiza a lista das linguagens

	elif (command[:8] == "request "): 
	# comando 'request':
	# vai pedir o ip e porto do TRS ao TCS e pedir uma traducao ao TRS

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

		else: # Faz pedido do ip e porto do TRS ao TCS

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
				s.settimeout(5)
				d = s.recvfrom(1024) # Recebe resposta do TCS
			except socket.timeout:
				print "socket.recv timed out. TRS is probably down. Exiting..."
				socketTRS.close()
				shutApp(s)
			except:
				print "SOCKET_ERROR: Error receiving message from TCS: UNR expected. Exiting..."
				shutApp(s)

			reply = d[0]

			rep = reply.split(" ")

			# Testa possiveis erros na resposta do TCS
			if (len(rep) > 3 or len(rep) < 2):
				print "Protocol error in message received from TCS. Exiting...\n"
				shutApp(s)

			if (rep[0] != "UNR"):
				print "Wrong message received from TCS\n"
				shutApp(s)

			if (rep[1] == "EOF\n"):
				print "Translation request could not be completed\n"
				continue

			elif (rep[1] == "ERR\n"):
				print "User request is corrupted\n"
				continue

			# Guarda a informacao para se ligar ao TRS que vai tratar do pedido de traducao
			ipTRS = rep[1]
			
			try:
				portTRS = eval(rep[2])
			except:
				print "Port specification is not an integer. TCS corrupted. Exiting..."
				shutApp(s)
			
			hostTRS = socket.gethostbyaddr(ipTRS)[0]
			addressTRS = (hostTRS,portTRS)

			socketTRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				socketTRS.connect(addressTRS) # Estabelece ligacao TCP com o TRS
			except socket.error as err:
				print "SOCKET_ERROR: Failed connecting. Exiting..."
				socketTRS.close()
				shutApp(s)

			try:
				translation_type = comm[2] # Guarda o tipo de traducao -> 't' ou 'f'
			except:
				print "Command wrongly formatted\n"
				socketTRS.close()
				continue

			if (comm[2] == "t"): # Traducao de texto
				nWords = len(comm[3:])
				if (nWords == 0):
					print "No words to translate\n"
					socketTRS.close()
					continue
				msg = "TRQ t " + str(nWords)
				for i in range(nWords):
					msg += " " + comm[3:][i]
				msg += "\n"

				try:
					socketTRS.send(msg) # Envia pedido de traducao ao TRS

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: ", msg
					print senderror
					print "Exiting..."
					socketTRS.close()
					shutApp(s)

				try:
					socketTRS.settimeout(5)
					msg = socketTRS.recv(1024) # Recebe resposta do TRS ao pedido de traducao
				except socket.timeout:
					print "socket.recv timed out. TRS is probably down. Exiting..."
					socketTRS.close()
					shutApp(s)
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

				for i in range(len(msg[3:])): # Escreve a linha com o texto traduzido
					translation += " " + msg[3:][i]

				print "\nTranslation:" , translation

			elif (comm[2] == "f"): # Traducao de ficheiro

				if (len(comm) > 4): # Quando se tenta traduzir mais que um ficheiro
					print "Incorrect way to translate file. Try translating one file at a time\n"
					socketTRS.close()
					continue

				try: # Mensagem com nome e tamanho do ficheiro
					msg = "TRQ f " + comm[3] + " " + str(os.stat(comm[3]).st_size) + " "
				except:
					print "File does not exist. Try a different file\n"
					socketTRS.close()
					continue

				try:
					socketTRS.send(msg) # Envia inicio da mensagem de pedido de traducao de ficheiro ao TRS
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: msg"
					print senderror
					print "Exiting..."
					socketTRS.close()
					shutApp(s)

				file_to_trl = open(comm[3],"rb") # Abertura do ficheiro a traduzir

				# Envia ficheiro
				print "Uploading file to server..."

				data = file_to_trl.read(256) # Comeca a enviar o ficheiro

				while (data): # Ciclo de envio do ficheiro por chunks de 256bytes de cada vez
					try:
						socketTRS.send(data)

					except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: (BINARY DATA)"
						print senderror
						print "Exiting..."
						file_to_trl.close()
						socketTRS.close()
						shutApp(s)

					data = file_to_trl.read(256)

				file_to_trl.close()

				try:
					socketTRS.send("\n") # Envia o '\n' de final da mensagem
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: (EXTRA FORMAT)"
					print senderror
					socketTRS.close()
					shutApp(s)

				print "File uploaded\n"

				# Recepcao do ficheiro

				# Vai recebendo pequenas quantidades de bytes para perceber que tipo de mensagem recebeu
				try:
					socketTRS.settimeout(5)
					translated = socketTRS.recv(3)
				except socket.timeout:
					print "socket.recv timed out. TRS is probably down. Exiting..."
					socketTRS.close()
					shutApp(s)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				if ( translated != "TRR"):
					print "Protocol error. Expecting file translation. Exiting..."
					socketTRS.close()
					shutApp(s)

				try:
					socketTRS.settimeout(5)
					translated = socketTRS.recv(3)
				except socket.timeout:
					print "socket.recv timed out. TRS is probably down. Exiting..."
					socketTRS.close()
					shutApp(s)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				if (translated == " NT"): # Caso receba 'TRR NTA'

					try:
						socketTRS.settimeout(5)
						translated = socketTRS.recv(1)
					except socket.timeout:
						print "socket.recv timed out. TRS is probably down. Exiting..."
						socketTRS.close()
						shutApp(s)
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

				if (translated == " ER"): # Caso receba 'TRR NTA'

					try:
						socketTRS.settimeout(5)
						translated = socketTRS.recv(1)
					except socket.timeout:
						print "socket.recv timed out. TRS is probably down. Exiting..."
						socketTRS.close()
						shutApp(s)
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

				# Le o espaco que vem a seguir
				try:
					socketTRS.settimeout(5)
					byte = socketTRS.recv(1)
				except socket.timeout:
					print "socket.recv timed out. TRS is probably down. Exiting..."
					socketTRS.close()
					shutApp(s)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				filename = ""

				# Le byte a byte do socket para receber o filename
				while (byte != " "):
					filename += byte
					try:
						socketTRS.settimeout(5)
						byte = socketTRS.recv(1)
					except socket.timeout:
						print "socket.recv timed out. TRS is probably down. Exiting..."
						socketTRS.close()
						shutApp(s)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

				print "Filename: " , filename

				# Le o espaco que vem a seguir
				try:
					socketTRS.settimeout(5)
					byte = socketTRS.recv(1)
				except socket.timeout:
					print "socket.recv timed out. TRS is probably down. Exiting..."
					socketTRS.close()
					shutApp(s)
				except:
					print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
					socketTRS.close()
					shutApp(s)

				filesize = ""

				# Le byte a byte do socket para receber o filesize
				while (byte != " "):
					filesize += byte
					try:
						socketTRS.settimeout(5)
						byte = socketTRS.recv(1)
					except socket.timeout:
						print "socket.recv timed out. TRS is probably down. Exiting..."
						socketTRS.close()
						shutApp(s)
					except:
						print "SOCKET_ERROR: Error receiving message from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

				print "File size: " , filesize, " bytes"

				# Inicia a recepcao do ficheiro
				print "Downloading file..."

				################################################################
				filesize = eval(filesize)

				try: # Se o ficheiro ja existir na diretoria, e eliminado
					os.remove("translation_" + filename)
					print "File on directory overwritten"
				except:
					print "Translation file created"

				# Abre ou cria o ficheiro onde vao ser guardados os dados recebidos
				recv_file = open("translation_" + filename,"wb+")

				# Le dados do socket em chunks de 256bytes ate receber o numero de bytes
				# que e esperado receber, i.e. o indicado na mensagem
				while (filesize >= 0):
					try:
						socketTRS.settimeout(5)
						data = socketTRS.recv(256)
					except socket.timeout:
						print "socket.recv timed out. TRS is down or file is smaller than specified"
						print "Exiting..."
						socketTRS.close()
						shutApp(s)
					except:
						print "SOCKET_ERROR: Error receiving file from TRS. Exiting..."
						socketTRS.close()
						shutApp(s)

					filesize -= len(data)
					if (filesize < 0 and data[-1] == "\n"): #remover \n do ficheiro enviado
						data = data[:-1]
					elif (filesize < 0 and data[-1] != "\n"):
						print "Error receiving file. The specified size is different to received\n"
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
