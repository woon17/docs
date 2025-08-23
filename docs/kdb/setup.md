# KDB+ Setup on M3 (Arm64)

## Issue with M3 Architecture

KDB+ can run on Arm64, but it causes integration issues with other tools like KDB Developer.

## Setup Steps

### 1. Open Terminal with Rosetta (Intel/x86_64 mode)

```bash
arch -x86_64 /System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal &
```

### 2. Build OpenSSL 1.1 Manually

Homebrew has disabled OpenSSL 1.1, so we need to build it manually.

!!! warning "Important"
    Make sure the terminal is opened with Rosetta (`uname -m` should return `x86_64`), otherwise you'll encounter issues when installing KDB Developer.

### 3. Install OpenSSL 1.1

Download and build OpenSSL 1.1.1w:

```bash
mkdir -p ~/dev/openssl-1.1-x86
cd ~/dev/openssl-1.1-x86

curl -LO https://www.openssl.org/source/openssl-1.1.1w.tar.gz
tar -xzf openssl-1.1.1w.tar.gz
cd openssl-1.1.1w

./Configure darwin64-x86_64-cc --prefix=$HOME/openssl-1.1-x86
make -j$(sysctl -n hw.logicalcpu)
make install
```

Create symbolic links:

```bash
sudo mkdir -p /usr/local/opt/openssl@1.1/lib

sudo ln -sf ~/openssl-1.1-x86/lib/libssl.1.1.dylib /usr/local/opt/openssl@1.1/lib/libssl.1.1.dylib
sudo ln -sf ~/openssl-1.1-x86/lib/libcrypto.1.1.dylib /usr/local/opt/openssl@1.1/lib/libcrypto.1.1.dylib
```

Verify the installation:

```bash
file /usr/local/opt/openssl@1.1/lib/libssl.1.1.dylib
# Should output: Mach-O 64-bit dynamically linked shared library x86_64
```

### 4. Remove Quarantine from KX Developer Files

Remove quarantine attributes from all .so files in the KX Developer folder:

```bash
find /path/to/kx-developer -name "*.so" -exec xattr -d com.apple.quarantine {} +
```
