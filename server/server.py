#!/usr/bin/env python3
""""FTP Protocols Server"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
import socket
import sys
import commands

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
    file_size = int(file_size_buff)
    data = recvAll(sock, file_size)
    return data
def data_connection():
    tmp_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
    tmp_socket.bind(('',0))
    socket_number = str(tmp_socket.getsockname()[1])
    send_data(connection_socket,  socket_number)
    tmp_socket.listen(1)
    new_socket ,addr = tmp_socket.accept()
    return new_socket


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
print ('The server is ready to receive')
connection_socket ,addr = server_socket.accept()
print ('Connected by', addr)
data =''
while 1:
    try:
        exec_code = recv(connection_socket)
        if exec_code == "ls":
            tmp = ""
            data_socket = data_connection()
            for line in commands.getoutput('ls'):
                tmp += line
            send_data(data_socket, tmp)
            data_socket.close()
        if exec_code == "quit":
            break
        if exec_code == "get":
            data_socket = data_connection()
            file_name = recv(data_socket)
            while 1:
                try:
                    file = open(file_name, "r")
                except:
                    print("problem opening the file", file_name)
                try:
                    byte = file.read(1)
                    while byte != "":
                        send_data(data_socket, byte)
                        byte = file.read(1)
                finally:
                    data_socket.close()
                    file.close()

    except:
        pass
connection_socket.close()
print("Command Socket Closed")
