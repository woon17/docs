# Lock-free algorithms & CAS

This page explains lock-free programming and the Compare-And-Swap (CAS) primitive. It's written for developers learning how the Disruptor achieves high throughput without traditional locks.

## What is "lock-free"?

- Lock-free algorithms avoid mutual-exclusion locks (no synchronized blocks or mutexes) for their core coordination. They rely on atomic operations so at least one thread makes progress at any time.
- Benefits: no thread-blocking, reduced context-switch overhead, often lower latency.
- Downsides: more complex reasoning, potential for livelock or starvation under contention.

## Compare-And-Swap (CAS)

CAS is an atomic CPU-supported primitive that updates a memory location only if it has an expected value.

Pseudo-signature:

```
boolean compareAndSwap(address, expectedValue, newValue)
```

It atomically does:

- if (*address == expectedValue) { *address = newValue; return true; }
- else return false;

In Java this is exposed through `Atomic*` classes (e.g. `AtomicInteger.compareAndSet`).

### Simple Java example (AtomicInteger increment)

```java
import java.util.concurrent.atomic.AtomicInteger;

public class CasIncrement {
    private final AtomicInteger value = new AtomicInteger(0);

    public void increment() {
        int oldVal;
        int newVal;
        do {
            oldVal = value.get();
            newVal = oldVal + 1;
        } while (!value.compareAndSet(oldVal, newVal));
    }
}
```

Notes:
- The loop retries until the CAS succeeds.
- This is lock-free: threads may retry, but none block on locks.

## ABA problem and mitigation

- ABA: a location holds value A, a thread reads A, other thread changes A->B->A, CAS succeeds but the state changed in between.
- Mitigations:
  - Use versioned references (pair value + stamp). Java provides `AtomicStampedReference`.
  - Use hazard pointers or epoch-based reclamation for complex data-structure safe reclamation.

Example with `AtomicStampedReference`:

```java
import java.util.concurrent.atomic.AtomicStampedReference;

AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 0);
int[] stampHolder = new int[1];
String current = ref.get(stampHolder);
int stamp = stampHolder[0];
boolean ok = ref.compareAndSet(current, "X", stamp, stamp+1);
```

## Use-cases in Disruptor

- Sequencers and cursor positions use atomic variables and ordered writes to publish sequences without locks.
- RingBuffer slots are preallocated; CAS is used for claims and publications in some implementations or for coordination when multiple producers exist.

## Performance tips

- Keep CAS loops short and minimize the amount of work between read and CAS.
- Use exponential/backoff waits if contention is high.
- Prefer striped or partitioned data structures to reduce contention.

## References

- LMAX Disruptor: https://github.com/LMAX-Exchange/disruptor
- Atomic classes: https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html
- ABA problem and memory reclamation: Harris' papers and Michael & Scott.
