"""
TCP Server — Ping Pong (Exercise 0)

Author      : Pietro Boccadoro
Modified by : Gianpaolo Detomaso
Date        : 2024-04-11
Modified    : 2026-05-06
Version     : 1.1
"""

import socket   # standard library module for networking


HOST = "127.0.0.1"  # loopback address — accept connections from this machine only
PORT = 65432        # port to listen on


def createServerSocket():
    """
    Create and configure a TCP server socket.

    This function initializes a socket using:
    - AF_INET for IPv4 addressing
    - SOCK_STREAM for TCP communication (connection-oriented protocol)

    Additional configuration:
    - SO_REUSEADDR allows immediate reuse of the port after the program exits,
      avoiding "Address already in use" errors caused by the TIME_WAIT state.

    Returns:
        socket.socket: A configured TCP server socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock


def bindAndListen(sock):
    """
    Bind the server socket to a specific address and enable listening mode.

    This function performs two operations:
    1. Binding:
       - Associates the socket with (HOST, PORT), allowing the OS
         to route incoming connections to this socket.

    2. Listening:
       - Puts the socket into passive mode, enabling it to accept
         incoming connection requests.
       - The backlog (1) specifies the maximum number of pending
         connections in the queue.

    Args:
        sock (socket.socket): The TCP server socket.
    """
    sock.bind((HOST, PORT))
    sock.listen(1)


def acceptConnection(sock):
    """
    Accept an incoming client connection.

    This function blocks until a client completes the TCP
    three-way handshake (SYN, SYN-ACK, ACK).

    Returns:
        tuple:
            - conn (socket.socket): A new socket dedicated to the client.
            - addr (tuple): (IP, port) of the connected client.
    """
    conn, addr = sock.accept()
    print(f"[Server] Connection accepted from {addr}")
    return conn, addr


def receiveMessage(conn):
    """
    Receive and decode a message from the client.

    This function uses recv(), which:
    - blocks until data is available or the connection is closed
    - returns a bytes object

    Key behavior:
    - If recv() returns an empty bytes object (b""), it indicates
      that the client has closed the connection.

    Args:
        conn (socket.socket): The client connection socket.

    Returns:
        str or None:
            - Decoded message if data is received
            - None if the connection is closed
    """
    data = conn.recv(1024)

    if not data:
        print("[Server] Client closed the connection.")
        return None

    message = data.decode("utf-8").strip()
    print(f"[Server] Received: {message!r}")
    return message


def handleMessage(message):
    """
    Process a client message and generate a response.

    This function encapsulates the application logic,
    keeping it independent from networking operations.

    Current behavior:
    - "PING" → "PONG"
    - Any other input → "Unknown message"

    Args:
        message (str): The received client message.

    Returns:
        str: The response to send back to the client.
    """
    if message == "PING":
        return "PONG"
    else:
        return f"Unknown message: {message!r}"


def sendReply(conn, reply):
    """
    Send a response to the connected client.

    This function uses sendall(), which ensures that all bytes
    are transmitted, handling partial sends internally.

    Args:
        conn (socket.socket): The client connection socket.
        reply (str): The message to send.
    """
    conn.sendall(reply.encode("utf-8"))
    print(f"[Server] Sent:     {reply!r}")


def communicationLoop(conn):
    """
    Handle continuous communication with a connected client.

    This function implements the main interaction loop:
    1. Receive a message
    2. Process it
    3. Send a reply

    The loop continues until the client closes the connection.

    Args:
        conn (socket.socket): The client connection socket.
    """
    while True:
        message = receiveMessage(conn)

        if message is None:
            break

        reply = handleMessage(message)

        sendReply(conn, reply)


def closeSockets(conn, server_sock):
    """
    Close both the client connection socket and the server socket.

    - Closing the client socket terminates the TCP connection (FIN exchange).
    - Closing the server socket stops the server from accepting new connections.

    Args:
        conn (socket.socket): The client connection socket.
        server_sock (socket.socket): The server listening socket.
    """
    conn.close()
    server_sock.close()


def main():
    """
    Entry point of the TCP server application.

    Responsibilities:
    - Create and configure the server socket
    - Bind and start listening
    - Accept a client connection
    - Handle communication
    - Cleanly close sockets

    This function orchestrates the server lifecycle.
    """
    server_sock = createServerSocket()

    bindAndListen(server_sock)

    print(f"[Server] Listening on {HOST}:{PORT} ...")

    conn, addr = acceptConnection(server_sock)

    communicationLoop(conn)

    closeSockets(conn, server_sock)


if __name__ == "__main__":
    main()