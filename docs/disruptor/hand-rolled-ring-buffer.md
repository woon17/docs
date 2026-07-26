# Hand-Rolled Lock-Free Ring Buffer

A from-scratch MPSC (multi-producer, single-consumer) ring buffer that
illustrates the core mechanic behind the LMAX Disruptor — no external
`disruptor` library, no locks anywhere. Source: `performance/ringbuffer/RingBuffer.java`
and `performance/ringbuffer/RingBufferDemo.java` (3 producer threads publish, 1
consumer thread drains).

This complements [Lock-free & CAS](lock-free-cas.md) with a concrete,
line-by-line implementation instead of API-level pseudocode.

## Benchmark

3 producers x 2M events each, capacity 65536:

```
consumed 6,000,000 events in 0.600s (10,007,344 events/sec)
latency avg=6386666ns max=7995750ns
```

Latency is high here because producers outrun the consumer and repeatedly
fill the 64K-slot buffer — that's backpressure wait time, not per-operation
cost.

## The problem it solves

A normal thread-safe queue (`ArrayBlockingQueue`, `synchronized` list) takes
a lock on every `add()`/`take()`, even with no real contention. Lock cost
isn't just the acquisition — a blocked thread gets parked by the OS and
rescheduled later, microseconds, versus nanosecond CPU speed.

This buffer replaces "only one thread may touch shared state at a time"
(mutual exclusion) with "every thread computes a unique index up front, then
owns that index exclusively" (partitioning). Once ownership is unique,
there's nothing left to coordinate — you don't need a lock to protect a
memory address only one thread will ever write.

## Data structures

```java
private final Object[] buffer;               // the ring, size = capacity
private final int mask;                      // capacity - 1, e.g. 65536 -> 0xFFFF
private final AtomicLong claimSequence;       // monotonically increasing "ticket number"
private final AtomicLong consumeSequence;     // last slot the consumer fully finished
private final AtomicIntegerArray availableLap; // per-slot "which lap published this"
```

`capacity` must be a power of two so `seq & mask` computes `seq % capacity`
in one cycle instead of a division.

`seq` is a never-wrapping 64-bit counter (producer 1 gets seq 0, next
winner gets seq 1, forever increasing). The **slot** a seq lives in is
`seq & mask`, which does wrap (seq 0 and seq 65536 both map to slot 0). This
distinction — ever-increasing ticket vs. wrapping array index — is the whole
trick.

## Producer path

### 1. `claim()` — get a unique ticket

```java
long seq = claimSequence.incrementAndGet();
```

Compiles to a single hardware atomic instruction (`LOCK XADD` on x86, LL-SC
loop on ARM). No kernel involvement, no thread blocks. Three producers
calling this concurrently just serializes the increment at the
cache-coherence level (the cache line bounces between cores via MESI) —
each producer walks away with a **distinct** `seq`. This is the only point
where producers contend with each other; everything after is private to
whichever thread got that `seq`.

### 2. Backpressure gate — still inside `claim()`

```java
long wrapPoint = seq - capacity;
while (consumeSequence.get() < wrapPoint) {
    Thread.onSpinWait();
}
```

Say capacity is 4 and you just claimed seq=41. Slot = 41 & 3 = 1. But seq=37
also mapped to slot 1. If the consumer hasn't finished reading seq=37 yet
and you write into slot 1 now, you've stomped on data the consumer is
mid-read on — a live data race.

`wrapPoint = seq - capacity` says "don't proceed until the consumer has
fully consumed seq 37." If the consumer is behind, the producer spins
(`Thread.onSpinWait()` — a CPU hint, cheaper than a plain busy loop) until it
catches up. This is what makes the next step's "I own this slot exclusively"
claim actually true.

### 3. `set()` — write the payload

```java
buffer[(int) (seq & mask)] = value;
```

A completely plain, unsynchronized array store — no CAS, no volatile, no
lock. Safe only because the wrap-point gate guarantees no other thread is
touching this slot right now. This is the entire performance payoff: the
expensive part (writing your data) costs exactly what a plain array write
costs, because coordination already happened cheaply in `claim()`.

