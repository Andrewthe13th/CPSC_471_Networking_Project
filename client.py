#!/usr/bin/env python3
""""FTP Protocols"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
from socket import *


parser = argparse.ArgumentParser(description="FTP client side")
parser.add_argument("server_name", help='Web address of server')
parser.add_argument("port",  help="server port you wish to connecct to")
args = parser.parse_args()


# Name and port number of the server to
 # which want to conne ct .
server_name = args.server_name
serverPort= args.port

# Create a socket
client_socket = socket(AF_INET , SOCK_STREAM)

#Connect to the server
clientSocket.connect((serverName,serverPort))

#A string we want to send to the server
data = 'Hello world! This is a very long string.'
bytes_sent = 0

#Keep send in gbytes until all bytes are sent
while bytes_sent != len(data):
    pass
    #Send thatstring!
    bytes_sent += clientSocket.send(data[bytesSent:])

#Close the socket
clientSocket.close()
