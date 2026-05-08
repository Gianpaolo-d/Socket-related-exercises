"""
chat — TCP Chat Server (Exercise 4)

Author      : Gianpaolo Detomaso
Date        : 2026-05-06
Version     : 1.0
"""


messages = []

def addMessage(message: dict) -> None:
    """Add a new message to the in-memory message history."""
    print(f"New message from {message['author']}: {message['content']}")
    messages.append(message)


def getLastMessages(max_messages: int = 50) -> list:
    """Return the last `max_messages` messages from memory."""
    return messages[-max_messages:]

