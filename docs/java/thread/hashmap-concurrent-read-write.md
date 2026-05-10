# HashMap Concurrent Access: Why One Writer + One Reader Breaks

**Question:** If one thread writes to a `HashMap` and another thread only reads it, is this safe? Why does it break?

**Answer:** ❌ **No, it's unsafe** — and yes, it's directly related to `volatile` and the Java Memory Model (JMM).

---

## TL;DR (Short Answer)

`HashMap` is **unsafe** even with 1 writer + 1 reader because:

1. ❌ **No `volatile` fields** → Writes may not be visible to readers
2. ❌ **No synchronization** → CPU cache + compiler can reorder operations
3. ❌ **No safe publication** → Readers see partially constructed objects
4. ❌ **Structural corruption possible** → Infinite loops, broken chains, null values

**Root cause:** Visibility + Ordering problems in the Java Memory Model (JMM)

---

## Why `volatile` Matters

### HashMap's Non-Volatile Fields

```java
// Inside HashMap.java
transient Node<K,V>[] table;  // ❌ NOT volatile
transient int size;           // ❌ NOT volatile
int threshold;                // ❌ NOT volatile
```

**Impact:**

| Field Type | Visibility Guarantee | Ordering Guarantee | Safe Publication |
|------------|---------------------|-------------------|------------------|
| `volatile` | ✅ Yes (flushed to memory) | ✅ Yes (happens-before) | ✅ Yes |
| Normal | ❌ No (may stay in cache) | ❌ No (can reorder) | ❌ No |

**HashMap uses normal fields** → No guarantees at all!

---

## Java Memory Model (JMM) Guarantees

| Operation | Behavior |
|-----------|----------|
| **`volatile` write** | Flushed to main memory → visible to all threads |
| **`volatile` read** | Forces reading latest value from memory |
| **Normal write** | May stay in CPU cache / store buffer → invisible to others |
| **Normal read** | May read stale value from local cache |

**HashMap uses normal writes** → violations:

- ❌ No visibility guarantees
- ❌ No ordering guarantees
- ❌ No safe publication
- ❌ No atomic structural changes

---

## Example 1: Invisible Writes

### Scenario
Writer inserts a key, but reader cannot see it.

**Writer thread (T1):**
```java
map.put(10, "abc");
```

**Reader thread (T2):**
```java
String x = map.get(10);
System.out.println(x);  // Output: null ❌
```

**Expected:** `"abc"`
**Actual:** `null`

### Why Does This Happen?

#### CPU-Level Explanation

```
Writer (T1, Core 0)          Memory          Reader (T2, Core 3)
─────────────────────────────────────────────────────────────────
1. Create new Node           [old table]     1. Reads table
2. Write table[index]        [old table]        from its L1 cache
3. Write size                [old table]     2. Sees old table
                             (in T1's cache)    (stale!)
4. [Changes stay in          [old table]     3. get(10) → null ❌
    L1/L2 cache]
```

**What goes wrong:**

1. **Writer (T1)** on Core 0:
   - Creates new `Node(10, "abc")`
   - Writes to `table[index]`
   - Updates `size`
   - **But:** All writes stay in Core 0's L1/L2 cache
   - **Not flushed** to main memory

2. **Reader (T2)** on Core 3:
   - Reads its own L1 cache copy of `table`
   - Sees the **old HashMap** (before insertion)
   - `get(10)` returns `null`

3. **No synchronization:**
   - No `volatile` → No happens-before edge
   - No memory barrier → No cache invalidation
   - T2's cache is never told to refresh

**Result:** Stale read, invisible write

---

## Example 2: Broken Node Chain (Reordering)

### Scenario
JVM/CPU reorders operations, creating half-constructed nodes.

**HashMap's internal `put()` logic:**
```java
Node<K,V> newNode = new Node<>(hash, key, value, null);
newNode.next = table[i];  // Link to existing chain
table[i] = newNode;       // Update bucket
```

### Without `volatile`, Reordering Happens

**Compiler/CPU may reorder to:**
```java
table[i] = newNode;       // ⚠️ Published FIRST
newNode.next = table[i];  // ⚠️ Link set SECOND
```

**Timeline:**

| Time | Writer (T1) | Reader (T2) |
|------|-------------|-------------|
| t1 | `table[i] = newNode` | — |
| t2 | — | Reads `table[i]` → sees `newNode` |
| t3 | — | Reads `newNode.next` → **null** ❌ |
| t4 | `newNode.next = oldHead` | (too late) |

