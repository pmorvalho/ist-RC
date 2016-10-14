#!bin/usr/python

# Este projeto foi desenvolvido por:
# Grupo 52:
# - David Calhas, no. 80980, Curso: LEIC-A
# - Joao Silveira, no. 80789, Curso: LEIC-A
# - Pedro Orvalho, no. 81151, Curso: LEIC-A

#TRS


import socket
import sys
import os
import math
import errno
import argparse

# Classe do socket que faz a comunicacao entre o user e o TRS
class socketTCP:
	# construtor da classe
	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	# trata do listen do socket
	def listen(self, n):
		(self.server).listen(n)

	# funcao que trata de fazer a traducao de uma certa palavra da lingua respectiva do TRS para Portugues
	def text_translation(self, to_translate_aux, dict_words):
		# fazemos o split do input pelos espaco e passamos a leitura do numero de palavras que vamos traduzir
		to_translate_aux = to_translate_aux.split(" ")
		noWords = eval(to_translate_aux[0])
		
		if (len(to_translate_aux) != noWords+1):# Verifica se numero de palvaras a traduzir e igual ao indicado
			translation = "TRR ERR\n"
			return translation

		to_translate_aux[noWords] = to_translate_aux[noWords][:-1] # tirar \n
		if(noWords>0):
			# ignoramos o numero de palavras da string
			to_translate_aux = to_translate_aux[1:]
			# comeco da construcao da string de envio
			translation = "TRR t " + str(noWords)

			for i in range(noWords):
				if (to_translate_aux[i] not in dict_words):
					translation = "TRR NTA"
					print "Translation not found!"
					break
				else:
					translation += " " + dict_words[to_translate_aux[i]]
			translation += "\n"
		else:
			translation = "TRR ERR\n"
		return translation

	# funcao que trata de receber o ficheiro com o nome fname, enviado pelo cliente
	def receive_file(self, fname, l):
		fsize=""
		try:
			byte = socketAccept.recv(1)

			# le o tamanho do ficheiro
			while (byte != " "):
				fsize += byte
				byte = socketAccept.recv(1)

			print "File size: " , fsize

			fsize = eval(fsize)

			# cria um ficheiro para guardar os bytes recebidos do ficheiro que esta a ser traduzido
			try:
				os.remove(l + "/" + fname)
				print "File on directory overwritten"
			except:
				print "Translation file created"

			recv_file = open(l + "/" + fname,"wb+")
			try:
				while (fsize > 0):
					socketAccept.settimeout(10)
					data = socketAccept.recv(256)
					fsize -= len(data)
					if (fsize <= 0 and data[-1] == "\n"):
						data = data[:-1]
					elif(fsize <= 0 and data[-1] != "\n"):
						print "File size is too small. Protocol Error! Exiting!"
						raise senderror
					recv_file.write(data)
			except:
				print "Error receiving. Probably file size is wrong. Protocol error! Exiting"
				raise senderror

			recv_file.close()
		except:
			print "Error receiving..."
			raise senderror

	# funcao que trata de enviar o ficheiros para o cliente, dict_files e o dicionario dos ficheiros, fname e o filename e l e a linguagem do TRS
	def send_file(self, dict_files, fname, l):

		# comeco da construcao da string que vai ser enviada para o utilizador como resposta do ficheiro enviado
		msg = "TRR f " + dict_files[fname] + " " + str(os.stat(l + "/" + dict_files[fname]).st_size) + " "
		try:
			socketAccept.send(msg)
		except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to client: UNR ERR"
				print senderror
				return
		#enviar ficheiro
		print "Sending file to client..."

		file_to_trl = open(l + "/" + dict_files[fname],"rb")
		# le ficheiro e envia-o ao cliente
		data = file_to_trl.read(256)
		try:
			while (data):
				socketAccept.send(data)
				data = file_to_trl.read(256)
		except socket.error as senderror:
			if(senderror.errno != errno.ECONNREFUSED):
				raise senderror
			print "SOCKET_ERROR: Error sending message to client: UNR ERR"
			print senderror
			return
		file_to_trl.close()
		try:
			socketAccept.send("\n")
		except socket.error as senderror:
			if(senderror.errno != errno.ECONNREFUSED):
				raise senderror
			print "SOCKET_ERROR: Error sending message to client: UNR ERR"
			print senderror
			return
		print "File sent to client"

	# funcao que trata de receber a mensagem do cliente e perceber se e uma traducao de palavras ou de ficheiros
	def translate_and_send(self, word_dictionary, file_dictionary, lang):

		print 'Got connection from ', addr
		try:
			to_translate = socketAccept.recv(3) #le os tres primeiros bytes da mensagem e confirma o protocolo
		except:
			print "Error receiving..."
			return

		if (to_translate==""): # Quando o user fecha o socket sem ter enviado nada
			print "Error receiving..."
			return
		if ( to_translate != "TRQ"):
			print "Error in Protocol"
			socketAccept.close()
			sys.exit()

		try:
			to_translate = socketAccept.recv(3) # le os 3 bytes seguintes da mensagem
		except:
			print "Error receiving..."
			raise senderror
			return

		if ( to_translate == " t " ):
			try:
				to_translate = socketAccept.recv(1024) # recebe a(s) palavra(s) para traduzir
				print "Word(s) received..."
				transl = self.text_translation(to_translate, word_dictionary) # chama a funcao de traducao
			except:
				print "Error receiving..."
				raise senderror
				return

			try:
				socketAccept.send(transl) # envia a traducao da(s) palavra(s)
				if(transl!="TRR NTA\n"):
					print "Translation sent!"
			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to client: UNR ERR"
				print senderror
				return

		elif ( to_translate == " f " ):
			filename=""
			try:
				byte = socketAccept.recv(1)
				while (byte != " "): #le o nome do ficheiro que e para ser traduzido
					filename += byte
					byte = socketAccept.recv(1)

				print "Filename: " , filename
				self.receive_file(filename, lang) #recebe o ficheiro
			except:
				print "Error receiving..."
				raise senderror
			print "User file received"

			#devolver ficheiro com traducao
			if (filename in file_dictionary):
				print filename + "--->" + file_dictionary[filename]
				self.send_file(file_dictionary, filename, lang) # envia o ficheiro de traducao
				print "Translation sent!"
			else: #quando o ficheiro nao tem traducao no sistema
				socketAccept.send("TRR NTA\n")
				print "Translation not found!"
		else:
			print "Invalid translation request"
			translation = "TRR ERR\n"
			try:
				socketAccept.send(translation)
			except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: UNR ERR"
					print senderror
					return

	def terminateConnection(self):
		self.server.close()

