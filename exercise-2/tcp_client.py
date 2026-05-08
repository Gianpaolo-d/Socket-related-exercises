"""
TCP Client — Ping Pong with multiple connections handler (Exercise 2)

Author      : Pietro Boccadoro
Modified by : Gianpaolo Detomaso
Date        : 2024-04-11
Modified    : 2026-05-06
Version     : 1.2
"""

import socket   # standard library module for networking
import time     # used to introduce delays between messages


HOST = "127.0.0.1"  # server address
PORT = 65432        # server port (must match the server configuration)


def createSocket():
    """
    Create a TCP client socket.

    This function initializes a socket using:
    - AF_INET for IPv4 addressing
    - SOCK_STREAM for TCP communication

    TCP is a connection-oriented protocol that guarantees:
    - reliable delivery
    - ordered data transmission
    - no duplication

    Returns:
        socket.socket: A TCP socket ready to connect.
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connectToServer(sock):
    """
    Establish a connection to the server.

    This function initiates the TCP three-way handshake:
    1. Client sends SYN
    2. Server responds with SYN-ACK
    3. Client sends ACK

    The call blocks until the connection is successfully established
    or an exception is raised.

    Args:
        sock (socket.socket): The TCP client socket.
    """
    sock.connect((HOST, PORT))
    print(f"[Client] Connected to {HOST}:{PORT}")


def sendMessage(sock, message, attempt):
    """
    Send a message to the server over TCP.

    The message is encoded into bytes before transmission.
    sendall() ensures that all bytes are sent, even if the OS
    buffers the data in multiple chunks.

    Logging:
    - Prints the message being sent with the attempt number.
    - Uses !r formatting to show the exact representation.

    Args:
        sock (socket.socket): The connected TCP socket.
        message (str): The message to send.
        attempt (int): The current iteration number.
    """
    print(f"\n[Client] Send #{attempt}: {message!r}")
    sock.sendall(message.encode("utf-8"))


def receiveReply(sock):
    """
    Receive and decode a reply from the server.

    This function uses recv(), which:
    - blocks until data is available
    - reads up to 1024 bytes from the socket

    The received bytes are decoded using UTF-8.

    Args:
        sock (socket.socket): The connected TCP socket.

    Returns:
        str: The decoded server reply.
    """
    data = sock.recv(1024)
    reply = data.decode("utf-8")
    print(f"[Client] Reply:    {reply!r}")
    return reply


def pingLoop(sock):
    """
    Execute the main ping loop.

    This function sends a sequence of PING messages to the server
    and waits for a reply after each message.

    Behavior:
    - Sends 5 PING messages
    - Receives a reply after each send
    - Introduces a short delay between iterations

    This structure clearly separates:
    - sending logic (sendMessage)
    - receiving logic (receiveReply)

    Args:
        sock (socket.socket): The connected TCP socket.
    """
    for i in range(1, 6):
        message = "PING"

        sendMessage(sock, message, i)
        receiveReply(sock)

        time.sleep(0.5)


def closeSocket(sock):
    """
    Close the TCP connection and release system resources.

    Closing a TCP socket:
    - sends a FIN packet to the server
    - initiates connection teardown
    - releases the associated file descriptor

    Args:
        sock (socket.socket): The TCP socket to close.
    """
    print("\n[Client] All pings sent. Closing connection.")
    sock.close()


def main():
    """
    Entry point of the TCP client application.

    Responsibilities:
    - Create the socket
    - Connect to the server
    - Execute the ping loop
    - Close the connection

    This function orchestrates the client lifecycle.
    """
    sock = createSocket()

    connectToServer(sock)

    pingLoop(sock)

    closeSocket(sock)


if __name__ == "__main__":
    main()