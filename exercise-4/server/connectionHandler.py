"""
connectionHandler — TCP Chat Server (Exercise 4)

Author      : Gianpaolo Detomaso
Date        : 2026-05-06
Version     : 1.0
"""


import json
import chat
import socketManager

def handleMessage(client, message: str) -> None:
    """Parse and dispatch a single JSON message received from a client."""
    messageJSON = json.loads(message)
    messageType = messageJSON.get("type")

    if messageType == "name":
        # First message from a client: set the username and send history.
        if client and client.name is None:
            client.setName(messageJSON["name"])
            client.sendJSON({
                "type": "lastMessages",
                "lastMessages": chat.getLastMessages(),
            })

    elif messageType == "message":
        # Regular chat message.
        if client and client.name:
            newMessage = {
                "author": client.name,
                "content": messageJSON["message"],
            }
            socketManager.broadcastMessage({"type": "newMessage", "message": newMessage})
            chat.addMessage(newMessage)

    else:
        print(f"Unrecognized message type: {messageType}")


def handler(client) -> None:
    """
    Handle communication for a single connected client.

    Receives messages in a loop and delegates parsing to `handleMessage`.
    """
    while True:
        try:
            message = client.socket.recv(1024).decode()
            if not message:
                break

            handleMessage(client, message)

        except Exception as e:
            print(f"Error with client {client.address}: {e}")
            break

    print(f"Client {client.address} disconnected")
    client.close()

