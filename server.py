#!bin/usr/python

#Server


import socket	

address = socket.gethostname()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




server.bind((address,50000))



server.listen(5)

c, addr = server.accept()



print 'Got connection from', addr
print c.recv(400)


c.send('Thank you for your connection :)   (.)(.)  (.)|(.)  (.)\(.)  (.)|(.)   (.)/(.) <3')





c.close()



server.close()