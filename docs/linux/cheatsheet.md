## Check files or folders size (human-readable sizes)
```bash
show size of all items in current directory (sort by size)
du -sh * | sort -hr
ls -lah
```


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

## storage
```bash
// Check total size of current folder
du -sh .

// See size of each subfolder
du -sh *

// Sort folders by size (reverse -hr)
du -sh * | sort -h


// Check disk free space (overall, not folder)
df -h .
```


## IP
```bash
// Check mac local/private ip
ipconfig getifaddr en0 
```

## Check what service/process/task are using the port
```bash
ps aux | grep PID
```

## docker
```bash
// Show running containers
docker ps
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

// Show ALL containers (running + stopped)
docker ps -a

// Check logs (to confirm it’s alive)
docker logs grafana
docker logs -f grafana

// See what ports are exposed
docker port grafana
or
docker ps | grep grafana

```

## Quick external test in the same laptop (local ports exposed?)
```bash
// find your public IP
curl ifconfig.me
-> 1.2.3.4

// Try to open a TCP connection to <PUBLIC_IP> on port 1234 and tell me if it succeeds.
same laptop:
1. Tries to reach its own public IP
2. That traffic goes to the router
Router decides:
  ❌ drop it (no port forward) → SAFE
  ✅ forward it to laptop:1234 → EXPOSED
But ⚠️ IMPORTANT caveat (very important)
Some routers do not support NAT loopback. nc from the same laptop will always fail, Even if the port is actually exposed to the internet

The REAL definitive test:
Use a device NOT on your Wi-Fi
http://1.2.3.4:1234
```
