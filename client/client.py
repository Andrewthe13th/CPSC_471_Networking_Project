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
import os

def send_data(sock, data):
    data_size = str(len(data))
    while len(data_size) < 10:
        data_size = "0" + data_size
    data = data_size + data
    data_sent = 0
    while data_sent != len(data):
        data_sent += sock.send(data[data_sent:])
    
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
    try:
        file_size = int(file_size_buff)
        data = recvAll(sock, file_size)
    except:
        pass
    return data
    
class ftp_command(Cmd):
    def do_get(self, args):
        if len(args) > 0:
            msg = 'get'
            filename = args
            send_data(client_socket, msg)
            tmp_port = int(recv(client_socket))
            try:
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((server_name,tmp_port))
                send_data(data_socket, filename)
                print("downloading file")
                if os.path.exists(filename):
                    i = 1
                    num = "(" + str(i) + ")"
                    f_name, f_extension = os.path.splitext(filename)
                    tmp = f_name
                    filename = tmp + num + f_extension
                    while os.path.exists(filename):
                        i += 1
                        num = "(" + str(i) + ")"
                        filename = tmp + num + f_extension
                
                file = open(filename, "w+")

                while 1:
                    tmp = recv(data_socket)
                    if not tmp:
                        break
                    file.write(tmp)
                file.close()
                #TODO CHECK FILE HASH
                print("File download is complete")
            except socket.error as socketerror:
                print("Error: ", socketerror)
            
        else:
            print("get needs the name of the file you are trying to download")
    def do_put(self, args):
       if len(args) > 0:
            msg = 'put'
            filename = args
            send_data(client_socket, msg)
            tmp_port = int(recv(client_socket))
            try:
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((server_name,tmp_port))
                send_data(data_socket, filename)
                print("connection complete")
                while 1:
                    try:
                        file = open(filename, "r")
                    except:
                        print("problem opening the file", filename)
                    try:
                        byte = file.read(1)
                        while byte != "":
                            send_data(data_socket, byte)
                            byte = file.read(1)
                    finally:
                        file.close()
                        break
            except socket.error as socketerror:
                print("Error: ", socketerror)

       
    def do_ls(self, args):
        if len(args) == 0:
            msg = 'ls'
            send_data(client_socket, msg)
            tmp_port = int(recv(client_socket))
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.connect((server_name,tmp_port))
            tmp = ""
            while 1:
                tmp = recv(data_socket)
                if not tmp:
                    break
                print (tmp)
        else:
            print("ls does not take arguments")
    
    def do_quit(self, args):
        if len(args) == 0:
            msg = 'quit'
            send_data(client_socket, msg)
            print(recv(client_socket))
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
    print("FTP error: ", socketerror)

client_socket.close()
print("Command Socket Closed")
