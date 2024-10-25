#! /usr/bin/python
from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3000  # The port used by the server
DEBUG = True

# Initialize socket
with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        # Receive message
        buffer = bytes()
        while True:
            data = s.recv(1024)
            print(len(data))
            buffer += data
            if not data:
                break
        print("received")

        if DEBUG:
            print(buffer.decode())

        # Forward to web-server
        # TODO
        response = "mock"

        # Send response
        s.sendall(response.encode())
