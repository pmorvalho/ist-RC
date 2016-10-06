#!bin/usr/python

#Server


import socket
import sys
import os
import math

class socketTCP:

	def __init__(self, port):
		self.host = socket.gethostname()
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host, self.port))

	def listen(self, n):
		(self.server).listen(n)

	def translate_and_send(self, word_dictionary, file_dictionary, lang):
		c, addr = self.server.accept()

		print 'Got connection from ', addr

		to_translate = c.recv(3)

		print to_translate
		
		if ( to_translate != "TRQ"):
			print "ERROR"
			sys.exit()
		
		to_translate = c.recv(3)
		
		if ( to_translate == " t " ):
		
			to_translate = c.recv(1024)

			to_translate = to_translate.split(" ")

			# try:
			noWords = eval(to_translate[0])
			# except:
			# 	nao e um numero...
			to_translate[noWords] = to_translate[noWords][:-1] # tirar \n

		  

			to_translate = to_translate[1:]

			translation = "TRR t " + str(noWords)

			for i in range(noWords):
				if (to_translate[i] not in word_dictionary):
					translation = "TRR NTA"
					break
				else:
					translation += " " + word_dictionary[to_translate[i]]
			translation += "\n"

			print translation
			c.send(translation)
			
		elif ( to_translate == " f " ):

			byte = c.recv(1)
			filename = ""

			while (byte != " "):
				filename += byte
				byte = c.recv(1)

			print "Filename: " , filename

			byte = c.recv(1)
			filesize = ""

			while (byte != " "):
				filesize += byte
				byte = c.recv(1)

			print "File size: " , filesize

			filesize = eval(filesize)

			recv_file = open(lang + "/" + filename,"wb+")

			packs_no = filesize / 256

			if ( (filesize % 256) != 0 ):
				packs_no += 1

			print packs_no

			for i in range(packs_no):
				data = c.recv(256)
				recv_file.write(data)

			print type(data)
			
			recv_file.close()

			print "User file received"

			#devolver ficheiro com traducao

			msg = "TRR f " + file_dictionary[filename] + " " + str(os.stat(lang + "/" + file_dictionary[filename]).st_size) + " "

			c.send(msg)

			#enviar ficheiro
			print "Sending file to client..."
			  	
			file_to_trl = open(lang + "/" + file_dictionary[filename],"rb")
			
			#########################################
			print "Sending file to client..."
			data = file_to_trl.read(256)

			while (data):
				c.send(data)
				data = file_to_trl.read(256)

			file_to_trl.close()
	      	
			c.send("\n")

			print "File sent to client"
	        #########################################

		else:
			print "Invalid translation request"
			translation = "TRR ERR\n"
			c.send(translation)

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
			self.server.close()
			sys.exit()

		print "TRS successfully registered"

	def contact(self):
		msg, addr = self.server.recvfrom(1024)

		print msg

		#ALTERAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



		print "Vai printar addr"
		print addr

	def terminateConnection(self, portTCP):
		msg = "SUN " + self.language + " " + socket.gethostbyname(socket.gethostname()) + " " + str(portTCP) + "\n"
		addressTCS = (socket.gethostbyname(socket.gethostname()), self.port)
		print "Unregistation request being sent: "
		print addressTCS

		self.server.sendto(msg, addressTCS)

		print "Waiting for unregistration confirmation from TCS..."

		reply = self.server.recvfrom(1024)

		if (reply[0] == "SRR NOK\n"):
			print "Cannot unregister. Exiting..."
			self.server.close()
			sys.exit()

		print "TRS successfully unregistered. Exiting..."
		self.server.close()

def verify_input_len8(vec):
	if ( (vec[2]=="-p") or (type(eval(vec[3]))==int) ):
		if ( (vec[4]=="-n") or (type(vec[5])==str) ):
			if ( (vec[6]=="-e") or (type(eval(vec[7]))==int) ):
				return
			else:
				raise Exception
		else:
			raise Exception
	else:	
		raise Exception

def verify_final_input(port_TRS, nameTCS, port_TCS):
	if((type(port_TRS)!=int) or (type(nameTCS)!=str) or (type(port_TCS)!=int)):
		raise Exception


# Input
try: 

	if (len(sys.argv) == 8):
		verify_input_len8(sys.argv)
		port = eval(sys.argv[3])
		hostTCS = sys.argv[5]
		portTCS = eval(sys.argv[7])
		
	elif (len(sys.argv) == 6):
		if (sys.argv[2] == "-p"):
			port = eval(sys.argv[3])
			if (sys.argv[4] == "-n"):
				hostTCS = sys.argv[5]
				portTCS = 58052
				
			elif (sys.argv[4] == "-e"):
				portTCS = eval(sys.argv[5])
				hostTCS = socket.gethostname()
				
		elif (sys.argv[2] == "-n"):
			hostTCS = sys.argv[3]
			portTCS = eval(sys.argv[5])
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
			portTCS = eval(sys.argv[3])
			port = 59000
			hostTCS = socket.gethostname()
			
	elif (len(sys.argv)==2):
		port = 59000
		hostTCS = socket.gethostname()
		portTCS = 58052
	else:
		raise Exception


	verify_final_input(port, hostTCS, portTCS)


	sockUdp = socketUDP(socket.gethostname(), portTCS, sys.argv[1])

	sockUdp.register(port);

	# criar dicionario com as palavras do ficheiro

	lang_file = open(sockUdp.language + "/text_translation.txt","r")

	contentTrans = lang_file.readlines()

	words_translation = []
	for i in range(len(contentTrans)):
		line_split = contentTrans[i].split(" ")
		words_translation += [(line_split[0], line_split[1][:-1])]

	words_translation = dict(words_translation)
	lang_file.close()
	#

	# criar dicionario com as palavras do ficheiro
	lang_file = open(sockUdp.language + "/file_translation.txt","r")

	contentTrans = lang_file.readlines()

	file_translation = []
	for i in range(len(contentTrans)):
		line_split = contentTrans[i].split(" ")
		file_translation += [(line_split[0], line_split[1][:-1])]

	file_translation = dict(file_translation)
	lang_file.close()

	print file_translation

	sockTCP = socketTCP(port)	

	sockTCP.listen(5)

	while(1):

		sockTCP.translate_and_send(words_translation, file_translation, sockUdp.language)

except KeyboardInterrupt:
	print '\n'
	print 'KeyboardInterrupt found --- treating Control-C interruption'
	sockUdp.terminateConnection(port)
except ValueError:
	print "VALUE_ERROR: Invalid port given"
	print "PORT_INT: Port must be an integer"

except Exception:
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python TRS.py -p 50000 -n tejo.ist.utl.pt -e 58052"



finally:
	print "TRS Turning off -- System Exit"
	sys.exit(0)
