# LMAX Disruptor & Conduit Framework

## Overview

The LMAX Disruptor is a high-performance inter-thread messaging library that provides a simple yet powerful framework for exchanging data between threads. It is designed for low-latency, high-throughput scenarios where traditional queuing mechanisms introduce too much overhead.

The **Conduit** framework builds on top of the LMAX Disruptor to provide a reactive, event-driven architecture for building complex data processing pipelines.

## What is the LMAX Disruptor?

The LMAX Disruptor is a library that enables very high performance concurrent programming. It was developed by LMAX Exchange, a financial trading platform that required extremely low-latency message passing between threads.

### Key Features

- **Lock-free**: Uses CAS (Compare-And-Swap) operations instead of locks
- **Ring Buffer**: Pre-allocated circular buffer eliminates garbage collection overhead
- **Memory Barriers**: Carefully controlled memory visibility without locks
- **Cache-friendly**: Data structures designed to minimize cache line contention
- **Batching**: Naturally supports batch processing of events

### Core Concepts

#### Ring Buffer
A fixed-size circular buffer that holds references to events. It's pre-allocated at startup, which eliminates memory allocation during runtime.

```mermaid
flowchart LR
    S0["slot 0"] --> S1["slot 1"] --> S2["slot 2"] --> S3["slot 3"] --> S0
    Producer["Producer cursor<br/>(next slot to write)"] -.-> S1
    Consumer["Consumer cursor<br/>(next slot to read)"] -.-> S3
```

The buffer never grows or shrinks — producer and consumer cursors just keep advancing and
wrapping back to slot 0 once they pass the end. See
[Hand-Rolled Ring Buffer](hand-rolled-ring-buffer.md) for exactly how that wrap-around is made
safe without locks.

#### Sequence Numbers
Used to track positions in the ring buffer. Producers claim sequence numbers before writing, and consumers track which events they've processed.

#### Wait Strategies
Different strategies for consumers waiting for new events:

- **BusySpinWaitStrategy**: Lowest latency, highest CPU usage
- **YieldingWaitStrategy**: Low latency with some CPU yield
- **SleepingWaitStrategy**: Lower CPU usage, higher latency
- **BlockingWaitStrategy**: Lowest CPU usage, highest latency

## Why Use Disruptor?

### Traditional Queue Problems

Traditional concurrent queues (like `java.util.concurrent` queues) suffer from:

1. **Lock Contention**: Multiple threads competing for locks
2. **Cache Coherency**: False sharing and cache line bouncing
3. **Memory Allocation**: Creating/destroying objects causes GC pressure
4. **Context Switching**: Blocking operations cause thread context switches

### Disruptor Solutions

| Problem | Disruptor Solution |
|---------|-------------------|
| Lock Contention | Lock-free algorithms using CAS |
| Cache Coherency | Cache line padding to prevent false sharing |
| Memory Allocation | Pre-allocated ring buffer |
| Context Switching | Busy-spin wait strategies |

## Performance Characteristics

The Disruptor can process **millions of events per second** with **nanosecond latencies** on modern hardware.

### Benchmark Comparison

| Queue | Throughput (ops/sec) |
|---|---|
| Disruptor | ~25M |
| `ArrayBlockingQueue` | ~5M |
| `LinkedBlockingQueue` | ~3M |

!!! note "Illustrative, not measured on this project's hardware"
    These numbers are the kind of ratio commonly cited for the Disruptor vs. `java.util.concurrent`
    queues, not a benchmark run captured on a specific machine here. Treat them as "expect roughly
    this shape of difference," and benchmark on your own target hardware before relying on exact
    figures — see the real, captured numbers in
    [Hand-Rolled Ring Buffer](hand-rolled-ring-buffer.md#benchmark) for an example of the latter.

## Common Use Cases

1. **Financial Trading Systems**: Ultra-low latency order processing
2. **Real-time Analytics**: High-throughput data stream processing
3. **Event Sourcing**: Recording domain events in order
4. **Log Aggregation**: Collecting and processing log entries
5. **IoT Data Processing**: Handling sensor data streams

## Getting Started

To use the Disruptor in your project, add the dependency:

```xml
<dependency>
    <groupId>com.lmax</groupId>
    <artifactId>disruptor</artifactId>
    <version>4.0.0</version>
</dependency>
```

## Next Steps

- [Conduit Framework Overview](conduit-framework.md) - Learn about the reactive framework built on Disruptor
- [Performance Comparison](performance.md) - Detailed performance analysis
- [Example Applications](examples.md) - Real-world usage examples
- [Lock-free & CAS](lock-free-cas.md) - Deep dive into lock-free programming and Compare-And-Swap
- [Hand-Rolled Ring Buffer](hand-rolled-ring-buffer.md) - From-scratch MPSC ring buffer implementation, line by line

## Resources

- [LMAX Disruptor GitHub](https://github.com/LMAX-Exchange/disruptor)
- [Technical Paper](https://lmax-exchange.github.io/disruptor/disruptor.html)
- [Martin Fowler's Article](https://martinfowler.com/articles/lmax.html)