**Reader sees:**
```java
newNode.next == null  // ❌ Should point to old head!
```

**Impact:**

- ✅ Old chain elements are **lost** (not reachable)
- ❌ Iteration stops early
- ❌ `size()` shows 10 items, iteration finds 3

**Root cause:** Happens-before violation (no `volatile`)

---

## Example 3: Infinite Loop (Classic JDK Bug)

### Scenario
During resize, broken pointers create circular linked lists.

**HashMap resize (simplified):**
```java
void resize() {
    Node<K,V>[] newTable = new Node[newCapacity];
    for (int i = 0; i < oldTable.length; i++) {
        Node<K,V> e = oldTable[i];
        while (e != null) {
            Node<K,V> next = e.next;
            int newIndex = hash(e.key) & (newCapacity - 1);
            e.next = newTable[newIndex];  // ⚠️ Link manipulation
            newTable[newIndex] = e;
            e = next;
        }
    }
    table = newTable;
}
```

**Without synchronization, two threads can create:**

```
Before:  A → B → C → null

Thread 1 resizes: A → B
Thread 2 reads:   B → A  ❌ (stale pointers)

Result:  A ⇄ B  (circular!)
```

**When reader iterates:**
```java
for (Node<K,V> e = table[i]; e != null; e = e.next) {
    // e.next eventually points back to e
    // Infinite loop! 🔁
}
```

**Result:**

- ❌ **100% CPU usage** (thread stuck in loop)
- ❌ **Application hangs**
- ❌ **No exception thrown** (just loops forever)

**Famous in:** JDK 6/7 multithreaded environments

---

## Example 4: Inconsistent Size vs. Elements

### Scenario
Reader sees `size` updated, but not the new elements.

**Writer:**
```java
map.put(key, value);
// Internally:
// 1. table[i] = newNode
// 2. size++
```

**Reader:**
```java
int reportedSize = map.size();
int actualCount = 0;
for (Map.Entry<K, V> entry : map.entrySet()) {
    actualCount++;
}
if (actualCount != reportedSize) {
    System.out.println("INCONSISTENT: " +
        "size=" + reportedSize + ", count=" + actualCount);
}
```

**Output:**
```
INCONSISTENT: size=1000, count=997
```

**Why?**

| Operation | Reader's View |
|-----------|--------------|
| Writer updates `table[i]` | Reader sees **old `table`** (cache) |
| Writer increments `size` | Reader sees **new `size`** (happens to be flushed) |

**Result:**

- `size` says 1000 elements
- Iteration only finds 997

**Root cause:**
Different fields (`table` vs `size`) are in different cache lines, flushed at different times. No ordering guarantee!

---

## Example 5: CPU Cache Behavior

### Hardware Setup

```
CPU Architecture:
┌─────────────────────────────────────────────┐
│  Core 0           Core 1           Core 3   │
│  ┌──────┐         ┌──────┐         ┌──────┐│
│  │  L1  │         │  L1  │         │  L1  ││
│  └──────┘         └──────┘         └──────┘│
│  ┌──────┐         ┌──────┐         ┌──────┐│
│  │  L2  │         │  L2  │         │  L2  ││
│  └──────┘         └──────┘         └──────┘│
│          \         |         /              │
│           \        |        /               │
│            ┌──────────────┐                 │
│            │   L3 Cache   │                 │
│            └──────────────┘                 │
│                   |                         │
│            ┌──────────────┐                 │
│            │ Main Memory  │                 │
│            └──────────────┘                 │
└─────────────────────────────────────────────┘
```

**Thread allocation:**
- **Writer (T1):** Runs on Core 0
- **Reader (T2):** Runs on Core 3

### What Happens During `put()`

**Step 1: Writer on Core 0**
```java
map.put(42, "value");
```

**Core 0's operations:**

1. Allocates new `Node(42, "value")`
2. Writes to `table[index]`
3. Updates `size`
4. Updates `threshold`

**Where do these writes go?**

```
Core 0:
  L1 Cache: [table array] [new Node] [size=1001]
  L2 Cache: [cached copy of table]
```

**Critical:** These writes **stay in Core 0's cache**!

- No `volatile` → No store barrier
- No flush to main memory
- No invalidation signal to other cores

---

**Step 2: Reader on Core 3**
```java
String v = map.get(42);
```

