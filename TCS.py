#!bin/usr/python

"""
	Este e o codigo do Server
	Estudantes que participaram no desenvolvimento deste projeto:
		David Calhas 
		Joao Silveira
		Pedro Orvalho
"""


#Imports made for the execution of this application
import socket
import errno
import sys
import time



"""
	Classe socketServer
	esta classe e a representacao do socket pelo qual se faz a comunicacao com os users e TRS servers
	Atributos:

		host - nome do host onde o TCS esta a correr
		port - numero do porto pelo qual e feita a comunicacao
		server - o socket em si

"""

class socketServer:
	


	def __init__(self, port):
		try:
			self.host = socket.gethostname()
			self.port = port
			self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server.bind((self.host, self.port))

		except Exception:#In case the creation of the socket creates an error
			print "SOCK_ERROR: Error creating socket"#Message to warn the user of the current situation
			time.sleep(10.0)#Random time to wait before we try to create the socket again
			print "SOCK_RETRY: Retrying in 10 seconds"
			socketServer(port)#Retrying to create the socket

	"""
		Metodo contact da classe socketServer
		Este metodo e o algoritmo do processo de comunicacao
	"""

	def contact(self, languages, lnames):
		print "Waiting for contact from someone"


		try:
			self.server.settimeout(300.0)#Este timeout serve apenas para o utilizador saber que estamos vivos
			msg, addr = self.server.recvfrom(1024)#Rececao de uma mensagem de no maximo 1024 bytes
		except Exception:
			print "CONN_TIMEOUT: Just waited 5 minutes for a connection and didn't get one"
			print "CONN_RETRY: Retrying to get connection"
			return#Como existe um loop que esta sempre a chamar o contact a comunicacao e feita novamente


		message = msg.split(" ")#split do message por espacos para analisar a primeira palavra e as seguintes
		print "Just received messaged: from IP:" + addr[0] + ' from Port:' + str(addr[1])
		print "Message received: " + msg

		if (msg[:3] == "ULQ"):
			if(len(languages) == 0):#se o tamanho do dicionario languages for zero quer dizer que ainda nao existem servidores TRS's registados
				try:
					self.server.sendto("ULR EOF\n", addr)#Envio do erro a aplicacao do utilizador
					print "ERROR_ULR: there are no TRS services available"
					return
				except socket.error as senderror:#Tratamento de um erro, pode acontecer caso exista um erro na chamada de sistema sendto
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: ULR EOF"
					print senderror
					return



			if(len(message) > 1):#A mensagem deve so conter uma palavra 'ULQ' se conter mais quer dizer que existe um erro no seu formato
				try:
					self.server.sendto("ULR ERR\n", addr)#Envio para a aplicacao do utilizador a dizer que houve um erro no formato da mensagem enviada por parte dele
					print "ERROR_ULR: messsage format corrupted"
					return
				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: ULR ERR"
					print senderror
					return

			msg_lang = "ULR " + str(len(languages))#Construcao da resposta ao comando 'ULQ' que vai ser 'ULR NL L1 L2 ... LN'

			for i in range(len(languages)):
				msg_lang += " " + lnames[i]#Concatenacao de todas as linguagens que tem um servidor TRS registado numa so string

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
		elif (msg[:3] == "UNQ"):#Tratamento da mensagem 'UNQ'
			if(len(message) != 2):#Se o tamanho da mensagem for diferente de dois entao avisa se a aplicacao do utilizador que existe um erro no formato da mensagem
				print "ERROR_UNQ: message sent from user is corrupted"
				try:
					self.server.sendto('UNR ERR\n', addr)
					return
				except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to client: UNR ERR"
						print senderror
						return

			TRS_lang = message[1][:-1]#Aqui vai se buscar a string message o numero da linguagem com a qual a aplicacao do utilizador se quer conectar
			
			try:
				TRS_info = languages[TRS_lang]#TRS_info vai conter o nome da linguagem, o ip do servidor TRS correspondente e o respetivo port pelo qual e feita a comunicacao
			except:
				print "ERROR_UNQ: invalid language name"
				try:
					self.server.sendto('UNR EOF\n', addr)
					return

				except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to client: UNR EOF"
						print senderror
						return

			TRS_ip = TRS_info[0]#nome da linguagem
			TRS_port = TRS_info[1]#ip do servidor TRS's 

			print "User app wants to connect to the following TRS - Language: " , TRS_lang , " IP: " , TRS_ip , " Port: " , TRS_port
			try:
				#Envio a aplicacao do servidor da mensagem com o formato de acordo com o enunciado contendo o port e o ip do servidor TRS
				self.server.sendto('UNR ' + TRS_ip + ' ' + str(TRS_port) + '\n', addr)

			except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to client: UNR"
					print senderror
					return

		elif (msg[:3] == "SRG"):
				if(len(message) != 4): #Se o tamanho de uma mensagem com SRG no inicio for diferente de 4, entao quer dizer que a mensagem esta corrupta
					try:
						print "error in SRG format from TRS"
						self.server.sendto("SRR ERR\n", addr)
						return
					except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: SRR ERR"
						print senderror
						return


				#Neste if e feita a verificacao de se a linguagem do TRS que se quer registar ja existe e se o ip e port do mesmo tambem ja esta registado
				if (message[1] in lnames or (message[2],eval(message[3])) in languages.values()):
					try:
						print "SRG_ERROR: error registrating TRS service"
						self.server.sendto('SRR NOK\n', addr)#Se passou no if acima entao e enviado ao servidor TRS que nao foi registado
						return
					except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to TRS server: SRR NOK"
						print senderror
						return

				#E adicionado ao dicionario languages um elemento com key - nome da linguagem com o respetivo tuplo - (ip, porto)
				languages[message[1]] = (message[2],eval(message[3]))
				lnames += [message[1]]
				print languages[message[1]]
				print "Successfully registrated TRS service: " + message[1] + "\n"
				try:
					self.server.sendto('SRR OK\n', addr)
				except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to TRS server: SRR OK"
					print senderror
					return



		elif (msg[:3] == "SUN"):
			# remove do fich um TRS de uma certa linguagem
			TRS_lang = message[1]
			if(len(message) != 4): #Se uma mensagem com a palavra inicial SUN nao tiver 4 palavras entao quer dizer que o seu formato e corrupto
				print "SUN_ERROR: message sent is corrupted"
				return
			try:
				if (languages[TRS_lang] == (message[2], eval(message[3]))):#Verificacao do servidor TRS no dicionario de linguagens registadas
					lnames.remove(TRS_lang)#remocao do servidor TRS
					languages.pop(TRS_lang)
					status_SUN = "OK\n"
					print "Successfully removed TRS service: " + message[1]
				else:
					status_SUN = "NOK\n"
					print "SUN_WARNING: TRS service not removed: " + message[1]

				self.server.sendto('SUR ' + status_SUN, addr)#Envio ao servidor TRS a mensagem a dizer se foi ou nao feita com sucesso a sua remocao

			except socket.error as senderror:#Tratamento de um erro que possa existir na chamada de sistema sendto
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message SUR to TRS server"
				print senderror
				return

		else:
			print "CONN_ERROR: Received message with worng format"
			return 




	#Este metodo faz a atualizacao do ficheiro languages.txt de acordo com o conteudo no dicionario languages
	def updateLanguages(self, file, languages, lnames):
		lang_f = open("languages.txt", "w")
		print "Languages being added to languages.txt"
		print "Number of languages being written to the languages.txt file: " + str(len(languages))
		for i in range(len(languages)):#percorre todos os elementos em languages
			lang = lnames[i]
			print "Adding language: " + lang
			lang_f.write(lang + ' ' + languages[lang][0] + ' ' + str(languages[lang][1]) + '\n')#Escrita no ficheiro do TRS com a respetiva linguagem, ip e porto
		lang_f.close()
	
	#Este metodo fecha o socket
	#So e feita a sua chamada quando o programa acaba
	def terminateConnection(self):
		self.server.close()

