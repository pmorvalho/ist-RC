#!bin/usr/python

#Server


import socket
import sys
import os
import math
import errno

class socketTCP:

	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def listen(self, n):
		(self.server).listen(n)

	def text_translation(self, to_translate_aux, dict_words):
		to_translate_aux = to_translate_aux.split(" ")
		# try:
		noWords = eval(to_translate_aux[0])
		# except:
		# 	nao e um numero...
		to_translate_aux[noWords] = to_translate_aux[noWords][:-1] # tirar \n

		to_translate_aux = to_translate_aux[1:]
		translation = "TRR t " + str(noWords)
		for i in range(noWords):
			if (to_translate_aux[i] not in dict_words):
				translation += "TRR NTA"
				print "Translation not found!"
				break
			else:
				translation += " " + dict_words[to_translate_aux[i]]
		translation += "\n"
		return translation

	def receive_file(self, fname, l):
		fsize=""
		byte = socketAccept.recv(1)
		while (byte != " "):
			fsize += byte
			byte = socketAccept.recv(1)

		print "File size: " , fsize

		fsize = eval(fsize)

		recv_file = open(l + "/" + fname,"wb+")

		while (fsize > 0):
			data = socketAccept.recv(256)
			recv_file.write(data)
			fsize -= len(data)

		recv_file.close()

	def send_file(self, dict_files, fname, l):

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


	def translate_and_send(self, word_dictionary, file_dictionary, lang):

		print 'Got connection from ', addr

		to_translate = socketAccept.recv(3)

		if ( to_translate != "TRQ"):
			print "ERROR"
			sys.exit()

		to_translate = socketAccept.recv(3)

		if ( to_translate == " t " ):
			to_translate = socketAccept.recv(1024)
			print "Word(s) received..."
			transl = self.text_translation(to_translate, word_dictionary)
			try:
				socketAccept.send(transl)
				print "Translation sent!"
			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to client: UNR ERR"
				print senderror
				return

		elif ( to_translate == " f " ):
			filename=""
			byte = socketAccept.recv(1)
			while (byte != " "):
				filename += byte
				byte = socketAccept.recv(1)

			print "Filename: " , filename
			self.receive_file(filename, lang)

			print "User file received"

			#devolver ficheiro com traducao
			if (filename in file_dictionary):
				print filename + "--->" + file_dictionary[filename]
				self.send_file(file_dictionary, filename, lang)
				print "Translation sent!"
			else:
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


class socketUDP:

	def __init__(self, host, port, language):
		self.hostTCS = host
		self.port = port
		self.language = language
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def register(self, portTCP):
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

		reply = self.server.recvfrom(1024)

		if (reply[0] == "SRR NOK\n"):
			print "Cannot register. Exiting..."
			self.server.close()
			sys.exit()

		print "TRS successfully registered"

	def terminateConnection(self, portTCP):
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

		reply = self.server.recvfrom(1024)

		if (reply[0] == "SRR NOK\n"):
			print "Cannot unregister. Exiting..."
			self.server.close()
			sys.exit()

		print "TRS successfully unregistered. Exiting..."
		self.server.close()

def verify_input_len8(vec):
	if ( (vec[2]=="-p") and (type(eval(vec[3]))==int) ):
		port = eval(vec[3])
		if ( (vec[4]=="-n") and (type(vec[5])==str) ):
			hostTCS = vec[5]
			if ( (vec[6]=="-e") and (type(eval(vec[7]))==int) ):
				portTCS = eval(vec[7])
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	elif( (vec[2]=="-p") and (type(eval(vec[3]))==int) ):
		port = eval(vec[3])
		if ( (vec[4]=="-e") and (type(eval(vec[5]))==int) ):
			portTCS = eval(vec[5])
			if ( (vec[6]=="-n") and (type(vec[7])==str) ):
				hostTCS = vec[7]
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	elif( (vec[2]=="-n") and (type(vec[3])==str) ):
		hostTCS = vec[3]
		if ( (vec[4]=="-p") and (type(eval(vec[5]))==int) ):
			port = eval(vec[5])
			if ( (vec[6]=="-e") and (type(eval(vec[7]))==int) ):
				portTCS = eval(vec[7])
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	elif( (vec[2]=="-n") and (type(vec[3])==str) ):
		hostTCS = vec[3]
		if ( (vec[4]=="-e") and (type(eval(vec[5]))==int) ):
			portTCS = eval(vec[5])
			if ( (vec[6]=="-p") and (type(eval(vec[7]))==int) ):
				port = eval(vec[7])
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	elif( (vec[2]=="-e") and (type(eval(vec[3]))==int) ):
		portTCS = eval(vec[3])
		if ( (vec[4]=="-p") and (type(eval(vec[5]))==int) ):
			port = eval(vec[5])
			if ( (vec[6]=="-n") and (type(vec[7])==str) ):
				hostTCS = vec[7]
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	elif( (vec[2]=="-e") and (type(eval(vec[3]))==int) ):
		portTCS = eval(vec[3])
		if ( (vec[4]=="-n") and (type(vec[5])==str) ):
			hostTCS = vec[5]
			if ( (vec[6]=="-p") and (type(eval(vec[7]))==int) ):
				port = eval(vec[7])
				return port, portTCS, hostTCS
			else:
				raise Exception
		else:
			raise Exception
	else:
		raise Exception