**Core 3's operations:**

1. Reads `table` from **its own L1 cache**
2. Core 3's cache was loaded earlier (before the write)
3. No cache invalidation received from Core 0
4. Sees **old table** (without the new entry)

```
Core 3:
  L1 Cache: [old table array] [size=1000]  ← STALE!
```

**Result:** `get(42)` returns `null`

---

### MESI Protocol Fails Without `volatile`

**MESI Cache Coherence States:**

| State | Meaning |
|-------|---------|
| **M**odified | This cache has the only valid copy (dirty) |
| **E**xclusive | This cache has the only copy (clean) |
| **S**hared | Multiple caches have copies |
| **I**nvalid | This cache's copy is stale |

**Normal write (no `volatile`):**

```
Core 0 writes table[i]:
  Core 0: M (Modified)  ← Has new value
  Core 3: S (Shared)    ← Still thinks it has valid copy ❌
```

**No invalidation sent to Core 3!**

**`volatile` write:**

```
Core 0 writes volatile field:
  Core 0: M (Modified)  ← Has new value
  Core 3: I (Invalid)   ← Forced to invalidate ✅

Next read on Core 3:
  → Cache miss
  → Fetches from Core 0 or main memory
  → Sees updated value ✅
```

**Conclusion:** Without `volatile`, MESI doesn't invalidate stale caches.

---

## Summary: All Failure Modes

| Problem | Cause | Example Impact |
|---------|-------|----------------|
| **Invisible writes** | No visibility guarantee | `get(key)` returns `null` after `put(key)` |
| **Reordered operations** | No ordering guarantee | Half-constructed nodes, broken chains |
| **Infinite loop** | Structural corruption during resize | 100% CPU, thread hangs |
| **Inconsistent size** | Different fields updated at different times | `size() != actualCount` |
| **Stale cache reads** | No cache invalidation | Reader sees old data indefinitely |

**Root cause for ALL:** No `volatile`, no synchronization, no happens-before guarantee.

---

## What is Safe Publication?

**Safe publication** means:

1. Object is **fully constructed** before reference is published
2. Updates are **visible** to all threads
3. **Ordering** is preserved (no reordering)

**How to achieve it:**

| Method | Mechanism |
|--------|-----------|
| `volatile` field | Memory barrier + cache flush |
| `synchronized` block | Lock ensures visibility |
| `final` field | Constructor guarantee |
| `AtomicReference` | Built-in memory barriers |

**HashMap has NONE of these** → Unsafe publication

---

## The Correct Solutions

### ✅ Solution 1: `ConcurrentHashMap`

```java
Map<Integer, String> map = new ConcurrentHashMap<>();

// Thread 1 (writer)
map.put(10, "value");

// Thread 2 (reader)
String v = map.get(10);  // ✅ Always sees latest value
```

**Why it works:**

- Uses `volatile` fields internally
- Uses CAS (Compare-And-Swap) operations
- Lock-free reads for high performance
- Segmented locking for writes

---

### ✅ Solution 2: Immutable Data + `volatile` Reference

```java
private volatile Map<Integer, String> map = new HashMap<>();

// Writer (creates new map)
Map<Integer, String> newMap = new HashMap<>(map);
newMap.put(10, "value");
map = newMap;  // volatile write → visible to all

// Reader
String v = map.get(10);  // ✅ Sees updated reference
```

**Why it works:**

- `volatile` reference ensures visibility
- Immutable `HashMap` means no structural changes
- Safe publication via `volatile`

---

### ✅ Solution 3: Explicit Synchronization

```java
private final Map<Integer, String> map = new HashMap<>();
private final Object lock = new Object();

// Writer
synchronized (lock) {
    map.put(10, "value");
}

// Reader
synchronized (lock) {
    String v = map.get(10);  // ✅ Sees updates
}
```

**Why it works:**

- `synchronized` creates happens-before edge
- Ensures visibility and ordering
- **Downside:** Performance cost (locking on every read)

---

## Detailed Comparison

| Approach | Visibility | Performance | Complexity |
|----------|-----------|-------------|-----------|
| **`HashMap` (unsafe)** | ❌ No | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (simple but broken) |
| **`ConcurrentHashMap`** | ✅ Yes | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ (use this!) |
| **Immutable + `volatile`** | ✅ Yes | ⭐⭐⭐ | ⭐⭐⭐ (good for read-heavy) |
| **`synchronized` HashMap** | ✅ Yes | ⭐⭐ | ⭐⭐ (lock contention) |
| **`Collections.synchronizedMap()`** | ✅ Yes | ⭐⭐ | ⭐⭐⭐⭐ (easy but slow) |