### 4. `publish()` — make it visible to the consumer

```java
availableLap.set((int) (seq & mask), lapOf(seq));
```

Why isn't step 3 enough alone? The consumer runs on a different core.
Without an explicit signal, the JVM/CPU may reorder or delay-propagate the
plain write from step 3 — nothing forces it to become visible "in time" or
"in order" to the consumer.

`AtomicIntegerArray.set()` is a **volatile** write (JLS 17.4.5): if a
volatile write W happens-before a volatile read R that observes it,
everything the writing thread did before W — including plain writes — is
guaranteed visible to the reading thread after R.

So the pair (plain write, then volatile write) on the producer side, matched
with (volatile read, then plain read) on the consumer side, acts as a
release/acquire fence — the same visibility contract a mutex's
`unlock()`/`lock()` gives, without ever touching the OS scheduler. This is
why `get()` on the consumer side is allowed to be a plain read: the fence
already happened.

### Why a lap counter, not a boolean flag

The buffer only has 65536 slots but the demo pushes 6,000,000 events through
it — each slot gets reused ~91 times. If slot 100 held lap 3's data behind a
boolean "ready" flag, once lap 4 overwrites slot 100, the consumer can't
tell "fresh lap-4 data" from "stale lap-3 data still flagged ready." A
boolean has no way to distinguish generations.

```java
private int lapOf(long seq) { return (int) (seq / capacity); }
```

`lapOf(seq)` is which trip-around-the-buffer this seq belongs to (seq
0..65535 = lap 0, seq 65536..131071 = lap 1, ...). `isAvailable(seq)` checks
`availableLap[slot] == lapOf(seq)` — only true if *this exact* seq's publish
is the most recent one, not an earlier lap's stale flag. This is a bug that
literally cannot show up in a small test (`events < capacity`) — it only
appears once you exceed one full lap, which is exactly the regime the
benchmark deliberately runs in (2M events per producer vs. 64K capacity).

## Consumer path

```java
if (!ringBuffer.isAvailable(next)) { Thread.onSpinWait(); continue; }  // volatile read
Event event = ringBuffer.get(next);                                    // plain read, safe due to the fence above
// ... process event ...
ringBuffer.markConsumed(next);                                         // consumeSequence.set(seq)
next++;
```

The consumer is single-threaded, so it needs zero synchronization among
"itself" — just the one release/acquire pair with producers described
above. `markConsumed` writes `consumeSequence`, which unblocks producers
spinning in the wrap-point gate. `AtomicLong` here is used purely for its
volatile semantics (visibility to producer spin-loops), not for any atomic
read-modify-write — only the consumer thread ever writes it, so a plain
`volatile long` would behave identically.

## Concrete walkthrough (capacity = 4, mask = 3)

| seq | slot (seq & 3) | lap (seq / 4) | what happens |
|---|---|---|---|
| 0 | 0 | 0 | producer claims, writes, publishes lap 0 into slot 0 |
| 1 | 1 | 0 | same, slot 1 |
| 2 | 2 | 0 | same, slot 2 |
| 3 | 3 | 0 | same, slot 3 — buffer now full |
| 4 | 0 | 1 | wrapPoint = 4-4 = 0 → producer must wait until `consumeSequence >= 0`. Once it has, this producer overwrites slot 0 and publishes **lap 1** |

If the consumer were still slow and hadn't consumed seq 0 yet, the producer
claiming seq=4 spins at the wrap-point gate rather than clobbering slot 0.

## How to use it

```java
RingBuffer<MyEvent> ring = new RingBuffer<>(1 << 16); // capacity must be power of 2

// producer thread(s):
long seq = ring.claim();
ring.set(seq, new MyEvent(...));
ring.publish(seq);

// consumer thread (exactly one):
long next = 0;
while (running) {
    if (!ring.isAvailable(next)) { Thread.onSpinWait(); continue; }
    MyEvent event = ring.get(next);
    // ... process event ...
    ring.markConsumed(next);
    next++;
}
```

