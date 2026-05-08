"""
socketManager — TCP Chat Server (Exercise 4)

Author      : Gianpaolo Detomaso
Date        : 2026-05-06
Version     : 1.0
"""


import json
import threading
import socket

import connectionHandler
import config

# Array of currently connected clients.
connections = []


class ClientConnection:
    """Represents a single TCP client connection."""

    def __init__(self, client_socket: socket.socket, address):
        self.socket = client_socket
        self.address = address
        self.name = None

    def setName(self, name: str) -> None:
        """Assign the username to this connection."""
        print(f"Client {self.address} set name to {name}")
        self.name = name

    def sendJSON(self, message: dict) -> None:
        """Send a JSON message to the client."""
        try:
            self.socket.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Error sending message to {self.address}: {e}")
            self.close()

    def close(self) -> None:
        """Close the socket and remove the client from the registry."""
        try:
            self.socket.close()
        finally:
            if self in connections:
                connections.remove(self)


def broadcastMessage(message: dict) -> None:
    """Send a JSON message to all connected clients."""
    for client in list(connections):
        try:
            client.sendJSON(message)
        except Exception as e:
            print(f"Error sending message to {client.address}: {e}")
            client.close()


def startServer(host: str = config.HOST, port: int = config.PORT) -> None:
    """Start the TCP server and accept clients forever."""
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen()
    print(f"Server started on {host}:{port}")

    while True:
        clientSocket, addr = serverSocket.accept()
        print(f"Client connected from {addr}")

        client = ClientConnection(clientSocket, addr)
        connections.append(client)

        threading.Thread(target=connectionHandler.handler, args=(client,), daemon=True).start()