# Classe do socket que serve de meio de comunicacao com o TCS
class socketUDP:
 	#construtor
	def __init__(self, host, port, language):
		self.hostTCS = host
		self.port = port
		self.language = language
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def register(self, portTCP): #funcao de registo com o TCS
		msg = "SRG " + self.language + " " + socket.gethostbyname(socket.gethostname()) + " " + str(portTCP) + "\n"
		addressTCS = (socket.gethostbyname(self.hostTCS), self.port)
		print "Registation on TCS being sent: "
		print addressTCS

		try:
			self.server.sendto(msg, addressTCS)
		except socket.error as senderror:
			if(senderror.errno != errno.ECONNREFUSED):
				print "SENDERROR"
				raise senderror
			print "SOCKET_ERROR: Error sending message to client: UNR ERR"
			print senderror
			return
		print "Waiting for registration confirmation from TCS..."

		reply = self.server.recvfrom(1024) # resposta do TCS

		if (reply[0] == "SRR NOK\n"):
			print "Cannot register. Exiting..."
			self.server.close()
			sys.exit()

		print "TRS successfully registered"

	def terminateConnection(self, portTCP): #funcao que trata de remover o TRS da lista de TRSs do TCS
		msg = "SUN " + self.language + " " + socket.gethostbyname(socket.gethostname()) + " " + str(portTCP) + "\n"
		addressTCS = (socket.gethostbyname(self.hostTCS), self.port)
		print "Unregistation request being sent: "
		print addressTCS

		try:
			self.server.sendto(msg, addressTCS)
		except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to client: UNR ERR"
				print senderror
				return
		print "Waiting for unregistration confirmation from TCS..."
		try:
			self.server.settimeout(10)
			reply = self.server.recvfrom(1024) #resposta do TCS
		except:
			print "Error receiving... TCS does not respond. Aborting. Exiting..."
			sys.exit("TRS Turning off -- System Exit")
		if (reply[0] == "SRR NOK\n"): # Erro do TCS
			print "Cannot unregister. Exiting..."
			self.server.close()
			sys.exit()

		print "TRS successfully unregistered. Exiting..."
		self.server.close()

	def getServer(self):
		return self.server