def verify_input_len6(vec):
	if ( (vec[2]=="-p") and (type(eval(vec[3]))==int) ):
		port = eval(vec[3])
		if ( (vec[4]=="-n") and (type(vec[5])==str) ):
			hostTCS = vec[5]
			portTCS = 58052
			return port, portTCS, hostTCS
		elif ( (vec[4]=="-e") and (type(eval(vec[5]))==int) ):
			portTCS = eval(vec[5])
			hostTCS = socket.gethostname()
			return port, portTCS, hostTCS
		else:
			raise Exception
	elif( (vec[2]=="-n") and (type(vec[3])==str) ):
		hostTCS = vec[3]
		if ( (vec[4]=="-p") and (type(eval(vec[5]))==int) ):
			port = eval(vec[5])
			portTCS = 58052
			return port, portTCS, hostTCS
		elif ( (vec[4]=="-e") and (type(eval(vec[5]))==int) ):
			portTCS = eval(vec[5])
			port = 59000
			return port, portTCS, hostTCS
		else:
			raise Exception
	elif( (vec[2]=="-e") and (type(eval(vec[3]))==int) ):
		portTCS = eval(vec[3])
		if ( (vec[4]=="-p") and (type(eval(vec[5]))==int) ):
			port = eval(vec[5])
			hostTCS = socket.gethostname()
			return port, portTCS, hostTCS
		elif ( (vec[4]=="-n") and (type(vec[5])==str) ):
			hostTCS = vec[5]
			port = 59000
			return port, portTCS, hostTCS
		else:
			raise Exception
	else:
		raise Exception

def verify_input_len4(vec):
	if ( (vec[2]=="-p") and (type(eval(vec[3]))==int) ):
		port = eval(vec[3])
		hostTCS = socket.gethostname()
		portTCS = 58052
		return port, portTCS, hostTCS
	elif( (vec[2]=="-n") and (type(vec[3])==str) ):
		hostTCS = vec[3]
		port = 59000
		portTCS = 58052
		return port, portTCS, hostTCS
	elif( (vec[2]=="-e") and (type(eval(vec[3]))==int) ):
		portTCS = eval(vec[3])
		port = 59000
		hostTCS = socket.gethostname()
		return port, portTCS, hostTCS
	else:
		raise Exception


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
	if (len(sys.argv) == 8):
		port, portTCS, hostTCS = verify_input_len8(sys.argv)
	elif (len(sys.argv) == 6):
		port, portTCS, hostTCS = verify_input_len6(sys.argv)
	elif (len(sys.argv) == 4):
		port, portTCS, hostTCS = verify_input_len4(sys.argv)
	elif (len(sys.argv) == 2):
		port = 59000
		hostTCS = socket.gethostname()
		portTCS = 58052
	else:
		raise Exception

	sockUdp = socketUDP(hostTCS, portTCS, sys.argv[1])
	sockUdp.register(port);
	registed = 1;
	print ""

	################## criar dicionario com as palavras do ficheiro #####################
	words_translation = []
	file_translation = []

	deal_with_files(words_translation, file_translation)
	words_translation = dict(words_translation)
	file_translation = dict(file_translation)

	###################################################################################
	sockTCP = socketTCP(port)

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

except Exception:
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python TRS.py -p 50000 -n tejo.ist.utl.pt -e 58052"



finally:
	if( registed == 1):
		sockUdp.terminateConnection(port)
	print "TRS Turning off -- System Exit"
	sys.exit(0)
