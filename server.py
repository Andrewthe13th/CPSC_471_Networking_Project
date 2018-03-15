#!/usr/bin/env python3
""""FTP Protocols Server"""
__author__ = "Andrew De La Fuente and Paul Smith"
__copyright__ = "Copyright (C) 2018 Andrew De La Fuente and Paul Smith"
__license__ = "Public Domain"
__version__ = "1.0"

import argparse
import socket
import sys
import subprocess

#TODO: WILL REPLACE CLIENT_SOCKET.SEND TO OUR OWN FORMAT
def send_data(self):
    pass


#TODO: Will REPLACE CLIENT_SOCKET.RCV TO OUR OWN FORMAT
def rec_data(self):
    pass

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
        exec_code = connection_socket.recv(1024)
        exec_code = exec_code.decode() 
        if exec_code == "ls":
            proc = subprocess.Popen(exec_code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout_value = proc.stdout.read() + proc.stderr.read()
            send_data(stdout_value)
        if exec_code == "quit":
            break
        #if exec_code == "get":
         #   tmp_socket = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
          #  tmp_socket.bind(('',0))
           # print(tmp_socket.getsockname())
            #connection_socket.send(tmp_socket.getsockname())
            #while 1:
             #   try:
              #      tmp_cmd = tmp_socket.recv(1024)
               #     if tmp_cmd == 'close':
                #        tmp_socket.close()
                 #       print("Download Socket Closed")
                #except:
                 #   pass
    except:
        pass
#    print("waiting")
#
#    tmpBuff= ''
#
#    while len(data) != 40:
#        tmpBuff = connection_socket.recv(40)
#        if not tmpBuff :
#            break
#        data += tmpBuff
#print (data)
connection_socket.close()
print("Command Socket Closed")
