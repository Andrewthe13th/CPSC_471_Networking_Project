#!/usr/bin/env python3
""""FTP Protocols Server"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
from socket import *


parser = argparse.ArgumentParser(description="FTP server side")
parser.add_argument("port",  help="server port you wish to listen on")
args = parser.parse_args()

#Theporton which to listen
server_port = args.port
# Create a TCP socket
serversocket = socket(AF_INET ,SOCK_STREAM)

#Bind the socket to the port
server_socket.bind((' ',server_port))
#Startlisteningforincomingconnectons

server_socket.listen(1)
print ('The serverisready to receive')

# Forever accept incoming connections
while 1:

    # Accept a c o n n e c tio n ; get c l i e n t ’ s s o c k e t

    connection_socket ,addr = server_socket.accept()

    # The temporary b u f f e r
    tmpBuff= ''

    while len(data) != 40:
        # Receive whatever the newly conne c te d c l i e n t has to send
        tmpBuff = connection_socket.recv(40)

        # The o th e r s i de u n e x p e c t e d l y c l o s e d i t ’ s s o c k e t
        if not tmpBuff :
            break
        data += tmpBuff


print (data)

# Close the s o c k e t
connection_socket.close()
