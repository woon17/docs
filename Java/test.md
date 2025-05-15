## Stack

- **Purpose**: Stores method call frames, local variables, and references.
- **Scope**: Thread-local (each thread has its own stack).
- **Speed**: Very fast (LIFO access).
- **Memory Management**: Automatically freed after method execution.
- **Lifetime**: Limited to the duration of the method.
- **Garbage Collected?**: No.
- **Common Error**: `StackOverflowError` for deep recursion.

```java
void method() {
    int x = 10;         // x is stored on the stack
    String s = "hi";    // reference is on the stack; "hi" is in the string pool
}
```

---

## Heap

- **Purpose**: Stores all Java objects and arrays.
- **Scope**: Shared memory, accessible by all threads.
- **Speed**: Slower than stack (due to GC and dynamic allocation).
- **Memory Management**: Managed by the Garbage Collector.
- **Lifetime**: Until no longer referenced.
- **Garbage Collected?**: Yes.
- **Common Error**: `OutOfMemoryError` when heap is exhausted.

```java
String s = new String("hi"); // a new object is created in the heap
```

---

## Comparison Table

| Feature          | Stack                      | Heap                        |
|------------------|-----------------------------|-----------------------------|
| Stores           | Primitives, refs, call frames| Objects, arrays             |
| Scope            | Per-thread                  | Shared across threads       |
| Speed            | Fast                        | Slower                      |
| GC-managed       | No                          | Yes                         |
| Lifetime         | Until method exits          | Until dereferenced          |
| Common Errors    | StackOverflowError          | OutOfMemoryError            |

---

## Summary

- Use **stack** for fast-access local data inside methods.
-  Use **heap** for objects and data that must persist beyond method calls.