def deal_with_files(dict_words, dict_files):
#  funcao que poe em dicionarios as palavras e ficheiros que podem ser traduzidos
	lang_file = open(sockUdp.language + "/text_translation.txt","r")

	contentTrans = lang_file.readlines()


	for i in range(len(contentTrans)):
		line_split = contentTrans[i].split(" ")
		dict_words += [(line_split[0], line_split[1][:-1])]

	lang_file.close()
	#

	# criar dicionario com as palavras do ficheiro
	lang_file = open(sockUdp.language + "/file_translation.txt","r")

	contentTrans = lang_file.readlines()


	for i in range(len(contentTrans)):
		line_split = contentTrans[i].split(" ")
		dict_files += [(line_split[0], line_split[1][:-1])]

	lang_file.close()


try:
# trata do input
	registed = 0

	#Parse dos comandos do terminal###########################
	parser = argparse.ArgumentParser()

	parser.add_argument("lang", help="TRS language")
	parser.add_argument("-p", help="TRS port", type=int)
	parser.add_argument("-n", help="TCS host")
	parser.add_argument("-e", help="TCS port", type=int)

	try:
		args = parser.parse_args()
	except:
		print "FORMAT_ERROR: Wrong way to execute this program"
		print "SOLUTION_EXAMPLE: python TRS.py -p 50000 -n tejo.ist.utl.pt -e 58052"
		print "TRS Turning off -- System Exit"
		sys.exit(0)

	port = 59000
	hostTCS = socket.gethostname()
	portTCS = 58052

	if args.p:
		port = args.p

	if args.n:
		hostTCS = args.n

	if args.e:
		portTCS = args.e
	##########################################################

	sockUdp = socketUDP(hostTCS, portTCS, args.lang) # socket UDP de contacto com o TCS
	try:
		sockUdp.getServer().settimeout(10)
		sockUdp.register(port) # regista o TRS no TCS
	except:
		print "TRS does not respond. Please try to initiate TRS again"
		sys.exit("TRS Turning off -- System Exit")

	registed = 1; #flag de estar registado
	print ""

	# criar dicionario com as palavras do ficheiro
	words_translation = []
	file_translation = []

	deal_with_files(words_translation, file_translation)
	words_translation = dict(words_translation)
	file_translation = dict(file_translation)

	sockTCP = socketTCP(port) #cria o socket TCP que serve para contacto com o cliente

	sockTCP.listen(5)

	while(1):
		print "Waiting for a user to contact..."
		socketAccept, addr = sockTCP.server.accept()
		sockTCP.translate_and_send(words_translation, file_translation, sockUdp.language)
		socketAccept.close()
		print ""

except KeyboardInterrupt:
	print '\n'
	print 'KeyboardInterrupt found --- treating Control-C interruption'
except ValueError:
	print "VALUE_ERROR: Invalid port given"
	print "PORT_INT: Port must be an integer"
except socket.error:
	print "SCOKET ERROR"
	print "Aborting...."

except Exception:
	#TODO: ver disto
	print "Cenas"

finally:
	if(registed == 1):
		sockUdp.terminateConnection(port)
	print "TRS Turning off -- System Exit"
	sys.exit(0)
