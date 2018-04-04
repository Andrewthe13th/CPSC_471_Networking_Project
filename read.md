# Simplified FTP server and FTP client

Simplified FTP server and FTP client. The client shall
connect to the server and support uploading and downloading of files to/from server.

## Getting Started

Place the server and client folder on the ecs.fullerton.edu titan server.


## Start the server

Start the server.py file from the command line with the port you want to listen on

```
python server.py 1234
```

### Start the client

Start the client.py file from the command line with ecs.fullerton.edu server and the port to connect to

```
python client.py ecs.fullerton.edu 1234
```

### Run the client commands

On the client side, run the commands.

```
ftp>ls

ftp>get <filename>

ftp>put <filename>

ftp>quit
```


## Authors

* **Andrew De La Fuente**
* **Paul Smith**
