#! /usr/bin/python
import socket
from sys import argv

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10000  # The port used by the server

message = argv[1] if len(argv) > 1 else ""

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(message.encode())
