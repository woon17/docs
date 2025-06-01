## Find which process is using a specific port 8080:
```bash
lsof -i :8080
```

##  lists processes listening on TCP port 8082, showing clean output
```bash
lsof -nP -iTCP:8080 -sTCP:LISTEN
```

| Option         | What It Does                                                                 |
|----------------|------------------------------------------------------------------------------|
| `lsof`         | Lists open files (including network sockets)                                 |
| `-n`           | Don’t resolve IPs to hostnames (faster, no DNS delay)                        |
| `-P`           | Don’t convert port numbers to names (e.g. show `8082` instead of `us-cli`)   |
| `-iTCP:8082`   | Filter: only show TCP connections on port 8082                               |
| `-sTCP:LISTEN` | Filter: only show **listening** sockets (not established connections)        |


## detailed information about the process with PID ( using wide output (no truncation).)

```bash
ps -p 123 -ww
```

`-ww`:	Show full command line without cutting off arguments (double w means no truncation at all)

##  lists all running Java processes with their PID and main class or jar file.

```bash
jps -l
```

## shows which IP/port the Java process(pid=12345) is listening on

```bash
lsof -nP -p 12345 -iTCP -sTCP:LISTEN
```

## List all open network ports (Java or not)
```bash
lsof -nP -iTCP -sTCP:LISTEN
or 
netstat -anp tcp
```


## show both TCP and/or UDP

```bash
lsof -i
lsof -iTCP
lsof -iUDP
```


## Check UDP Connectivity via nc (netcat):  see the message, UDP is open.

```bash
listener: listen on my port 1234
nc -u -l -p 1234

publisher: send msg to listener ip:port
echo "test" | nc -u <listener_public_ip> 1234


```
