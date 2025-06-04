# Use cases - CPU-Intensive Tasks
## What's the problem?
One thread = one core. If your task is heavy (e.g., calculating 1 million primes), the thread will use one CPU core only.

## Single-threaded issue:
Even if you have 8 CPU cores, you're only using 1. Wasteful.

## Multi-threaded solution:
Split the work into chunks, run each on a separate thread. Parallelism = much faster.

##  Example: Prime number calculator
1. 1 million numbers → find primes.
1. Split into 4 chunks.
1. Use 4 threads → 4 CPU cores at once.
   
we can reduce total runtime because 4 cores are working simultaneously.

```java
// Each thread works on a chunk
ExecutorService pool = Executors.newFixedThreadPool(4);
for (int i = 0; i < 4; i++) {
    pool.submit(() -> calculatePrimes(...));
}
```