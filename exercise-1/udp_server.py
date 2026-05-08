"""
UDP Server — Ping Pong with count (Exercise 1)

Author      : Pietro Boccadoro
Modified by : Gianpaolo Detomaso
Date        : 2024-04-11
Modified    : 2026-05-06
Version     : 1.2
"""

import socket   # standard library module for networking

HOST = "127.0.0.1"  # loopback address — accept datagrams from this machine only
PORT = 65433        # port to listen on (different from the TCP example to avoid conflicts)

counter = 0  # global counter to track the number of pings received

def increaseCounter():
    """
    Increment the global counter by one.

    This function modifies the global variable 'counter' to keep track
    of how many "PING" messages have been received by the server.

    The use of a global variable allows the count to persist across
    multiple calls to this function, effectively maintaining state
    across different client interactions.

    Returns:
        int: The updated value of the counter after incrementing.
    """
    global counter
    lastvalue = counter 
    counter += 1
    print(f"[Server] Counter increased {lastvalue} -> {counter}")
    return counter

def createAndBindSocket():
    """
    Create and configure a UDP socket bound to the specified HOST and PORT.

    This function performs two key operations:
    1. Socket creation:
       - Uses AF_INET to specify IPv4 addressing.
       - Uses SOCK_DGRAM to indicate UDP (User Datagram Protocol),
         which is connectionless and does not guarantee delivery,
         ordering, or duplication protection.

    2. Socket binding:
       - Associates the socket with a local address (HOST, PORT),
         allowing the operating system to route incoming UDP datagrams
         destined for this endpoint to the socket.
       - Unlike TCP, UDP does not require listen() or accept(),
         as there is no concept of connection establishment.

    Returns:
        socket.socket: A bound UDP socket ready to receive datagrams.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    return sock

def receiveMessage(sock):
    """
    Receive and decode a UDP datagram from a client.

    This function blocks execution until a datagram is received.
    It uses recvfrom(), which differs from TCP's recv() by returning:
      - the raw data (bytes)
      - the sender's address (IP, port)

    Key behaviors:
    - A maximum of 1024 bytes is read from the incoming datagram.
      Any excess data beyond this limit is truncated.
    - The received bytes are decoded using UTF-8 encoding and
      stripped of leading/trailing whitespace.

    Logging:
    - Prints the received message and the sender's address.
    - Uses !r (repr) formatting to make invisible characters
      (e.g., newline, spaces) explicit for debugging.

    Args:
        sock (socket.socket): The UDP socket used for receiving data.

    Returns:
        tuple:
            - message (str): The decoded message string.
            - client_addr (tuple): (IP, port) of the sender.
    """
    data, client_addr = sock.recvfrom(1024)
    message = data.decode("utf-8").strip()
    print(f"[Server] Received {message!r} from {client_addr}")
    return message, client_addr
    
def handleMessage(message):
    """
    Process a client message and generate an appropriate response.

    This function encapsulates the application-level logic of the server,
    keeping it independent from networking concerns.

    Current behavior:
    - If the message is "PING", responds with "PONG".
    - For any other input, returns a formatted "Unknown" response.

    This design allows easy extension (e.g., adding new commands)
    without modifying the networking layer.

    Args:
        message (str): The decoded client message.

    Returns:
        str: The response to be sent back to the client.
    """
    if message == "PING":
        return "PONG #" + str(increaseCounter())
    else:
        return f"Unknown: {message!r}"
    
def sendReply(sock, reply, client_addr):
    """
    Send a UDP response to a specific client.

    This function uses sendto(), which is required for UDP communication.
    Unlike TCP, UDP sockets are connectionless, meaning:
    - There is no persistent connection state.
    - The destination address must be specified for every message sent.

    The response string is encoded into bytes using UTF-8 before transmission.

    Logging:
    - Prints the outgoing message and the destination address.
    - Uses !r formatting to ensure accurate representation.

    Args:
        sock (socket.socket): The UDP socket used for sending data.
        reply (str): The message to send.
        client_addr (tuple): The destination address (IP, port).
    """
    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Sent {reply!r} back to {client_addr}\n")
    
def listenLoop(sock):
    """
    Continuously listen for incoming UDP datagrams and process them.

    This function implements the main server loop:
    1. Wait for a message from a client.
    2. Process the message using application logic.
    3. Send a response back to the originating client.

    The loop runs indefinitely until externally interrupted
    (e.g., via Ctrl+C).

    This structure clearly separates:
    - input handling (receiveMessage)
    - business logic (handleMessage)
    - output handling (sendReply)

    Args:
        sock (socket.socket): The bound UDP socket.
    """
    while True:
        message, client_addr = receiveMessage(sock)
        reply = handleMessage(message)
        sendReply(sock, reply, client_addr)

def main():
    """
    Entry point of the UDP server application.

    Responsibilities:
    - Initialize and bind the UDP socket.
    - Display server startup information.
    - Start the main listening loop.

    This function orchestrates the overall server lifecycle,
    delegating specific tasks to dedicated helper functions.
    """
    sock = createAndBindSocket()

    print(f"[Server] Listening for UDP datagrams on {HOST}:{PORT} ...")
    print("[Server] Press Ctrl+C to stop.\n")

    listenLoop(sock)

# Run main() only when the file is executed directly
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Catch Ctrl+C so the server exits cleanly without a traceback
        print("\n[Server] Stopped.")