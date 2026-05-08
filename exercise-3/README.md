# Socket related exercises: Exercise 3 (Unreliable channel simulation)

The final modification introduces a simulation of packet loss in UDP communication.

## What changed in Exercise 3

### Drop probability
A probability constant defines how often server replies should be dropped:

```python
DROP_PROBABILITY = 0.3
```

### Server-side simulation
Before sending a response, the server randomly decides whether to send or drop it:

```python
if random.random() < DROP_PROBABILITY:
    print("[Server] Dropped reply (simulated loss)")
    return
```

If the condition is met, the reply is not sent at all.

### Client-side timeout handling
On the client side, this behaviour is visible through the socket timeout. Because some replies are no longer guaranteed, the client must tolerate missing messages:

```python
sock.settimeout(2.0)
```

When a timeout occurs, the client continues gracefully instead of crashing:

```python
except socket.timeout:
    print("Timeout — no reply received")
```

This models how real-world UDP applications need to be designed to handle packet loss.


