#!bin/usr/python

#Client 

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "tejo"

port = 58011

#print host

address = (host, port)

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
    
    for i in range(eval(rep[1])):
      print str(i+1) + " - " + rep[i+2]
      
    languages = rep[2:-1] + [rep[-1][:-1]]

  if (command[:7] == "request"):
    print languages
    rep = command.split(" ")
    print "Pedido bla " + rep[1] + "\n"
    
  if (command == "exit"):
    sys.exit("Volte em breve!")

s.close()




	