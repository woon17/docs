
# Graceful Shutdown in Java using ShutdownSignalBarrier

This document explains how to use `ShutdownSignalBarrier` and `SigInt.register` for graceful shutdown in Java applications.

## Purpose

To handle shutdown signals (like Ctrl+C) gracefully and ensure that the main thread does not terminate unexpectedly. This is commonly used in systems like Aeron, Netty, or long-running microservices.

---

## Code Example

```java
ShutdownSignalBarrier barrier = new ShutdownSignalBarrier();
SigInt.register(() -> {
    barrier.signal();
    System.out.println("Signal received");
});

barrier.await();
System.out.println("Main thread terminated");
```

---

## Explanation

| Component              | Purpose                                              |
|------------------------|------------------------------------------------------|
| `ShutdownSignalBarrier` | Blocks the main thread until a shutdown signal is received |
| `SigInt.register(...)`  | Registers a signal handler for SIGINT (Ctrl+C)      |
| `barrier.signal()`      | Unblocks the main thread                            |
| `barrier.await()`       | Waits for the shutdown signal                       |

---

## Use Cases

- Aeron applications
- Long-running agents or daemons
- Console-based servers
- Microservices that require proper cleanup

---

## Summary

This mechanism is essential to:

- Keep the application running until explicitly terminated
- Ensure clean resource release
- Avoid ungraceful shutdowns that might corrupt state or leave ports open

