# Socket related exercises: Exercise 1 (Message counter)

In the second step, a new feature was introduced in the UDP server: a counter that tracks how many PING messages have been received.

## What changed in Exercise 1

### Persistent server state (runtime counter)
A persistent state is introduced on the server side using a global variable:

```python
counter = 0
```

Every time a valid message is received, the counter is incremented by a dedicated function:

```python
def increaseCounter():
    global counter
    counter += 1
    return counter
```

### Updated message handling
Previously, the server returned a static response:

- `return "PONG"`

After the change, the counter value is embedded in the response:

- `return "PONG #" + str(increaseCounter())`

This means each valid `PING` increases internal state, and the client receives progressively increasing numbers.

### Important behaviour note
This state exists only while the server is running. If the server restarts, the counter is reset to zero because the variable is reinitialized.

