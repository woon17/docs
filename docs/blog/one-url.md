# Open `https://www.google.com` in Chrome

Opening a URL like `https://www.google.com` feels effortless, but under the hood, the browser performs a complex series of operations involving DNS, TCP, TLS, and HTTP. This guide walks through each step — and how to inspect them using terminal.

---

## Full Workflow When Opening a URL

Steps performed by the browser:

1. **URL parsing**
2. **DNS resolution** – Resolves `www.google.com` to an IP address.
3. **TCP connection** – Connects to port 443 (HTTPS).
4. **TLS handshake** – Establishes a secure session.
5. **HTTP GET request** – Requests content from the server.
6. **HTTP response** – Receives data.
7. **Rendering** – Renders HTML/CSS/JS content.

---

## Inspecting Each Step in Terminal

We’ll use `www.google.com` in all examples.

---

### 1. DNS Resolution via dig

**Command:**
```bash
dig www.google.com
```
The resolved IP address(es) of www.google.com
```bash
;; QUESTION SECTION:
;www.google.com.			IN	A

;; ANSWER SECTION:
www.google.com.		87	IN	A	142.250.4.105
www.google.com.		87	IN	A	142.250.4.99
```

```
| Field             | Meaning                                                                |
| ----------------- | ---------------------------------------------------------------------- |
| `www.google.com.` | The domain I queried                                                 |
| `87`              | TTL (Time To Live) in seconds — how long this record can be cached |
| `IN`              | Class of record — "IN": "Internet"                           |
| `A`               | Record type — "A": IPv4 address                                   |
| `142.250.4.105`   | One of the **IPv4 addresses** for `www.google.com`                     |

```

1. Why Are There Multiple IPs? (DNS load balancing or round-robin DNS)
    1. Google has many servers worldwide to handle billions of requests.
    1. When I access www.google.com, my system picks one IP from this list (often the closest one).
    1. This improves availability, speed, and redundancy.
1. TTL 87
    1. my system or browser can cache this DNS response for 87 seconds.
    2. After that, it must ask the DNS server again (could get different IPs next time).

### 2. DNS + TCP + TLS + HTTP via curl
```bash
curl -v https://www.google.com
```
show: DNS lookup, TCP connection attempt, TLS handshake, HTTP request/response

```bash
* Host www.google.com:443 was resolved.
* IPv6: (none)
* IPv4: 142.250.4.103, 142.250.4.147, 142.250.4.106, 142.250.4.104, 142.250.4.99, 142.250.4.105
*   Trying 142.250.4.103:443...
* Connected to www.google.com (142.250.4.103) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
*  CAfile: /etc/ssl/cert.pem
*  CApath: none
* (304) (IN), TLS handshake, Server hello (2):
* (304) (IN), TLS handshake, Unknown (8):
* (304) (IN), TLS handshake, Certificate (11):
* (304) (IN), TLS handshake, CERT verify (15):
* (304) (IN), TLS handshake, Finished (20):
* (304) (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=www.google.com
*  start date: May 12 08:44:44 2025 GMT
*  expire date: Aug  4 08:44:43 2025 GMT
*  subjectAltName: host "www.google.com" matched cert's "www.google.com"
*  issuer: C=US; O=Google Trust Services; CN=WR2
*  SSL certificate verify ok.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://www.google.com/
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: www.google.com]
* [HTTP/2] [1] [:path: /]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET / HTTP/2
> Host: www.google.com
> User-Agent: curl/8.7.1
> Accept: */*

```

| Step                 | What Happened                                                 |
| -------------------- | ------------------------------------------------------------- |
| DNS Resolution       | Found multiple IPs, used `142.250.4.103`                      |
| TCP Connection       | Connected to IP:443                                           |
| TLS Handshake        | TLS 1.3 used; cipher `CHACHA20-POLY1305` negotiated           |
| Certificate Check    | Issued by Google Trust; matched domain; verified successfully |
| Protocol Negotiation | Chose HTTP/2 via ALPN                                         |
| HTTP Request         | Sent `GET /` with headers over a secure HTTP/2 channel        |

`CAfile: /etc/ssl/cert.pem`:
    This line tells me where curl is looking for trusted Certificate Authorities (CAs) to verify the HTTPS server's certificate. This file is a bundle of trusted root certificates, pre-installed by my operating system (usually   macOS or Linux). It allows curl (or any SSL/TLS library like OpenSSL or SecureTransport) to say: `Do I trust the  certificate from www.google.com? Let me check if it's signed by someone I trust (e.g., Google Trust Services`

| Item           | Explanation                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| `CAfile:`      | Path to the file containing trusted Certificate Authorities (CAs)                           |
| Used For       | Verifying if a server's HTTPS certificate is **valid and trusted**                          |
| File Example   | `/etc/ssl/cert.pem` (can vary by OS — e.g., `/etc/pki/ca-trust/extracted/` on some distros) |
| Related Option | I can override with `curl --cacert /path/to/custom.pem`                                   |

`* (304) (IN), TLS handshake, Unknown (8)`: 

| Output                        | Meaning                                                            |
| ----------------------------- | ------------------------------------------------------------------ |
| `TLS handshake, Unknown (8):` | TLS 1.3 server sent an **Encrypted Extensions** message            |
| Why it's “Unknown”            | `curl -v` just doesn’t label it clearly (not a bug, just cosmetic) |
| Is this bad?                  | ❌ No — it's part of every proper TLS 1.3 connection                |


### 3. View TLS Details via openssl
    (TLS version, certs, ciphers): `openssl s_client -connect example.com:443`



### 4. Availability via curl
Checking if the server is reachable and what headers it returns: `curl -I https://example.com`

Debugging the full connection including DNS, TCP, TLS, and HTTP request/response: `curl -v https://www.google.com`