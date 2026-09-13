# Use case: coinbase fix api

## info

1. Artio solution does [not support SSL/TLS](https://github.com/artiofix/artio/issues/238). use [stunnel](https://www.stunnel.org/) and haproxy

    ```mermaid
    flowchart LR
        Artio["Artio<br/>(plain TCP, no TLS)"] --> HAProxy["haproxy"] --> Stunnel["stunnel<br/>(TLS termination)"] --> Coinbase["Coinbase FIX endpoint<br/>(TLS required)"]
    ```

    Artio speaks plain TCP; `stunnel` is what actually wraps the connection in TLS before it
    reaches Coinbase, with `haproxy` in front for routing/load-balancing.


2. use openssl to verify connection to Sandbox fix endpoint
    ```bash
    openssl s_client -connect fix-ord.sandbox.exchange.coinbase.com:6121 -tls1_2
    openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -tls1_2
    ```
