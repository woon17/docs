# Use cases - Blocking Tasks (e.g., UI, I/O)
## What's the problem?
When a thread waits for something (like reading from disk, getting user input, or waiting for a network response), it does nothing during that time.

## Single-threaded issue:
If you're using only one thread, your program halts and can't do anything else while waiting.

## Multi-threaded solution:
Put the blocking task on a separate thread. The main thread can continue running, updating UI, or processing other events.

## Example: Chat app with file upload
1. You click "Upload file".
1. Upload takes 10 seconds due to network.
1. Without threads, the entire UI freezes for 10 seconds (annoying).
1. With threads, the UI is responsive while the file uploads in background.

```java
// Good use of thread to handle blocking I/O
new Thread(() -> {
    uploadFile(); // simulate 10-second blocking task
}).start();
```