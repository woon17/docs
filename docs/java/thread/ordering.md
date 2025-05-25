The ordering problem in multithreaded programming can be caused by:

=== "Due to single thread"
    Modern compilers and CPUs may reorder instructions for performance as long as the result is the same from the perspective of that single thread.

    🔸 But this can break correctness in multithreaded scenarios.

    ```java
    int x = 0;
    boolean flag = false;

    // Thread 1
    x = 42;           // Step 1
    flag = true;      // Step 2 (might be reordered before Step 1)

    // Thread 2
    if (flag) {
        System.out.println(x); // May print 0!
    }
    ```

    Because the compiler/CPU might reorder setting flag = true before x = 42, `Thread 2` might see flag == true but read an old value of x.


=== "Due to different threads"
    Even if the instructions are ordered correctly in each thread, if there’s no proper synchronization (e.g., volatile, locks, atomic ops), Thread 2 may see stale or reordered results due to:

    - CPU caches
    - Memory model differences
    - Write buffers not flushed



## Java Memory Model (JMM)
The Java Memory Model explicitly allows such reordering unless:

- use volatile
- synchronize (synchronized, Lock)
- use atomic classes (AtomicInteger, etc.)

These establish happens-before relationships that:

- ✅ Prevent reordering
- ✅ Guarantee visibility

