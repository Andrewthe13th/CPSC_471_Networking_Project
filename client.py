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
#import subprocess

class ftp_command(Cmd):

    def do_hello(self, args): #command examples
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print (name)
        
    #TODO: Open a new socket, DL file, close socket    
    def do_get(self, args):
        pass
    
    #TODO Open a new socket, Upload file, close socket
    def do_put(self, args):
        pass

    #TODO: FINISHED NEEDS TESTING
    def do_ks(self, args):
        if len(args) == 0:
            msg = 'ls'
            client_socket.send(msg)
            print(client_socket.recv(1024))
            
        else:
            print("ls does not take arguments")
    
    #TODO close all remaining sockets and close the clients connection. Check for active DL/upload connections?
    def do_quit(self, args):
        if len(args) == 0:
            msg = 'quit'
            client_socket.send(msg)
            print(client_socket.recv(1024))
            return True
        else:
            print("quit takes no arguments")

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
    prompt = ftp_command()
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
print("Command Socket Closed")
