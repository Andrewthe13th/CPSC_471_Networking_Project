#!/usr/bin/env python3
""""FTP Protocols"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
import socket
import sys
from cmd import Cmd


class ftp_Command(Cmd):

    def do_hello(self, args): #command examples
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print (name)

    def do_quit(self, args):
        """Quits the program."""
        raise SystemExit

parser = argparse.ArgumentParser(description="FTP client side")
parser.add_argument("server_name", help='Web address of server')
parser.add_argument("port",  help="server port you wish to connecct to")
args = parser.parse_args()

server_name = args.server_name
server_port= args.port

if server_port.isdigit():
    server_port = int(server_port)
else:
    print("The port {} is in the wrong format".format(server_port))
    sys.exit()

try:
    print("Creating socket")
    client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    print("Connecting to server")
    client_socket.connect((server_name,server_port))
    print("Setting up FTP commands")
    prompt = ftp_Command()
    prompt.prompt = 'ftp> '
    prompt.cmdloop('FTP connection established')
except socket.error as socketerror:
    print("Error: ", socketerror)






#data = 'Hello world! This is a very long string.'
#bytes_sent = 0


#while bytes_sent != len(data):
#    pass
#    bytes_sent += client_socket.send(data[bytesSent:])

client_socket.close()