Rules that must hold or it breaks:

- **Exactly one consumer.** Multiple consumers racing on `next`/`markConsumed`
  would violate the single-writer assumption on `consumeSequence`.
- **Any number of producers**, but each must do `claim()` → `set()` →
  `publish()` in that order for that exact `seq` every time — skipping
  `publish()` leaves that slot permanently unavailable and stalls the
  consumer forever.
- **Consumer must process seqs strictly in order** (0, 1, 2, ...) —
  `isAvailable`/`get` are keyed by the exact expected `seq`.

The correctness check in `RingBufferDemo` (`event.producerSeq() != prev + 1`
→ throw) exists specifically to catch out-of-order/torn-publish failure
modes — worth keeping in a benchmark rather than measuring throughput blind.

## What breaks if you remove any one piece

| Remove | Failure mode |
|---|---|
| `incrementAndGet` → plain `++` | Two producers get the same `seq`, silently overwrite each other's event |
| `AtomicIntegerArray` → plain `int[]` for `availableLap` | Consumer can observe the flag before observing the buffer write (reordering) → reads stale/zeroed data, a "torn publish" |
| Lap counter → boolean flag | Consumer reads stale data from a previous wrap after ~65536 events |
| Wrap-point gate in `claim()` | Producer overwrites a slot the consumer hasn't read yet → data race |

## Next steps

- Compare throughput against `ArrayBlockingQueue` (lock-based baseline)
- Compare `Thread.onSpinWait()` vs busy-spin vs `LockSupport.parkNanos` wait
  strategies
- Try the real `com.lmax:disruptor` library for the production API surface

## Self-test

??? question "Why avoid locks at all?"
    Locks block threads → OS parks/reschedules them → microseconds lost.
    Lock-free ops resolve at the CPU cache-coherence level → nanoseconds.

??? question "What's the core trick replacing mutual exclusion?"
    Partitioning. Each producer gets a unique index via one atomic op, then
    owns that slot exclusively — nothing left to coordinate after that.

??? question "What does claimSequence.incrementAndGet() actually do on hardware?"
    One `LOCK XADD` instruction (x86). No kernel involvement. Concurrent
    calls serialize at the cache-line level; each thread gets a distinct
    number.

??? question "Why is seq (ticket) different from slot (array index)?"
    `seq` grows forever (0,1,2,3...). `slot = seq & mask` wraps (seq 0 and
    seq 65536 both → slot 0 if capacity=65536). Ticket = identity, slot =
    storage location.

??? question "Why is buffer[seq & mask] = value a plain unsynchronized write, and why is that safe?"
    Because the wrap-point gate already guarantees no other thread is
    touching that slot right now. Coordination happened earlier in
    `claim()`, so the actual write is free.

??? question "Why isn't the plain write to buffer[] enough on its own?"
    JVM/CPU can reorder or delay-propagate plain writes across cores —
    there's no guarantee the consumer sees it in time or in order.

??? question "How does publish() fix the visibility problem?"
    `availableLap.set(idx, lap)` is a volatile write (JLS 17.4.5). A
    volatile write, followed by a volatile read that observes it, makes
    everything before the write visible — the same contract a lock's
    unlock/lock gives, without touching the OS.

??? question "Why not just a boolean 'ready' flag instead of a lap counter?"
    Slots get reused (65536 slots, millions of events). A boolean can't
    tell "fresh data from this lap" apart from "a stale flag left over from
    a previous lap."

??? question "What are the 3 usage rules?"
    Exactly one consumer. Any number of producers, but always
    claim→set→publish in order for each seq. Consumer must process seqs
    strictly in order.

## Further reading

- [Lock-free & CAS](lock-free-cas.md)
- [LMAX Disruptor overview](index.md)
- [Aeron Ring Buffer: Performance & Threading](../aeron/ring-buffer.md) — same
  ring buffer idea, applied to Aeron's built-in implementations
