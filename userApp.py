#!bin/usr/python

#Client

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if (len(sys.argv) == 3):
  if (sys.argv[1] == "-n"):
    host = sys.argv[2]
    port = 58052
  elif (sys.argv[1] == "-p"):
    port = sys.argv[2]
    host = "localhost"

elif (len(sys.argv) == 5):
  if (sys.argv[1] == "-n"):
    host = sys.argv[2]
    if(sys.argv[3] == "-p"):
      port = sys.argv[4]
  elif (sys.argv[1] == "-p"):
    port = sys.argv[2]
    if(sys.argv[3] == "-n"):
      host = sys.argv[4]

else:
  host = socket.gethostname()
  port = 58052

#print host

address = (host, port)

print(address)

#s.connect(address)

#ip = socket.gethostbyname(host)

#print "Got connection to server ->  IPaddress", address[0], " port:", ip

#raw_input("Please enter the message you wish to send: ")

while(1):
  command = raw_input("Command: ")
  
  if (command == "list"):
    msg = "ULQ\n"

    s.sendto(msg, address)

    d = s.recvfrom(1024)
    reply = d[0]
    addr = d[1]
    
    rep = reply.split(" ")

    #caso nao haja linguagens disponiveis
    if ( eval(rep[1]) == 0 ):
      print "Nao ha linguagens disponiveis"
    else:
      for i in range(eval(rep[1])):
        print str(i+1) + " - " + rep[i+2]
        
      languages = rep[2:-1] + [rep[-1][:-1]]

  if (command[:7] == "request"):
    comm = command.split(" ")
    lang = eval(comm[1]) - 1

    msg = "UNQ " + languages[lang] + "\n"

    s.sendto(msg, address)

    d = s.recvfrom(1024)
    reply = d[0]

    rep = reply.split(" ")

    if ( rep[0] != "UNR" ):
      print "Algo esta mal..."

    ipTRS = rep[1]
    portTRS = eval(rep[2])
    hostTRS = socket.gethostbyaddr(ipTRS)[0]
    addressTRS = (hostTRS,portTRS)
    #addressTRS = (socket.gethostname(),59000) #LALALALALALALALALALALALALLALALALALALALALALALLALALA

    print "Cenas maradas a acontecer: "

    print addressTRS

    #print "IP: " + portTRS + " Port: " + ipTRS

    socketTRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketTRS.connect(addressTRS)

    if (comm[2] == "t"):
      nWords = len(comm[3:])
      msg = "TRQ t " + str(nWords)
      for i in range(nWords):
        msg += " " + comm[3:][i]
      msg += "\n"
      print "Texto a traduzir: " + msg
      socketTRS.send(msg)

      msg = socketTRS.recv(1024)

      msg = msg.split(" ")

      translation = ""

      for i in range(len(msg[3:])):
        translation += msg[3:][i]

      print translation

    if (comm[2] == "f"):
      msg = "TRQ f " + comm[3] + " " + "size" + " " + "data" + "\n"
      print msg

    socketTRS.close()
    
  if (command == "exit"):
    sys.exit("Volte em breve!")

s.close()
