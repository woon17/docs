# Use cases - Small, Fast Tasks (High Volume)
## What's the problem?
If you do 1 million tiny tasks one by one, you underutilize your CPU.

## Single-threaded issue:
One thread does all tasks → slow throughput.

## Multi-threaded solution:
Create a thread pool that processes many tasks in parallel. This increases throughput dramatically.

##  Example: Prime number calculator
1. Each hash takes ~1 microsecond.
1. Doing sequentially = slow.
1. Spread across 8 threads → process in parallel.

we can finish the batch faster because many threads handle many tasks at once.

```java
ExecutorService pool = Executors.newFixedThreadPool(8);
for (int i = 0; i < 1_000_000; i++) {
    pool.submit(() -> hash(UUID.randomUUID()));
}
```