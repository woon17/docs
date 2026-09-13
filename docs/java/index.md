# Java Development

Welcome to Java development documentation covering memory management, concurrency patterns, and threading best practices.

## Overview

This section provides comprehensive coverage of Java fundamentals and advanced topics, with particular focus on memory management and concurrent programming patterns essential for high-performance applications.

## Core Topics

### Memory Management
- **[Stack vs Heap Memory](test.md)** - Understanding Java's memory model and allocation patterns
- **[Agrona's Agent Pattern, Explained](agrona-agent-pattern.md)** - `Agent`/`AgentRunner`/`IdleStrategy` from scratch — the plumbing behind every GC demo agent below
- **[GC Basics, Visually](gc-basics.md)** - Generations, Eden/Survivor, and G1 regions explained with diagrams, from zero
- **[GC Deep Dive: Leak to OOM](gc-leak-oom.md)** - G1 regions, humongous objects, and GC-log analysis, built from a real leak-to-crash walkthrough
- **[GC Case Study: Healthy Churn](gc-survivor-demo.md)** - The Eden/Survivor/Old cycle actually happening, contrasted against the leak

### Threading & Concurrency
- **[Threading Guide](thread/)** - Complete guide to Java threading concepts and patterns
- **[Visibility Issues](thread/visibility.md)** - Understanding memory visibility in multi-threaded applications
- **[Atomicity Issues](thread/atomicity.md)** - Ensuring atomic operations in concurrent code
- **[Ordering Issues](thread/ordering.md)** - Memory ordering and synchronization
- **[Volatile Keyword](volatile.md)** - Understanding volatile and its proper usage

### Threading Use Cases
- **[Blocking Tasks](thread/block-task.md)** - Handling I/O-bound operations with threads
- **[CPU-Intensive Tasks](thread/CPU-Intensive-task.md)** - Optimizing compute-heavy workloads  
- **[Small, Fast Tasks](thread/small-fast-task.md)** - High-volume, low-latency task processing

### Application Lifecycle
- **[Shutdown Mechanisms](shutdown.md)** - Proper application shutdown and resource cleanup

## Getting Started

!!! tip "New to Java Threading?"
    Start with the [Threading Guide](thread/) to understand fundamental concepts, then explore specific use cases based on your application needs.

### Learning Path
1. **Memory Fundamentals** - Understand [Stack vs Heap](test.md) memory allocation
2. **Threading Basics** - Learn core concepts from the [Threading Guide](thread/)
3. **Concurrency Issues** - Study [visibility](thread/visibility.md), [atomicity](thread/atomicity.md), and [ordering](thread/ordering.md) problems
4. **Practical Applications** - Apply knowledge to specific [use cases](thread/block-task.md)

## Best Practices

### Performance Considerations
- Choose appropriate threading patterns based on workload characteristics
- Understand when multiple threads help vs. hurt performance
- Proper resource management and cleanup

### Common Pitfalls
- Race conditions and synchronization issues
- Memory leaks in multi-threaded applications
- Improper use of volatile and synchronization primitives

## Related Topics

- **[System Design](../system_design/)** - Architecture patterns for scalable systems
- **[KDB+ Integration](../kdb/)** - Database connectivity and performance optimization
- **[Spring Boot](../spring-boot/)** - Application framework integration

---

## Contributing

This documentation includes practical examples, performance benchmarks, and real-world use cases. Each section provides both theoretical background and hands-on implementation guidance.