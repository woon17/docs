# GitHub SSH Key Management
## Generate an SSH Key for GitHub

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github
```

- `-C` is a comment (any label, not functionally required)
- `-f` specifies the filename to save the key
- Press **Enter twice** to skip setting a passphrase (or set one for security)



## Add the Public Key to GitHub

```bash
cat ~/.ssh/id_ed25519_github.pub
```

1. Copy the output
2. Go to [GitHub → Settings → SSH and GPG keys](https://github.com/settings/keys)
3. Click **"New SSH key"**, give it a name, and paste the public key



## Configure SSH to Use the Right Key

Edit (or create) the `~/.ssh/config` file:

```ini
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
```
The `IdentitiesOnly yes` tells SSH to use only this key instead of offering every key in your agent.

without it, it will try:

- Keys from ssh-agent
- Default files in ~/.ssh/ 
    - ~/.ssh/id_rsa
    - ~/.ssh/id_ecdsa
    - ~/.ssh/id_ed25519
    - ~/.ssh/id_dsa
    - Any others added in recent OpenSSH versions
- Keys listed in your ~/.ssh/config for the current Host (`Host github.com`)

with it, SSH uses only the key you specified — no default keys, no ssh-agent keys, no surprises.


## Test SSH Connection to GitHub
=== "ssh -T"
    this is assume I configed the ssh key correctly (using ssh-add(ssh-agent) or editing ~/.ssh/config)

    ```bash
    ssh -T git@github.com
    ```

    Expected result:

    ```
    Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
    ```

=== "ssh using specific key"
    Use case:
    
    - You're testing if a specific key works
    - You haven’t set up a config file or SSH agent
    - You want a one-off manual override
    ```bash
    ssh -i ~/.ssh/id_ed25519_github git@github.com
    ```

    Expected result:

    ```
    PTY allocation request failed on channel 0
    Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
    Connection to github.com closed.
    ```
## Use SSH with Git

```bash
git clone git@github.com:your-username/your-repo.git
```

## Notes

- GitHub uses `git@github.com` for all SSH connections.
- SSH authentication is done via **public key fingerprint**, not username.
- GitHub matches the SSH key to your account during the handshake.
- You can manage multiple SSH keys by configuring `~/.ssh/config` for each host.
