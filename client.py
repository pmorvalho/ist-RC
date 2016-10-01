#!bin/usr/python

#Client

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "tejo.ist.utl.pt"

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
    rep = command.split(" ")
    lang = eval(rep[1]) - 1

    msg = "UNQ " + languages[lang] + "\n"
    print msg

    s.sendto(msg, address)

    d = s.recvfrom(1024)
    reply = d[0]

    rep = reply.split(" ")

    ipTRS = rep[1]
    portTRS = eval(rep[2])
    hostTRS = socket.gethostbyaddr(ipTRS)[0]
    addressTRS = (socket.gethostbyname("194.210.231.23"),50000)

    print addressTRS

    #print "IP: " + portTRS + " Port: " + ipTRS

    socketTRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socketTRS.connect(addressTRS)

    socketTRS.send("Hello bby")

    print socketTRS.recv(200)

    socketTRS.close()
    
  if (command == "exit"):
    sys.exit("Volte em breve!")

s.close()

