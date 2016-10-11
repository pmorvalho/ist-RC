#!bin/usr/python

#Client

import socket
import sys
import os
import errno
import time


def shutApp(): 
  s.close()
  sys.exit("Thank you! Come again")

def list_languages(sock,lang):
  #raise an exception if necessary 
  d = sock.recvfrom(1024)
  reply = d[0]
  addr = d[1]

  rep = reply.split(" ")

  if (rep[0] != "ULR"):
    print "TCS reply does not comply with te protocol"
  elif ( rep[1] == "EOF\n" ): #caso nao haja linguagens disponiveis
    print "No languages available"
  elif (rep[1] == "ERR\n"):
    print "ULQ request wrongly formatted"
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

while(1):
  try:
    command = raw_input("Command: ")
  except IOError:
    print "INPUT_ERROR: error reading input"
    continue

  
  if (command == "list"):
    msg = "ULQ\n"

    try:
      s.sendto(msg, address)
    except socket.error as senderror:
      if(senderror.errno != errno.ECONNREFUSED):
        raise senderror
      print "SOCKET_ERROR: Error sending message to TCS server: ULQ"
      print senderror
      continue

    languages = []

    list_languages(s,languages)

  if (command[:7] == "request"):
    
    comm = command.split(" ") #lista com os varios argumentos do comando
    
    try: 
      lang = eval(comm[1]) - 1
    except:
      print "Language index not valid"
      continue
    
    if (len(languages) == 0):
      print "No languages. Try using 'list' first"
      
    elif (lang >= len(languages) or lang < 0):
      print "Language index not valid"
      
    else: #Envia mensagem ao TCS
      
      msg = "UNQ " + languages[lang] + "\n"
      
      try:
        s.sendto(msg, address)
      except socket.error as senderror:
        if(senderror.errno != errno.ECONNREFUSED):
          raise senderror
        print "SOCKET_ERROR: Error sending message to TCS: UNQ"
        print senderror
        #TODO: sair graciosamente
        continue

      try:
        d = s.recvfrom(1024)
      except:
        print "SOCKET_ERROR: Error receiving message from TCS: UNR expected"
        print senderror
        #TODO: sair graciosamente

      reply = d[0]

      rep = reply.split(" ")

      if (rep[0] != "UNR"):
        print "Wrong message received from TCS (ainda falta abandonar de forma graciosa)"
        #TODO: sair graciosamente
        sys.exit()

      if (rep[1] == "EOF"):
        print "Translation request could not be completed (ainda falta abandonar de forma graciosa)"
        #TODO: sair graciosamente
        sys.exit()

      elif (rep[1] == "ERR"):
        print "UNR ERR (ainda falta abandonar de forma graciosa)"
        #TODO: sair graciosamente
        sys.exit()

      #TODO: mandar try aqui
      ipTRS = rep[1]
      portTRS = eval(rep[2])
      hostTRS = socket.gethostbyaddr(ipTRS)[0]
      addressTRS = (hostTRS,portTRS)
      
      socketTRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      while(1):
        try:
          socketTRS.connect(addressTRS)
          break
        except socket.error as err:
          print "SOCKET_ERROR: Failed connecting"

      
      if (comm[2] == "t"):
      	nWords = len(comm[3:])
      	msg = "TRQ t " + str(nWords)
      	for i in range(nWords):
      	  msg += " " + comm[3:][i]
      	msg += "\n"
      	print "Sent to TRS: " + msg

        try:
          socketTRS.send(msg)

        except socket.error as senderror:
          if(senderror.errno != errno.ECONNREFUSED):
            raise senderror
          print "SOCKET_ERROR: Error sending message to TRS server: msg"
          print senderror
          print "(falta abandonar de forma graciosa)"
          sys.exit()

      	msg = socketTRS.recv(1024)

      	msg = msg.split(" ")

      	translation = ""

      	for i in range(len(msg[3:])):
      	  translation += " " + msg[3:][i]

        # Verificar se deu TRR ERR ou TRR NTA

      	print "Translation:" , translation

      elif (comm[2] == "f"):
      	msg = "TRQ f " + comm[3] + " " + str(os.stat(comm[3]).st_size) + " "
      	print msg

        try:
          socketTRS.send(msg)
        except socket.error as senderror:
          if(senderror.errno != errno.ECONNREFUSED):
            raise senderror
          print "SOCKET_ERROR: Error sending message to TRS server: msg"
          print senderror
          continue
        
        #enviar ficheiro
        print "Uploading file to server..."
        
        file_to_trl = open(comm[3],"rb")
      	
      	data = file_to_trl.read(256)

        while (data):
          try:
            socketTRS.send(data)

          except socket.error as senderror:
            if(senderror.errno != errno.ECONNREFUSED):
              raise senderror
            print "SOCKET_ERROR: Error sending message to TRS server: (BINARY DATA)"
            print senderror
            continue

          data = file_to_trl.read(256)

        file_to_trl.close()
      	
        try:
      	  socketTRS.send("\n")
        except socket.error as senderror:
          if(senderror.errno != errno.ECONNREFUSED):
            raise senderror
          print "SOCKET_ERROR: Error sending message to TRS server: (EXTRA FORMAT)"
          print senderror
          continue

        print "File uploaded"

      	#recepcao do ficheiro

        translated = socketTRS.recv(3)

        if ( translated != "TRR"):
          print "Error receiving file translation"
          sys.exit()
        
        translated = socketTRS.recv(3)

        if (translated != " f "):
          print "Error in message format"
          sys.exit()

        #####################################################################
        byte = socketTRS.recv(1)
        filename = ""

        while (byte != " "):
          filename += byte
          byte = socketTRS.recv(1)

        print "Filename: " , filename

        byte = socketTRS.recv(1)
        filesize = ""

        while (byte != " "):
          filesize += byte
          byte = socketTRS.recv(1)

        print "File size: " , filesize

        print "Downloading file..."

        ################################################################
        filesize = eval(filesize)

        recv_file = open("translation_" + filename,"wb+")

        while (filesize > 0):
          data = socketTRS.recv(256)
          recv_file.write(data)
          filesize -= len(data)

        recv_file.close()

        print "Download complete"

      else:
        print "Command wrongly formatted"
        socketTRS.close()
        continue


      socketTRS.close()
    
  if (command == "exit"):
    shutApp()


