# Socket related exercises - Exercise 4 (TCP Chat)

A minimal TCP-based chat application implemented in Python.

- **Server** accepts multiple TCP clients, receives messages, and **broadcasts** new messages to all connected clients.
- **Client** connects to the server, sends the user name once, then allows the user to type messages from the terminal.

> Note: The current codebase uses simple `recv(1024)` reads and assumes that each JSON message arrives as a whole.

---

## Table of Contents

- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Message Protocol](#message-protocol)
- [How to Run](#how-to-run)
- [Client Commands](#client-commands)
- [Limitations & Notes](#limitations--notes)

---

## Project Structure

```
exercise-4/
├─ client/
│  ├─ main.py
│  ├─ socketManager.py
│  ├─ cliManager.py
│  └─ config.py
├─ server/
│  ├─ main.py
│  ├─ socketManager.py
│  ├─ connectionHandler.py
│  ├─ chat.py
│  └─ config.py
└─ README.md
```

- `client/main.py`: Entry point for the client.
- `client/socketManager.py`: TCP connection + send/receive loop.
- `client/cliManager.py`: Terminal UI (reads user input char-by-char, supports `exit`).
- `client/config.py`: Client-side host/port configuration.

- `server/main.py`: Entry point for the server.
- `server/socketManager.py`: TCP server socket, connection registry, broadcast logic.
- `server/connectionHandler.py`: Per-client receive loop and message dispatch.
- `server/chat.py`: In-memory message storage (for `lastMessages`).
- `server/config.py`: Server-side host/port configuration.

---

## How It Works

### 1) Handshake (client name)
When a client connects:
1. The client asks the user for a name.
2. The client sends a JSON message with `type: "name"` and the provided `name`.
3. The server stores the name in the associated client connection.
4. The server immediately responds with the most recent messages using `type: "lastMessages"`.

### 2) Chat messages
For each user message:
1. The client sends a JSON message with `type: "message"`.
2. The server wraps it with `{ author: <client name>, content: <message> }`.
3. The server broadcasts it to all connected clients with `type: "newMessage"`.
4. The server stores the message in memory so new clients can request history.

---

## Message Protocol

All client/server messages are JSON.

### Client → Server: set name
```json
{
  "type": "name",
  "name": "Alice"
}
```

### Client → Server: send chat message
```json
{
  "type": "message",
  "message": "Hello everyone"
}
```

### Server → Client: deliver last messages
```json
{
  "type": "lastMessages",
  "lastMessages": [
    { "author": "Bob", "content": "..." },
    { "author": "Carol", "content": "..." }
  ]
}
```

### Server → Client: broadcast new message
```json
{
  "type": "newMessage",
  "message": {
    "author": "Alice",
    "content": "Hello everyone"
  }
}
```

---

## How to Run

### Prerequisites
- Python 3.x

### Start the server (Terminal 1)
From the project root (`exercise-4/`):

```bash
python3 server/main.py
```

The server binds to `127.0.0.1:16767` (see `server/config.py`).

### Start the client (Terminal 2)
From the project root (`exercise-4/`):

```bash
python3 client/main.py
```

Then:
1. Enter your name.
2. Type messages and press Enter.

---

## Client Commands

- Type `exit` (and press Enter) to disconnect and terminate the client.

---

## Limitations & Notes

- **No message framing**: TCP is a byte stream; this code uses `recv(1024)` without explicit framing (e.g., newline delimiter or length prefix). This is acceptable for a small exercise but not robust for production.
- **In-memory history only**: chat history is stored in memory (`server/chat.py`) and resets when the server restarts.

