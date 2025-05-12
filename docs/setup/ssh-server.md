# client to server by using ssh (windows version)
## set up: 
- You (Windows) = SSH Client
- VM (Linux) = SSH Server

## Generate an SSH Key in client

```bash
ssh-keygen -t ed25519 -C "vm test" -f ~/.ssh/id_ed25519_key
```

- `-C` is a comment (any label, not functionally required)
- `-f` specifies the filename to save the key
- Press **Enter twice** to skip setting a passphrase (or set one for security)



## Add the Public Key to vm server

```bash
cat ~/.ssh/id_ed25519_key.pub # in Client
```

1. Copy the output
2. login vm server by password first (ssh -p 1234 woon@1.0.0.X)
3. `vim ~/.ssh/authorized_keys # in server` and paste the public key in the last entry



## Configure SSH to Use the Right Key

Edit (or create) the `C:\Users\woon\.ssh\config` file: 

```ini
# in Client
Host X.0.0.X
  User woon
  Port 1234
  HostName X.0.0.X
  IdentityFile C:\Users\woon\.ssh\id_ed25519_key
  IdentitiesOnly yes
```


## Test SSH Connection to server
`ssh X.0.0.X` (Host X.0.0.X in client .ssh/config)
```bash
ssh -vvv X.0.0.X # in Client
```

Expected result (for the first time):

```bash
The authenticity of host '[X.0.0.X]:1234 ([X.0.0.X]:1234)' can't be established.
ED25519 key fingerprint is SHA256:abcd/efg.
This host key is known by the following other names/addresses:
    C:\Users\woon/.ssh/known_hosts:1: [X.0.0.1]:1234
    C:\Users\woon/.ssh/known_hosts:2: [X.0.0.4]:1234
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[X.0.0.X]:1234' (ED25519) to the list of known hosts.
Connection reset by X.0.0.X port 1234
```

* `SHA256:abcd/efg.` the SSH host fingerprint shown when you connect to a server is derived from the public host key files
    * To see the fingerprint for the ED25519 key 
        ```bash
        # Each Linux system running an SSH server has its own set of host keys stored in /etc/ssh
        /etc/ssh$ ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub # in Server
        ```
* 'This host key is known by the following other names/addresses' :  Cloned VMs Will Share Fingerprints
  * a new fingerprint will be saved to your known_hosts in the windows client machine. `C:\Users\woon\.ssh>more known_hosts # in Client`