lang_f = open("languages.txt", "a+")

fileLang_lines = lang_f.readlines()

langs = []
lang_names = []

for i in range(len(fileLang_lines)):#E feita uma lista que contem um tuplo (string, tuple) em cada posicao e contem todas as linguagens registadas
	file_line = fileLang_lines[i].split(" ")
	lang_names += [file_line[0]]
	langs += [(file_line[0], (file_line[1], eval(file_line[2])))]

langs = dict(langs)#Transforma a lista langs num dicionario

print "Number of languages: " + str(len(langs))

try:
	if (len(sys.argv) == 3):#Verificacao de input, neste caso se input for igual a 3 entao espera se que exista '...... -p PORT'
		if(sys.argv[1] == '-p'):
			s = socketServer(int(sys.argv[2]))
		else:
			raise Exception

	else:
		s = socketServer(58052)#Criacao do socket tendo o port um valor default que nos foi indicado no enunciado

	#estar a prova de erros!!

	print socket.gethostname()

	while(1):#Loop para fazer a comunicacao
		s.contact(langs, lang_names)

	s.updateLanguages(lang_f, langs, lang_names)#Atualiza o ficheiro languages.txt
	s.terminateConnection()#Termina programa




except KeyboardInterrupt:#Trata a interrupcao Control-C
	print '\n'
	print 'KeyboardInterrupt found --- treating Control-C interruption'
	s.updateLanguages(lang_f, langs, lang_names)
	s.terminateConnection()

except ValueError:#Trata o erro de o porto dado nao ser um inteiro
	print "VALUE_ERROR: Invalid port given"
	print "PORT_INT: Port must be an integer"

except Exception:#Trata o erro de o formato de chamada do programa ser errado
	print "FORMAT_ERROR: Wrong way to execute this program"
	print "SOLUTION_EXAMPLE: python TCS.py -p 50000"

except socket.gaierror:#Trata erro na chamada de sistema gethostname
	print "SOCKET_ERROR: Failed to get host name"


finally:#Este pedaco de codigo e sempre executado
	print "TCS Turning off -- System Exit"
	sys.exit(0)




# Italiano 123.345.566. 50000
# Alemao 123.345.566. 50000
# Ingles 123.345.566. 50000
# Frances 123.345.566. 50000