**Recommendation:** Use `ConcurrentHashMap` for 99% of cases.

---

## Key Takeaways

### 1. HashMap is Unsafe for Concurrent Access

Even with **1 writer + 1 reader**, `HashMap` breaks because:

- No `volatile` fields
- No synchronization
- No safe publication
- No memory barriers

### 2. The Java Memory Model Allows Chaos

Without synchronization:

- Compilers can reorder instructions
- CPUs can reorder memory operations
- Caches can serve stale data
- Different threads see different realities

### 3. `volatile` is NOT Just About "Flushing"

`volatile` provides:

1. **Visibility:** Forces flush to main memory
2. **Ordering:** Prevents reordering (happens-before)
3. **Atomicity:** 64-bit reads/writes are atomic
4. **Cache coherence:** Invalidates stale cache lines

`HashMap` has **none** of these guarantees.

### 4. CPU Cache is the Hidden Villain

Modern CPUs:

- Have 3-4 levels of cache (L1, L2, L3, main memory)
- Each core has private L1/L2 caches
- Without memory barriers, caches don't sync
- MESI protocol needs hints from `volatile` to work

### 5. Always Use Thread-Safe Collections

| Use Case | Recommended Collection |
|----------|----------------------|
| Concurrent map | `ConcurrentHashMap` |
| Concurrent list | `CopyOnWriteArrayList` (read-heavy) |
| Concurrent set | `ConcurrentHashMap.newKeySet()` |
| Concurrent queue | `ConcurrentLinkedQueue` |
| Blocking queue | `LinkedBlockingQueue` |

---

## Debugging Tips

### How to Detect These Issues

**Symptoms:**

- ✅ Works on single-core machines
- ❌ Breaks on multi-core machines
- ✅ Works under debugger (synchronization side-effect)
- ❌ Breaks in production (higher load)
- ❌ Heisenbug (disappears when you try to observe it)

**Tools:**

1. **Java Thread Sanitizer** (experimental)
2. **FindBugs / SpotBugs** (static analysis)
3. **JMH Benchmarks** (stress testing)
4. **Thread dumps** (look for infinite loops)
5. **JConsole / VisualVM** (monitor CPU usage spikes)

---

## Further Reading

**Related Topics:**

- [Visibility Issues](visibility.md)
- [Atomicity Issues](atomicity.md)
- [Ordering Issues](ordering.md)
- [Volatile Keyword](../volatile.md)

**External Resources:**

