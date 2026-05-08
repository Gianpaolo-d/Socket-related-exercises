# Socket related exercises: Exercise 0 (Refactoring and modularization)

The original TCP and UDP Ping-Pong programs were progressively improved across several exercises. The main goal was not to change the core behaviour, but to make the code more structured, easier to read, and closer to how real networking software is organized.

## What changed in Exercise 0

### Refactoring and modularization
Initially, most logic was written directly inside `main()`, which made the execution flow harder to follow.

The refactoring preserved the same behaviour but reorganized the code into dedicated functions, so `main()` becomes a high-level orchestrator:

- `sock = createSocket()`
- `connectToServer(sock)`
- `pingLoop(sock)`
- `closeSocket(sock)`

For example, instead of writing inline send/receive like:

```python
client_sock.sendall(message.encode("utf-8"))
data = client_sock.recv(1024)
reply = data.decode("utf-8")
```

the code is split into responsibilities:

- `sendMessage(sock, message, i)`
- `receiveReply(sock)`

This does not introduce new behaviour. It only centralizes responsibilities (encoding, buffer sizes, logging) so future changes are simpler.

### Server-side separation of concerns
On the server, application decisions were separated from socket handling. The networking layer transports data, while the message interpretation is encapsulated in a function like:

- `reply = handleMessage(message)`

Finally, in the UDP server, the receive/process/reply flow is kept explicit in the main loop via:

1. receive
2. handle
3. reply

This makes the loop easier to read because each step corresponds to a single responsibility.