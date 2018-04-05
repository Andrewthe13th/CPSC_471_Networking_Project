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

# ---------- FUNCTIONS --------------
def send_data(sock, data):
    """
    Funtion formats the header to the message
    and sends the data.

    Args:
        param1: Name of the socket to use.
        param2: The information to be sent.

    Returns:
        TNothing.

    Raises:
        KeyError: None.
    """
    data_size = str(len(data))
    #set header to 10 bytes
    while len(data_size) < 10:
        data_size = "0" + data_size
    
    data = data_size + data
    data_sent = 0

    #ensure all data is sent
    while data_sent != len(data):
        data_sent += sock.send(data[data_sent:])
    
def recvAll(sock, numBytes):
    """
    Function receives the data from a socket.

    Args:
        param1: Name of the socket to use.
        param2: The length of data to be received.

    Returns:
        The data received.

    Raises:
        KeyError: None.
    """
    recvBuff = ""
    tmpBuff = ""
    # ensure all data has been recieved
    while len(recvBuff) < numBytes:
        tmpBuff =  sock.recv(numBytes)
        # The other side has closed the socket
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff
    
def recv(sock):
    """
    Fuction receives receives header information before
    calling recvAll() to handle the data of the message. Passes
    any header information needed to receive the message to recvAll()

    Args:
        param1: Name of the socket to use.

    Returns:
        The full message received.

    Raises:
        KeyError: None.
    """
    data = ""
    file_size = 0	
    file_size_buff = ""
    # header size buffer
    file_size_buff = recvAll(sock, 10)
    try:
        file_size = int(file_size_buff)
        # recieve a file given a file size
        data = recvAll(sock, file_size)
    except:
        pass
    return data
    
class ftp_command(Cmd):
    """
    Class that sets up the FTP>> line and handles
    the commands for all functions for the FTP program

    Args:
        param1: Command line instructions
    """
    
    def do_get(self, args):
        """
        Function tells the server to send a file.
        File name is given on the command line

        Args:
            param1: The name of the file

        Returns:
            Nothing.

        Raises:
            KeyError: Throws an error if there is a problem connecting
                        to the new data socket.
                        Throws an error if function is called with no
                        file name given.
        """
        if len(args) > 0:
            msg = 'get'
            filename = args
            # send get to server
            send_data(client_socket, msg)
            tmp_port = int(recv(client_socket))
            try:
                # uses tcp to transfer data
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((server_name,tmp_port))
                send_data(data_socket, filename)
                print("downloading file")
                # if valid file
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
                # open file to read and send
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
        """
        Function tells the server to receive a file.
        File name is given on the command line

        Args:
            param1: The name of the file

        Returns:
            Nothing.

        Raises:
            KeyError: Throws an error if there is a problem connecting
                        to the new data socket.
                        Throws an error if there is a problem opening
                        the file
        """
        
        if len(args) > 0:
            msg = 'put'
            filename = args
            # send put to server
            send_data(client_socket, msg)
            tmp_port = int(recv(client_socket))
            try:
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((server_name,tmp_port))
                send_data(data_socket, filename)
                print("Uploading file")
                while 1:
                    try:
                        file = open(filename, "r")
                    except:
                        print("problem opening the file", filename)
                    try:
                        #send at one byte at a tome
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
        """
        Function tells the server to run the command "ls" and 
        return its results. Prints the "ls" results from server. Will
        not accept any commands after ls.

        Args:
            param1: None

        Returns:
            Nothing.

        Raises:
            KeyError: Throws an error for any arguments given after ls
        """
        if len(args) == 0:
            msg = 'ls'
            # send ls command to server
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
        """
        Function tells the server to quit the command connection

        Args:
            param1: None

        Returns:
            boolean value True

        Raises:
            KeyError: Throws an error for any argumenets given after quit
        """
        if len(args) == 0:
            msg = 'quit'
            # tell server to kill connection
            send_data(client_socket, msg)
            print(recv(client_socket))
            return True
        else:
            print("quit takes no arguments")


#----------- MAIN CODE -----------------

#setup arguements
parser = argparse.ArgumentParser(description="FTP client side")
parser.add_argument("server_name", help='Web address of server')
parser.add_argument("port",  help="server port you wish to connecct to")
args = parser.parse_args()

# set up server name and port
server_name = args.server_name
server_port= args.port

# check for valid port
if server_port.isdigit():
    server_port = int(server_port)
else:
    print("The port {} is in the wrong format".format(server_port))
    sys.exit()

try:
    #set up socket
    print("Creating socket")
    client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    print("Connecting to server")
    client_socket.connect((server_name,server_port))

    print("Setting up FTP commands")
    prompt = ftp_command()
    prompt.prompt = 'ftp> '
     # enable client input commands
    prompt.cmdloop('FTP connection established')
except socket.error as socketerror:
    print("FTP error: ", socketerror)

client_socket.close()
print("Command Socket Closed")