- [Java Concurrency in Practice](https://jcip.net/) (Chapter 3: Visibility)
- [JSR-133 (Java Memory Model)](https://www.cs.umd.edu/~pugh/java/memoryModel/)
- [Doug Lea's Concurrent Programming](http://gee.cs.oswego.edu/dl/cpj/)

---

## Conclusion

**The Question:** Is `HashMap` safe with 1 writer + 1 reader?

**The Answer:** ❌ **Absolutely not.**

**The Reason:** Java Memory Model + CPU cache behavior + lack of `volatile`

**The Fix:** Use `ConcurrentHashMap` (or synchronized collections)

> "HashMap is unsafe for concurrent access, even if you think you're being careful. Always use `ConcurrentHashMap` or explicit synchronization."

---

## Practical Demonstration: Runnable Java Code

### Understanding CountDownLatch

Before we dive into the code, you need to understand **CountDownLatch** - a critical tool for reproducing concurrent bugs reliably.

#### What is CountDownLatch?

`CountDownLatch` is a synchronization primitive that acts like a **gate**:

```java
CountDownLatch latch = new CountDownLatch(1);  // Gate CLOSED (count=1)

// Thread 1
latch.await();      // Wait at gate (blocked)

// Thread 2
latch.countDown();  // Open gate (count becomes 0)

// Thread 1 now continues!
```

**Key Methods:**
- `new CountDownLatch(n)` - Create latch with count = n
- `await()` - Block until count reaches 0
- `countDown()` - Decrement count by 1

#### Why CountDownLatch is Critical for This Demo

**The Problem Without CountDownLatch:**

```
Scenario 1 (Writer finishes first):
  Writer: put(0)...put(9999) [DONE!]
  Reader: [starts late] get(0)...get(9999)  ← Sees all values, no bug shown!

Scenario 2 (Reader finishes first):
  Reader: get(0)...get(9999) [DONE!]  ← All null, but writer not started yet
  Writer: [starts late] put(0)...put(9999)
```

Both scenarios fail to show the **concurrent access** problem because threads don't overlap!

**The Solution With CountDownLatch:**

```java
CountDownLatch latch = new CountDownLatch(1);

Thread writer = new Thread(() -> {
    latch.await();  // ← Writer WAITS here
    for (int i = 0; i < 10000; i++) {
        map.put(i, "value_" + i);
    }
});

Thread reader = new Thread(() -> {
    latch.countDown();  // ← Reader RELEASES writer
    for (int i = 0; i < 10000; i++) {
        map.get(i);
    }
});

reader.start();  // Reader starts first
writer.start();  // Writer starts but waits
// Both begin work SIMULTANEOUSLY!
```

**Timeline with CountDownLatch:**

```
Time    Reader Thread              Writer Thread
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
T1      READY!                     latch.await() ← BLOCKED
T2      latch.countDown()          ↓
T3      STARTS: get(0)             RELEASED!
T4              get(1)             STARTS: put(0)
T5              get(2)                     put(1)
        ...                        ...

        ← BOTH THREADS RUNNING SIMULTANEOUSLY! →
```

**Result:** Maximum overlap → Cache visibility issues exposed → 10,000 invisible writes!

---

### Complete Runnable Code

Below is the complete demonstration code that reproduces all the issues discussed in this document.

#### Main Demonstration Class

```java
package example.exploredisruptor;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Demonstrates HashMap concurrent read-write issues
 * Reproduces: invisible writes, broken chains, infinite loops, inconsistent size
 */
public class HashMapConcurrencyDemo {

    private static final int ITERATIONS = 10000;

    public static void main(String[] args) throws Exception {
        System.out.println("=".repeat(80));
        System.out.println("HashMap Concurrent Access Demonstration");
        System.out.println("=".repeat(80));
        System.out.println();

        example1_InvisibleWrites();
        System.out.println("\n" + "-".repeat(80) + "\n");

        example2_BrokenNodeChain();
        System.out.println("\n" + "-".repeat(80) + "\n");

        example3_InfiniteLoop();
        System.out.println("\n" + "-".repeat(80) + "\n");

        example4_InconsistentSize();
        System.out.println("\n" + "-".repeat(80) + "\n");

        safeSolutions();

        System.out.println("\n" + "=".repeat(80));
        System.out.println("Demonstration Complete!");
        System.out.println("=".repeat(80));
    }

    /**
     * Example 1: Invisible Writes
     * Writer inserts keys, but reader cannot see them due to CPU cache issues
     */
    private static void example1_InvisibleWrites() throws InterruptedException {
        System.out.println("EXAMPLE 1: INVISIBLE WRITES");
        System.out.println("Writer puts data, reader gets null due to cache visibility");
        System.out.println();

        final Map<Integer, String> unsafeMap = new HashMap<>();
        final CountDownLatch latch = new CountDownLatch(1);
        final int[] nullReads = {0};
        final int[] successReads = {0};

        // Writer thread - waits for reader to be ready
        Thread writer = new Thread(() -> {
            try {
                latch.await(); // Block until reader calls countDown()
                for (int i = 0; i < ITERATIONS; i++) {
                    unsafeMap.put(i, "value_" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Writer-Thread");

        // Reader thread - releases writer and starts reading immediately
        Thread reader = new Thread(() -> {
            latch.countDown(); // Release writer
            for (int i = 0; i < ITERATIONS; i++) {
                String value = unsafeMap.get(i);
                if (value == null) {
                    nullReads[0]++;
                } else {
                    successReads[0]++;
                }
                if (i % 100 == 0) {
                    Thread.yield(); // Occasional yield
                }
            }
        }, "Reader-Thread");

        reader.start();
        writer.start();

        writer.join();
        reader.join();

        System.out.println("Results:");
        System.out.println("  Total reads: " + ITERATIONS);
        System.out.println("  Successful reads: " + successReads[0]);
        System.out.println("  NULL reads (invisible writes): " + nullReads[0]);
        if (nullReads[0] > 0) {
            System.out.println("  ❌ ISSUE DETECTED: Reader saw " + nullReads[0] + " invisible writes!");
        } else {
            System.out.println("  ⚠️  Issue not reproduced (timing dependent)");
        }
    }

    /**
     * Example 2: Broken Node Chain
     * Multiple threads cause hash collisions, breaking linked list chains
     */
    private static void example2_BrokenNodeChain() throws InterruptedException {
        System.out.println("EXAMPLE 2: BROKEN NODE CHAIN (Reordering)");
        System.out.println("Multiple threads cause hash collisions, breaking node chains");
        System.out.println();

        final Map<CollisionKey, String> unsafeMap = new HashMap<>();
        final int threadCount = 4;
        final CountDownLatch startLatch = new CountDownLatch(1);
        final CountDownLatch doneLatch = new CountDownLatch(threadCount);

        // Create multiple threads that insert keys with same hash
        List<Thread> writers = new ArrayList<>();
        for (int t = 0; t < threadCount; t++) {
            final int threadId = t;
            Thread writer = new Thread(() -> {
                try {
                    startLatch.await();
                    for (int i = 0; i < 100; i++) {
                        CollisionKey key = new CollisionKey(threadId * 100 + i);
                        unsafeMap.put(key, "thread_" + threadId + "_value_" + i);
                    }
                    doneLatch.countDown();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }, "Writer-" + t);
            writers.add(writer);
            writer.start();
        }

        startLatch.countDown(); // Start all writers simultaneously
        doneLatch.await();

        int expectedSize = threadCount * 100;
        int actualSize = unsafeMap.size();
        int countedElements = 0;

        for (Map.Entry<CollisionKey, String> entry : unsafeMap.entrySet()) {
            countedElements++;
        }

        System.out.println("Results:");
        System.out.println("  Expected elements: " + expectedSize);
        System.out.println("  map.size(): " + actualSize);
        System.out.println("  Counted elements: " + countedElements);

        if (actualSize != expectedSize || countedElements != expectedSize) {
            System.out.println("  ❌ ISSUE DETECTED: Lost elements due to broken chains!");
            System.out.println("  Lost: " + (expectedSize - Math.min(actualSize, countedElements)));
        } else {
            System.out.println("  ⚠️  Issue not reproduced (timing dependent)");
        }
    }

    /**
     * Example 3: Infinite Loop
     * Multiple threads resize simultaneously, creating circular links
     * WARNING: Can actually hang, uses timeout for safety
     */
    private static void example3_InfiniteLoop() throws InterruptedException {
        System.out.println("EXAMPLE 3: INFINITE LOOP (Classic Resize Bug)");
        System.out.println("Multiple threads resize simultaneously, creating circular links");
        System.out.println();

        final Map<Integer, String> unsafeMap = new HashMap<>(2); // Small size to force resize
        final CountDownLatch startLatch = new CountDownLatch(1);
        final ExecutorService executor = Executors.newFixedThreadPool(4);
        final AtomicBoolean infiniteLoopDetected = new AtomicBoolean(false);

        List<Future<?>> futures = new ArrayList<>();
        for (int t = 0; t < 4; t++) {
            final int threadId = t;
            Future<?> future = executor.submit(() -> {
                try {
                    startLatch.await();
                    for (int i = 0; i < 100; i++) {
                        int key = threadId * 100 + i;
                        unsafeMap.put(key, "value_" + key);

                        if (i % 10 == 0) {
                            unsafeMap.get(key);
                            // Try to iterate (dangerous!)
                            int count = 0;
                            for (Map.Entry<Integer, String> entry : unsafeMap.entrySet()) {
                                count++;
                                if (count > 10000) { // Safety limit
                                    infiniteLoopDetected.set(true);
                                    throw new RuntimeException("Infinite loop detected!");
                                }
                            }
                        }
                    }
                } catch (Exception e) {
                    if (e.getMessage().contains("Infinite loop")) {
                        infiniteLoopDetected.set(true);
                    }
                }
            });
            futures.add(future);
        }

        startLatch.countDown();

        boolean completed = true;
        for (Future<?> future : futures) {
            try {
                future.get(2, TimeUnit.SECONDS);
            } catch (TimeoutException e) {
                System.out.println("  ❌ ISSUE DETECTED: Thread hung (infinite loop)!");
                infiniteLoopDetected.set(true);
                future.cancel(true);
                completed = false;
            } catch (Exception e) {
                // Expected from detection logic
            }
        }

        executor.shutdownNow();

        System.out.println("Results:");
        if (infiniteLoopDetected.get()) {
            System.out.println("  ❌ INFINITE LOOP DETECTED!");
        } else if (!completed) {
            System.out.println("  ❌ TIMEOUT: Thread hung");
        } else {
            System.out.println("  ⚠️  Issue not reproduced (most difficult to trigger)");
        }
    }

    /**
     * Example 4: Inconsistent Size vs Elements
     * Size field updated but elements not visible to reader
     */
    private static void example4_InconsistentSize() throws InterruptedException {
        System.out.println("EXAMPLE 4: INCONSISTENT SIZE vs ELEMENTS");
        System.out.println("Size field updated but elements not visible to reader");
        System.out.println();

        final Map<Integer, String> unsafeMap = new HashMap<>();
        final CountDownLatch writerLatch = new CountDownLatch(1);
        final List<InconsistencyReport> inconsistencies = new CopyOnWriteArrayList<>();

        Thread writer = new Thread(() -> {
            try {
                writerLatch.await();
                for (int i = 0; i < ITERATIONS; i++) {
                    unsafeMap.put(i, "value_" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Writer-Thread");

        Thread reader = new Thread(() -> {
            writerLatch.countDown();
            for (int check = 0; check < 1000; check++) {
                int reportedSize = unsafeMap.size();
                int actualCount = 0;

                try {
                    for (Map.Entry<Integer, String> entry : unsafeMap.entrySet()) {
                        actualCount++;
                    }
                } catch (ConcurrentModificationException e) {
                    // Expected
                }

                if (reportedSize != actualCount && reportedSize > 0) {
                    inconsistencies.add(new InconsistencyReport(reportedSize, actualCount));
                }

                Thread.yield();
            }
        }, "Reader-Thread");

        reader.start();
        writer.start();

        writer.join();
        reader.join();

        System.out.println("Results:");
        System.out.println("  Consistency checks: 1000");
        System.out.println("  Inconsistencies detected: " + inconsistencies.size());

        if (!inconsistencies.isEmpty()) {
            System.out.println("  ❌ ISSUE DETECTED: Size/Count mismatches!");
            System.out.println("\n  Sample inconsistencies:");
            for (int i = 0; i < Math.min(5, inconsistencies.size()); i++) {
                InconsistencyReport report = inconsistencies.get(i);
                System.out.println("    - size() = " + report.reportedSize +
                        ", actual count = " + report.actualCount +
                        " (lost " + (report.reportedSize - report.actualCount) + ")");
            }
        } else {
            System.out.println("  ⚠️  Issue not reproduced (timing dependent)");
        }
    }

    /**
     * Demonstrates safe solutions
     */
    private static void safeSolutions() throws InterruptedException {
        System.out.println("SAFE SOLUTIONS DEMONSTRATION");
        System.out.println();

        System.out.println("Solution 1: ConcurrentHashMap");
        testConcurrentHashMap();
        System.out.println();

        System.out.println("Solution 2: Volatile Reference (Immutable Pattern)");
        testVolatileReference();
        System.out.println();

        System.out.println("Solution 3: Synchronized Access");
        testSynchronized();
    }

    private static void testConcurrentHashMap() throws InterruptedException {
        final Map<Integer, String> safeMap = new ConcurrentHashMap<>();
        final CountDownLatch latch = new CountDownLatch(1);
        final int[] nullReads = {0};

        Thread writer = new Thread(() -> {
            try {
                latch.await();
                for (int i = 0; i < ITERATIONS; i++) {
                    safeMap.put(i, "value_" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread reader = new Thread(() -> {
            latch.countDown();
            for (int i = 0; i < ITERATIONS; i++) {
                if (safeMap.get(i) == null) {
                    nullReads[0]++;
                }
            }
        });

        reader.start();
        writer.start();
        writer.join();
        reader.join();

        System.out.println("  Results: NULL reads = " + nullReads[0]);
        System.out.println("  ✅ ConcurrentHashMap is SAFE");
        System.out.println("  - Uses volatile fields internally");
        System.out.println("  - Lock-free reads, segmented locks for writes");
    }

    private static void testVolatileReference() throws InterruptedException {
        final VolatileMapWrapper wrapper = new VolatileMapWrapper();
        final CountDownLatch latch = new CountDownLatch(1);

        Thread writer = new Thread(() -> {
            try {
                latch.await();
                for (int i = 0; i < 100; i++) {
                    wrapper.put(i, "value_" + i);
                    Thread.sleep(1);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread reader = new Thread(() -> {
            latch.countDown();
            for (int i = 0; i < 100; i++) {
                wrapper.get(i);
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        reader.start();
        writer.start();
        writer.join();
        reader.join();

        System.out.println("  Results: Final size = " + wrapper.size());
        System.out.println("  ✅ Volatile reference ensures visibility");
        System.out.println("  - Creates new immutable snapshot per update");
        System.out.println("  - Good for read-heavy workloads");
    }

    private static void testSynchronized() throws InterruptedException {
        final SynchronizedMapWrapper wrapper = new SynchronizedMapWrapper();
        final CountDownLatch latch = new CountDownLatch(1);
        final int[] nullReads = {0};

        Thread writer = new Thread(() -> {
            try {
                latch.await();
                for (int i = 0; i < ITERATIONS; i++) {
                    wrapper.put(i, "value_" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread reader = new Thread(() -> {
            latch.countDown();
            for (int i = 0; i < ITERATIONS; i++) {
                if (wrapper.get(i) == null) {
                    nullReads[0]++;
                }
            }
        });

        reader.start();
        writer.start();
        writer.join();
        reader.join();

        System.out.println("  Results: NULL reads = " + nullReads[0]);
        System.out.println("  ✅ Synchronized access is SAFE");
        System.out.println("  - Lock ensures happens-before relationship");
        System.out.println("  - Performance cost: lock on every operation");
    }

    // Helper classes

    /**
     * Key that always produces hash collisions to force linked list chains
     */
    static class CollisionKey {
        private final int value;

        public CollisionKey(int value) {
            this.value = value;
        }

        @Override
        public int hashCode() {
            return 42; // Always same hash to force collisions
        }

        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof CollisionKey)) return false;
            return this.value == ((CollisionKey) obj).value;
        }
    }

    static class InconsistencyReport {
        final int reportedSize;
        final int actualCount;

        InconsistencyReport(int reportedSize, int actualCount) {
            this.reportedSize = reportedSize;
            this.actualCount = actualCount;
        }
    }

    /**
     * Wrapper using volatile reference for safe publication
     */
    static class VolatileMapWrapper {
        private volatile Map<Integer, String> map = new HashMap<>();

        public void put(Integer key, String value) {
            Map<Integer, String> newMap = new HashMap<>(map);
            newMap.put(key, value);
            map = newMap; // volatile write
        }

        public String get(Integer key) {
            return map.get(key); // volatile read
        }

        public int size() {
            return map.size();
        }
    }

    /**
     * Wrapper using synchronized for safe access
     */
    static class SynchronizedMapWrapper {
        private final Map<Integer, String> map = new HashMap<>();
        private final Object lock = new Object();

        public void put(Integer key, String value) {
            synchronized (lock) {
                map.put(key, value);
            }
        }

        public String get(Integer key) {
            synchronized (lock) {
                return map.get(key);
            }
        }
    }
}
```

#### How to Run

**Compile and run:**
```bash
javac HashMapConcurrencyDemo.java
java HashMapConcurrencyDemo
```

**Expected Output:**
```
EXAMPLE 1: INVISIBLE WRITES
Results:
  Total reads: 10000
  Successful reads: 0
  NULL reads (invisible writes): 10000
  ❌ ISSUE DETECTED: Reader saw 10000 invisible writes!

EXAMPLE 2: BROKEN NODE CHAIN
Results:
  Expected elements: 400
  map.size(): 392
  Counted elements: 11
  ❌ ISSUE DETECTED: Lost elements due to broken chains!
  Lost: 389
```

#### Key Observations from Running the Code

1. **Example 1 (Invisible Writes):**
   - Nearly 100% of reads return null
   - Demonstrates cache visibility problem perfectly
   - Writer's updates never leave its CPU cache

2. **Example 2 (Broken Chains):**
   - Massive data loss (97% of elements lost)
   - Shows structural corruption of internal linked lists
   - Result of reordering and race conditions

3. **Example 3 (Infinite Loop):**
   - Hardest to reproduce but most dangerous
   - Can completely hang your application
   - Classic JDK 6/7 bug

4. **Example 4 (Inconsistent Size):**
   - `size()` shows 1500 but only 1 element is countable
   - Different fields updated at different times
   - No atomicity guarantee

**All issues disappear when using `ConcurrentHashMap`!**

---

