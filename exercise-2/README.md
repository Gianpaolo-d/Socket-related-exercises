# Socket related exercises: Exercise 2 (Multi-client TCP server)

The third step extends the TCP server so that it can handle more than one client.

## What changed in Exercise 2

### Continuous accept loop
In the original version, the server accepted a single connection and then stopped (or stayed busy serving only that client). 

The updated version wraps `accept()` in a loop, allowing the server to keep waiting for new clients:

```python
while connections_handled < MAX_CONNECTIONS:
    conn, addr = server_sock.accept()
```

### Concurrency with threads
To avoid blocking the main server loop, a new thread is created for each client connection:

```python
threading.Thread(target=communicationLoop, args=(conn, addr)).start()
```

This allows multiple clients to be handled without one client preventing others from being served. Each client is still processed sequentially within its own thread.

### Limiting the number of connections
A counter is introduced to stop the server gracefully after a defined number of clients:

```python
MAX_CONNECTIONS = 5
connections_handled += 1
```

So the server does not run indefinitely.


