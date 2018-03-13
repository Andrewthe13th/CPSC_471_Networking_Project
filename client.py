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
#from Crypto.Cipher import AES

class ftp_command(Cmd):
    
    #def encrypt(self):
        #key = 'This is a key123'
        #obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
        #message = "The answer is no"
        #ciphertext = obj.encrypt(message)
        #return ciphertext
    
    #def decrypt(self):
        #ciphertext = self
        #key = 'This is a key123'
        #obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
        #plaintext = obj2.decrypt(ciphertext)
        #plaintext = plaintext.decode()
    
    #TODO: WILL REPLACE CLIENT_SOCKET.SEND TO OUR OWN FORMAT
    def send_data(self):
        pass
    
    #TODO: Will REPLACE CLIENT_SOCKET.RCV TO OUR OWN FORMAT
    def rec_data(self):
        pass
    
        
    #TODO: PAUL IS STILL WORKING ON THIS, MAKING CONNECTIONG AND DL FILE
    def do_get(self, args):
        print(len(args), args)
        if len(args) > 0:
            msg = 'get'
            client_socket.send(msg)
            tmp_port = client_socket.recv(1024)
            try:
                print("Creating socket for download")
                tmp_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                tmp_socket.connect((server_name,tmp_port))
                #TODO DOWNLOAD FILE
                #TODO CHECK FILE HASH
                print("File download is complete")
                tmp_socket.send("close")
                print("Socket for download is closed")
                tmp_socket.close()
                
                
                
            except socket.error as socketerror:
                print("Error: ", socketerror)
            
        else:
            print("get needs the name of the file you are trying to download")


    #TODO OPEN A NEW SOCKET, UPLOAD FILES AND CLOSE SOCKET WHEN DONE
    def do_put(self, args):
        pass
        
    #TODO: FINISHED NEEDS TESTING
    def do_ks(self, args):
        if len(args) == 0:
            msg = 'ls'
            #msg = msg.encrypt()
            print(msg)
            client_socket.send(msg)
            print(client_socket.recv(1024))
            
        else:
            print("ls does not take arguments")
    
    #TODO FINISHED NEEDS TESTING
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
