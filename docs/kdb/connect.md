# connect to kdb+ manually

This guide helps you verify that your KDB+ instance is running and accepting remote connections — useful for Java integration, KX Dashboards, etc.

---

## Start a KDB+ Process Listening on a Port

Open a terminal and run:

```bash
q -p 5000
```

> This starts KDB+ (q process) and listens for incoming IPC connections on port 5000.

---

## Open a Second Terminal

Start another q session (acts like a client):

```bash
q
```

---

## Connect to the First KDB+ Process

In the second q session:

```q
h: hopen `:localhost:5000
```

This opens a handle `h` to the KDB+ server running on port 5000.

---

## Send a Test Command

Send a command to the remote session:

```q
h "1+1"
```

You should see the result in the Second q process:

```q
2
```


---

## Result

If the command returns `2`, your KDB+ server is reachable and working.

You can now connect to it from Java or any IPC-compatible client using:
```java
new Connection("localhost", 5000);
```