#! /usr/bin/python
from __future__ import annotations

from multiprocessing import Process
from socket import AF_INET, SOCK_STREAM, error, socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3000  # Port to listen on (non-privileged ports are > 1023)
DEBUG = True


class Connection:
    process: Process
    port: int
    addr: str

    def __init__(self, addr: str, conn: socket) -> None:
        def connection_process(conn: socket, tunnel: socket) -> None:
            tunnel.listen()
            local_conn, _ = tunnel.accept()
            while True:
                # Receive local message
                buffer = bytes()
                while True:
                    data = local_conn.recv(1024)
                    buffer += data
                    if len(data) == 0:
                        break

                # Repeat message to client
                conn.sendall(buffer)

                # Receive response from client
                buffer = bytes()
                while True:
                    data = conn.recv(1024)
                    buffer += data
                    if len(data) == 0:
                        break

                # Repeat response to local conn
                local_conn.sendall(buffer)

        # Create tunnel socket
        s = socket(AF_INET, SOCK_STREAM)
        port = 10000
        while True:
            try:
                s.bind(("localhost", port))
                break
            except error:
                port += 1

        # Run child process
        p = Process(target=connection_process, args=(conn, s))
        p.start()

        # Create connection
        self.addr = addr
        self.port = port
        self.process = p


# Handle connections
connections: set[Connection] = set()


# Initialize socket
with socket(AF_INET, SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        # Accept connections
        conn, (addr, _) = s.accept()

        # Create new Connection
        c = Connection(addr, conn)
        connections.add(c)

        if DEBUG:
            print(f"New connection created on port {c.port}")
