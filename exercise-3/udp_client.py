"""
UDP Client — Ping Pong with count unreliable channel simulation (Exercise 3)

Author      : Pietro Boccadoro
Modified by : Gianpaolo Detomaso
Date        : 2024-04-11
Modified    : 2026-05-06
Version     : 1.3
"""

import socket   # standard library module for networking
import time     # used to introduce delays between pings


HOST = "127.0.0.1"  # address of the server
PORT = 65433        # server port (must match the server configuration)


def createSocket():
    """
    Create and configure a UDP client socket.

    This function initializes a socket using:
    - AF_INET for IPv4 addressing
    - SOCK_DGRAM for UDP communication (connectionless protocol)

    Additionally, a timeout is configured to prevent blocking indefinitely
    when waiting for a server response.

    Key behaviors:
    - UDP does not establish a connection (no connect()).
    - A timeout ensures recvfrom() raises an exception instead of hanging.

    Returns:
        socket.socket: A configured UDP socket ready for communication.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    return sock


def sendMessage(sock, message, server_addr, attempt):
    """
    Send a UDP datagram to the server.

    This function encodes the message into bytes and transmits it
    using sendto(), which requires the destination address for each call.

    Logging:
    - Prints the message being sent along with the attempt number.
    - Uses !r formatting to show the exact representation of the message.

    Args:
        sock (socket.socket): The UDP socket used for sending data.
        message (str): The message to send.
        server_addr (tuple): The destination address (IP, port).
        attempt (int): The current ping iteration number.
    """
    print(f"[Client] Send #{attempt}: {message!r}")
    sock.sendto(message.encode("utf-8"), server_addr)


def receiveMessage(sock, ping_number):
    """
    Receive and decode a UDP reply from the server.

    This function waits for a datagram using recvfrom(), which:
    - blocks until data arrives or the timeout expires
    - returns both the data and the sender's address

    Key behaviors:
    - The received bytes are decoded using UTF-8.
    - If no reply is received within the timeout, a socket.timeout
      exception is raised and handled gracefully.

    Logging:
    - Prints the received reply and sender address.
    - Prints a timeout message if no response is received.

    Args:
        sock (socket.socket): The UDP socket used for receiving data.
        ping_number (int): The current ping iteration number.
    """
    try:
        data, server_addr = sock.recvfrom(1024)
        reply = data.decode("utf-8")

        print(f"[Client] Reply from {server_addr}: {reply!r}")

    except socket.timeout:
        print(f"[Client] Timeout — no reply received for ping #{ping_number}")


def pingLoop(sock):
    """
    Execute the main ping loop.

    This function sends a sequence of PING messages to the server
    and waits for corresponding replies.

    Behavior:
    - Sends 5 PING messages
    - Waits for a reply after each send
    - Handles potential packet loss using timeout logic
    - Introduces a short delay between iterations for readability

    This structure clearly separates:
    - sending logic (sendMessage)
    - receiving logic (receiveMessage)

    Args:
        sock (socket.socket): The configured UDP socket.
    """
    server_addr = (HOST, PORT)

    print(f"[Client] UDP socket ready. Will send to {HOST}:{PORT}\n")

    for i in range(1, 6):
        message = "PING"

        sendMessage(sock, message, server_addr, i)
        receiveMessage(sock, i)

        time.sleep(0.5)


def closeSocket(sock):
    """
    Close the UDP socket and release system resources.

    Unlike TCP, UDP does not perform a connection teardown
    (no FIN/ACK exchange). Closing the socket simply releases
    the associated file descriptor on the local system.

    Args:
        sock (socket.socket): The UDP socket to close.
    """
    print("\n[Client] Done. Closing socket.")
    sock.close()


def main():
    """
    Entry point of the UDP client application.

    Responsibilities:
    - Create and configure the UDP socket
    - Execute the ping loop
    - Close the socket cleanly

    This function orchestrates the client lifecycle,
    delegating tasks to dedicated helper functions.
    """
    sock = createSocket()

    pingLoop(sock)

    closeSocket(sock)


# Run main() only when the file is executed directly
if __name__ == "__main__":
    main()