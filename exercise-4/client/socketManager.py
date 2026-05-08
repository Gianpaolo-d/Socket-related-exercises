"""
socketManager — TCP Chat Client (Exercise 4)

Author      : Gianpaolo Detomaso
Date        : 2026-05-06
Version     : 1.0
"""


import json
import socket as Socket
import threading

import cliManager
import config

# Connection state shared with the CLI module
running = False

# Server socket instance
socket = None

# Username of this client
username = ""


def messageReceiver():
    """
    Continuously receive JSON messages from the server.

    Expected server message types:
    - "lastMessages": payload contains a list of messages to display.
    - "newMessage": payload contains a single new message to display.

    The receive loop stops when `running` is set to False or when the
    connection is closed.
    """
    global running, socket

    while running:
        try:
            message = socket.recv(1024).decode()
            if not message:
                break

            messageJSON = json.loads(message)

            if messageJSON.get("type") == "lastMessages":
                for msg in messageJSON.get("lastMessages", []):
                    cliManager.print(f"{msg['author']}: {msg['content']}")

            elif messageJSON.get("type") == "newMessage":
                msg = messageJSON.get("message", {})
                cliManager.print(f"{msg.get('author')}: {msg.get('content')}")

        except Exception as e:
            cliManager.print(f"Error: {e}")
            break

    try:
        socket.close()
    except Exception:
        pass


def sendMessage(message: str) -> None:
    """
    Send a chat message to the server.

    The protocol wraps the raw string inside a JSON object with:
    - type: "message"
    - message: <string>
    """
    payload = {
        "type": "message",
        "message": message,
    }
    socket.send(json.dumps(payload).encode())


def startClient(host: str = config.HOST, port: int = config.PORT) -> None:
    """
    Start the TCP chat client.

    Steps:
    1. Connect to the server.
    2. Ask the user for a name and send it as JSON {type:"name"}.
    3. Start a background receiver thread to print incoming messages.
    4. Start the interactive input loop.
    """
    global running, socket, username

    socket = Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM)
    socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    running = True

    username = input("Enter your name: ")
    handshake = {"type": "name", "name": username}
    socket.send(json.dumps(handshake).encode())

    threading.Thread(target=messageReceiver, daemon=True).start()

    cliManager.readInput()

    print("\nDisconnecting...")
    try:
        socket.close()
    finally:
        running = False


startClient("localhost", 16767)

