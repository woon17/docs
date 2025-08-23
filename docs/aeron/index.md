# Aeron Messaging

Welcome to Aeron documentation covering high-performance messaging protocols and low-latency communication patterns.

## Overview

Aeron is a high-performance messaging library designed for low-latency, high-throughput applications. It's particularly well-suited for financial systems, real-time analytics, and distributed systems requiring reliable message delivery.

## Core Topics

### Fundamentals
- **[Why Aeron?](adv.md)** - Advantages and use cases for Aeron messaging
- **[MDC vs Unicast](mdc-vs-unicast.md)** - Understanding Multi-Destination-Cast vs traditional unicast patterns

### Integration Examples
- **[Artio Fix Integration](artio/coinbase.md)** - Real-world implementation with Coinbase Fix API

## Key Features

### Performance Characteristics
- **Low Latency**: Optimized for microsecond-level messaging
- **High Throughput**: Handles millions of messages per second
- **Zero Copy**: Efficient memory usage patterns
- **Mechanical Sympathy**: Hardware-aware design

### Communication Patterns
- **Unicast**: Point-to-point reliable messaging
- **Multi-Destination-Cast (MDC)**: Efficient one-to-many communication
- **Publication/Subscription**: Event-driven messaging patterns

## Getting Started

!!! tip "New to Aeron?"
    Start with [Why Aeron?](adv.md) to understand the advantages, then explore [MDC vs Unicast](mdc-vs-unicast.md) to choose the right communication pattern.

### Learning Path
1. **Understand the Advantages** - Learn [why choose Aeron](adv.md) over other messaging solutions
2. **Communication Patterns** - Study [MDC vs Unicast](mdc-vs-unicast.md) trade-offs
3. **Real-world Examples** - Explore [Artio integration](artio/coinbase.md) implementations
4. **Performance Tuning** - Apply optimization techniques for your use case

## Use Cases

### Ideal Applications
- **Financial Trading Systems** - Low-latency order processing and market data
- **Real-time Analytics** - High-frequency data processing pipelines  
- **Distributed Systems** - Reliable inter-service communication
- **Gaming Infrastructure** - Real-time multiplayer game state synchronization

### When to Choose Aeron
- Sub-millisecond latency requirements
- High message throughput needs (1M+ messages/sec)
- Reliable delivery without complex middleware
- Direct control over messaging infrastructure

## Architecture Patterns

### Publisher-Subscriber Model
```
Publisher → Aeron Transport → Multiple Subscribers
```

### Request-Response Pattern
```
Client ←→ Aeron Transport ←→ Server
```

### Cluster Communication
```
Node A ←→ Aeron Cluster ←→ Node B, C, D
```

## Related Topics

- **[System Design](/system_design/)** - Architecture patterns for distributed systems
- **[Java Threading](/java/thread/)** - Concurrent programming for high-performance messaging
- **[KDB+ Integration](/kdb/)** - Database connectivity for real-time data processing

---

## Performance Considerations

Aeron's design prioritizes mechanical sympathy - understanding and working with hardware characteristics for optimal performance. This includes CPU cache usage, memory allocation patterns, and network interface optimization.

!!! note "Production Deployment"
    Aeron excels in production environments where predictable latency and high throughput are critical. Consider network topology, hardware specifications, and operating system tuning for optimal results.