# Issue with M3(Arm64): 
##kdb+ and kdb developer

setup kdb+: although it is okay to run with arm64, but it will cause other issue when integrate with others (ie. kdb developer)

1. new Terminal window that runs under Rosetta (Intel/x86_64 mode) 
    
    ```bash
    arch -x86_64 /System/Applications/Utilities/Terminal.app/Contents/MacOS Terminal &
    ```

2. openssl1.1, need to build banary manually as homebrew disable openssl1.1 already
3. openssl1.1, make sure terminal is opened `with rosetta` (uname -m = x86_64), otherwise u will suffer again when installing kdb developer
   
    ```bash
    mkdir -p ~/dev/openssl-1.1-x86
    cd ~/dev/openssl-1.1-x86

    curl -LO https://www.openssl.org/source/openssl-1.1.1w.tar.gz
    tar -xzf openssl-1.1.1w.tar.gz
    cd openssl-1.1.1w

    ./Configure darwin64-x86_64-cc --prefix=$HOME/openssl-1.1-x86
    make -j$(sysctl -n hw.logicalcpu)
    make install


    sudo mkdir -p /usr/local/opt/openssl@1.1/lib

    sudo ln -sf ~/openssl-1.1-x86/lib/libssl.1.1.dylib /usr/local/opt/openssl@1.1/lib/libssl.1.1.dylib
    sudo ln -sf ~/openssl-1.1-x86/lib/libcrypto.1.1.dylib /usr/local/opt/openssl@1.1/lib/libcrypto.1.1.dylib

    file /usr/local/opt/openssl@1.1/lib/libssl.1.1.dylib # Mach-O 64-bit dynamically linked shared library x86_64
    ```

4. One-liner to remove quarantine from all .so files in a kdb folder (recursively):

    ```bash
    find /path/to/kx-developer -name "*.so" -exec xattr -d com.apple.quarantine {} +
    ```
