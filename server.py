#!/usr/bin/env python3
""""FTP Protocols Server"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
import socket
import sys

parser = argparse.ArgumentParser(description="FTP server side")
parser.add_argument("port",  help="server port you wish to listen on")
args = parser.parse_args()

server_port = args.port

if server_port.isdigit():
    server_port = int(server_port)
else:
    print("The port {} is in the wrong format".format(server_port))
    sys.exit()


server_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)

server_socket.bind(('',server_port))

server_socket.listen(1)
print ('The serverisready to receive')

data =''
while 1:
    print("waiting")
    connection_socket ,addr = server_socket.accept()
    tmpBuff= ''

    while len(data) != 40:
        tmpBuff = connection_socket.recv(40)
        if not tmpBuff :
            break
        data += tmpBuff
print (data)

connection_socket.close()
print("socket closed")
