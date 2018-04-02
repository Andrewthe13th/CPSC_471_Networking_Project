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



#TODO: WILL REPLACE CLIENT_SOCKET.SEND TO OUR OWN FORMAT
def send_data(data):
    data_size = str(len(data))

    while len(data_size) < 10:
        data_size = "0" + data_size
    
    data = data_size + data
    
    data_sent = 0
    while data_sent != len(data):
        data_sent += client_socket.send(data[data_sent:])
    

#TODO: Will REPLACE CLIENT_SOCKET.RCV TO OUR OWN FORMAT
def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""
    while len(recvBuff) < numBytes:
        tmpBuff =  sock.recv(numBytes)
        # The other side has closed the socket
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff
    
def recv(sock):
    data = ""
    file_size = 0	
    file_size_buff = ""
    file_size_buff = recvAll(sock, 10)
    file_size = int(file_size_buff)
    data = recvAll(sock, file_size)
    return data
    
class ftp_command(Cmd):
    #TODO: PAUL IS STILL WORKING ON THIS, MAKING CONNECTIONG AND DL FILE
    def do_get(self, args):
        if len(args) > 0:
            msg = 'get'
            send_data(msg)
            tmp_port = client_socket.recv(10)
            print(tmp_port)
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
    def do_ls(self, args):
        if len(args) == 0:
            msg = 'ls'
            send_data(msg)
            tmp = ""
            while 1:
                #WARNING infinite loop
                tmp = recv(client_socket)
                if not tmp:
                    break
                print (tmp)
                
            
        else:
            print("ls does not take arguments")
    
    #TODO FINISHED NEEDS TESTING
    def do_quit(self, args):
        if len(args) == 0:
            msg = 'quit'
            send_data(msg)
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

client_socket.close()
print("Command Socket Closed")
