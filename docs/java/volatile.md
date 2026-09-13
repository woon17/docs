
# Java `volatile`, Thread Visibility, and Atomicity

In multithreaded programming, it's important to understand two key concepts: **visibility** and **atomicity**.

```mermaid
flowchart LR
    V["visibility problem<br/>(stale cached reads)"] -->|"fixed by"| Volatile["volatile"]
    A["atomicity problem<br/>(lost updates from read-modify-write)"] -->|"fixed by"| Atomic["AtomicInteger / synchronized"]
    Volatile -.->|"does NOT fix"| A
```

`volatile` solves exactly one problem and stops there — it's tempting to reach for it as a
general "make this thread-safe" keyword, but the diagram above is the whole story: it guarantees
visibility, full stop. A compound operation like `count++` still needs `AtomicInteger` or a lock
regardless of whether `count` is `volatile`.

For the full mechanism behind each side — memory barriers, CPU caches, the actual
read-modify-write race — see [Visibility Issues](thread/visibility.md) and
[Atomicity Issues](thread/atomicity.md), which this page summarizes.

---

## `volatile` and Thread Visibility

### What is Visibility?

**Visibility** means that when one thread modifies a variable, other threads see the updated value.

By default, the JVM and CPU may cache values in registers or CPU cache, so one thread might not immediately see changes made by another.

### How `volatile` Helps

The `volatile` keyword tells the JVM:
- Always read/write the variable **directly from/to main memory**
- Do **not cache** the value in registers or thread-local caches

### Example:

```java
volatile boolean running = true;

Thread t = new Thread(() -> {
    while (running) {
        // Wait for shutdown
    }
});
t.start();

Thread.sleep(1000);
running = false; // This change is immediately visible to thread t
```

Without `volatile`, `t` might keep running forever because it might never see `running = false`.

---

## `volatile` Does NOT Guarantee Atomicity

### ❓ What is Atomicity?

**Atomicity** means that a compound operation (like `count++`) executes as one **indivisible step** — no other thread can observe it in a halfway state.

### ❌ `volatile` Doesn't Help with This:

```java
volatile int count = 0;

public void increment() {
    count++; // NOT atomic!
}
```

This actually performs:
1. Read `count`
2. Increment it
3. Write it back

Multiple threads may read the same value before any writes complete, causing lost updates.

### Use `AtomicInteger` for Atomicity:

```java
AtomicInteger count = new AtomicInteger(0);

public void increment() {
    count.incrementAndGet(); // Atomic and visible
}
```

`AtomicInteger` uses low-level CPU instructions (like CAS) to ensure the operation is thread-safe and atomic.

---

## 🧠 Summary Table

| Feature    | `volatile`       | `AtomicInteger`         |
|------------|------------------|--------------------------|
| Visibility | Yes           | Yes                  |
| Atomicity  | ❌ No            | Yes                  |
| Use case   | State flags      | Counters, increments     |

---

## Conclusion

- Use `volatile` for simple **state flags** between threads (like shutdown signals).
- Use `AtomicInteger` or synchronization for **compound or critical updates**.
- Understanding both **visibility** and **atomicity** is essential for writing correct concurrent code in Java.

## Related

- [Visibility Issues](thread/visibility.md) — the CPU-cache mechanism behind `volatile`.
- [Atomicity Issues](thread/atomicity.md) — the read-modify-write race `volatile` can't fix.
- [Ordering Issues](thread/ordering.md) — the third pillar: instruction reordering.
- [Shutdown Mechanisms](shutdown.md) — `volatile`'s classic "state flag" use case in practice.
