Aeron is called a Layer 4 transport because it handles end-to-end message delivery, flow control, and reliability decisions — just like TCP/UDP. It's unique because it's designed from scratch for high-throughput, low-latency, and customizable transport logic, making it ideal for systems like trading engines, media streaming, and telemetry.

# Layer 4 vs Layer 7 Messaging Solutions

## Layer 4 vs Layer 7 Solutions

| Aspect | Layer 4 (e.g., Aeron) | Layer 7 (e.g., Kafka, gRPC) |
|--------|---------------------------|----------------------------------|
| OSI Role | Transport (reliability, flow, delivery) | Application (business logic, formats, routing) |
| Latency | Ultra-low (~µs) | Higher (~ms) |
| Protocol Overhead | Minimal (e.g., UDP + custom framing) | High (TCP, TLS, HTTP, JSON, etc.) |
| Memory Usage | Lean (no serialization unless needed) | High (serialization, buffering) |
| Threading | App-controlled, often lock-free | Thread pools, GC pressure |
| Flexibility | Full control of transport behavior | Fixed protocol stack (e.g., HTTP2 → gRPC) |
| Reliability | Optional, app-defined | Built-in, protocol-controlled |
| Back Pressure | App-level, precise control | Harder to tune, coarse-grained |
| Examples | Aeron, ZeroMQ (some modes), TCP, UDP | Kafka, RabbitMQ, gRPC, HTTP |

---

## Why Layer 4 (Aeron) is Much Faster

### 1. Fewer Layers → Less Work
Layer 7 adds multiple processing stages: protocol parsing, authentication, routing, deserialization.  
Aeron stays close to the metal — minimal parsing, minimal system calls.

### 2. No TCP Overhead
TCP adds latency from:
- Congestion control (slow start, retransmissions)
- Head-of-line blocking
- Connection setup (3-way handshake)
- Stream-oriented framing

Aeron uses UDP or shared memory and handles:
- Framing
- Retransmission (if needed)
- Flow control  
All at the application level, giving much finer control and predictability.

### 3. Memory and CPU Optimized
Aeron uses:
- Off-heap memory
- Lock-free ring buffers
- Busy-spinning to eliminate context switching and GC pauses

Layer 7 tools (e.g., Kafka, gRPC) often involve:
- Heap allocations
- Serialization (e.g., Protobuf, JSON)
- GC pressure
- Thread pool context switching

### 4. Deterministic Performance
Layer 4 solutions like Aeron are tuned for consistent latency, crucial in:
- High-frequency trading
- Video streaming
- Gaming

Layer 7 tools favor feature richness over raw speed.

---

## Analogy

- **Layer 4 (Aeron)** = Motorbike on an express lane: Fast, controlled, no traffic lights  
- **Layer 7 (Kafka/gRPC)** = Bus on city roads: More features (passengers, stops), but slower

---

## Summary

| Layer 4 (Aeron) | Layer 7 (Kafka/gRPC) |
|---------------------|---------------------------|
| Transport-focused | Feature-focused |
| Raw speed, tight control | Abstraction, rich features |
| Ideal for low-latency trading, IPC | Ideal for business logic, microservices |
