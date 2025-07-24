# Use case: coinbase fix api

## info

1. Artio solution does [not support SSL/TLS](https://github.com/artiofix/artio/issues/238). use [stunnel](https://www.stunnel.org/) and haproxy

2. use openssl to verify connection to Sandbox fix endpoint
    ```bash
    openssl s_client -connect fix-ord.sandbox.exchange.coinbase.com:6121 -tls1_2
    openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -tls1_2
    ```
