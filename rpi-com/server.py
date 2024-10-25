#! /usr/bin/python
from __future__ import annotations

import socket
from dataclasses import dataclass
from enum import Enum, auto
from time import time_ns
from typing import Optional

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3000  # Port to listen on (non-privileged ports are > 1023)
DEFAULT_TIMEOUT = 10000
DEBUG = True


# Define connection event
@dataclass
class Event:
    address: str
    eventType: EventType


class EventType(Enum):
    CONNECT = auto()
    REPLY = auto()
    DISCONNECT = auto()

    @classmethod
    def contains(cls, item):
        try:
            cls[item]
        except KeyError:
            return False
        return True


def parse_data(data: str, addr: str) -> Optional[Event]:
    if not EventType.contains(data):
        return None
    return Event(addr, EventType[data])


# Handle relation
connections: dict[str, int] = {}


def handle_event(event: Event) -> None:
    match event.eventType:
        case EventType.CONNECT:
            if event.address in connections:
                return
            print(f"CONNECTION - {event.address}")
            connections[event.address] = DEFAULT_TIMEOUT
        case EventType.REPLY:
            if event.address not in connections:
                return
            print(f"REPLY - {event.address}")
            connections[event.address] = DEFAULT_TIMEOUT
        case EventType.DISCONNECT:
            if event.address not in connections:
                return
            print(f"DISCONNECTION - {event.address}")
            connections.pop(event.address)


# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    last_t = time_ns() / 1e6

    while True:
        # Accept connections
        conn, (addr, _) = s.accept()

        # Parse event
        event = parse_data(conn.recv(1024).decode(), addr)

        # Handle event
        if event:
            handle_event(event)

        # Debug info
        if DEBUG:
            print("\n=========CONNECTIONS===========")
            for address, timeout in connections.items():
                print(f"\t{address} - ({timeout}s)")
            print("===============================\n")

        conn.close()
