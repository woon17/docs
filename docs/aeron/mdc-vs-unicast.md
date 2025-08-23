# Aeron MDC vs Unicast – Key Differences

When it comes to the UDP protocol, we can either use Unicast, which sends messages one to one, or multicast, which sends messages to many

## Overview

This guide compares Aeron's two main communication patterns for UDP-based messaging, helping you choose the right approach for your use case.

## Comparison Table

| Feature                      | **Aeron Unicast**                            | **Aeron MDC (Multi-Destination-Cast)**                     |
|-----------------------------|-----------------------------------------------|------------------------------------------------------------|
| **Protocol**                | UDP                                           | UDP                                                       |
| **Communication Type**     | 1 Publisher → 1 Subscriber                    | 1 Publisher → N Subscribers                               |
| **Control Mode**           | Not required                                  | `manual` or `dynamic` control mode required               |
| **Subscriber Registration** | Static (hardcoded endpoints)                  | Dynamic or manual registration of subscribers             |
| **Publisher Setup**        | Uses `endpoint=...`                           | Uses `control-mode=dynamic` + `control=host:port`         |
| **Subscriber Setup**       | Uses `endpoint=...`                           | Uses `endpoint=...|control=...|control-mode=dynamic`      |
| **Multicast Needed?**      | ❌ No                                          | ❌ No (achieves fanout via unicast)                        |
| **Dynamic Join/Leave**     | ❌ No (fixed peer)                             | ✅ Yes (subscribers can join/leave dynamically)            |
| **Number of Subscribers**  | 1 only                                        | Multiple                                                  |
| **Efficiency**             | Very efficient (1 send)                       | Less efficient (N sends for N subscribers)                |
| **Flexibility**            | Low                                           | High                                                      |
| **Typical Use Case**       | Point-to-point communication                  | Broadcast-like use case, clusters, logs, market data      |

---

## Channel Configuration Examples

### Unicast Channel
```
aeron:udp?endpoint=localhost:40123
```

### MDC (Publisher)
```
aeron:udp?control-mode=dynamic|control=localhost:40123
```

### MDC (Subscriber)
```
aeron:udp?endpoint=localhost:40124|control-mode=dynamic|control=localhost:40123
```

---

## Key Points

!!! info "MDC Implementation"
    **MDC uses unicast UDP under the hood**, but gives **multicast-like fan-out**. This approach avoids the complexity of multicast infrastructure while providing broadcast capabilities.

!!! tip "When to Use MDC"
    - **Pub/sub** patterns without relying on multicast infrastructure
    - **Aeron Cluster** and **high-availability systems**
    - Market data distribution scenarios
    - Log replication across multiple nodes

## See Also

- [Aeron Advantages](adv.md) - Why choose Aeron for messaging
- [Coinbase Fix API Integration](artio/coinbase.md) - Real-world Aeron implementation