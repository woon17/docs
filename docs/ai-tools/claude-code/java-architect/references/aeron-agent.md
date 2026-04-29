# Reference: aeron-agent

**Source file:** `.claude/java-architect/references/aeron-agent.md`

# Agrona Agent Pattern

## Single Agent

```java
@Slf4j
public class MyAgent implements Agent {
    private static final long INTERVAL_MS = 5_000;
    private final SystemEpochClock clock = SystemEpochClock.INSTANCE;
    private long lastRunTime;

    @Override
    public void onStart() {
        lastRunTime = clock.time();
        log.info("MyAgent started");
    }

    @Override
    public int doWork() {
        long now = clock.time();
        if (now - lastRunTime >= INTERVAL_MS) {
            // do work
            lastRunTime = now;
            return 1;   // work was done
        }
        return 0;       // no work — idle strategy backs off
    }

    @Override
    public String roleName() {
        return "MyAgent";
    }

    @Override
    public void onClose() {
        log.info("MyAgent closed");
    }
}
```

**`doWork()` return values:**
- Return `1` (or any positive int) when work was done — runner stays active
- Return `0` when nothing to do — idle strategy (e.g. `SleepingIdleStrategy`) backs off

## AgentRunner — wiring in main app

```java
AgentRunner runner = new AgentRunner(
        new SleepingIdleStrategy(),   // backs off when doWork returns 0
        Throwable::printStackTrace,   // error handler
        null,                         // AtomicCounter (optional, pass null)
        new MyAgent()
);
AgentRunner.startOnThread(runner, ThreadFactoryUtils.getNonDaemonThreadFactory());
```

Always close the runner on shutdown so `Agent.onClose()` is called:

```java
barrier.await();
log.info("Main thread terminated");
runner.close();
```

## Multiple Agents — CompositeAgent

```java
List<Agent> agents = new ArrayList<>();
agents.add(new AgentA());
agents.add(new AgentB());

AgentRunner runner = new AgentRunner(
        new SleepingIdleStrategy(),
        Throwable::printStackTrace,
        null,
        new CompositeAgent(agents)
);
AgentRunner.startOnThread(runner, ThreadFactoryUtils.getNonDaemonThreadFactory());
```

Each agent's `doWork()` is called in sequence on every loop iteration. Agents share one thread — keep `doWork()` non-blocking.

## Multiple Runners — parallel agents on separate threads

```java
AgentRunner runnerA = new AgentRunner(new SleepingIdleStrategy(), Throwable::printStackTrace, null, new AgentA());
AgentRunner runnerB = new AgentRunner(new SleepingIdleStrategy(), Throwable::printStackTrace, null, new AgentB());

AgentRunner.startOnThread(runnerA, ThreadFactoryUtils.getNonDaemonThreadFactory());
AgentRunner.startOnThread(runnerB, ThreadFactoryUtils.getNonDaemonThreadFactory());

barrier.await();
runnerA.close();
runnerB.close();
```

## Idle Strategies

| Strategy | Behaviour | Use When |
|----------|-----------|----------|
| `SleepingIdleStrategy` | Sleeps when idle | Default — low CPU, tolerates latency |
| `BusySpinIdleStrategy` | Spins continuously | Ultra-low latency, high CPU cost |
| `YieldingIdleStrategy` | Thread.yield() | Moderate latency, moderate CPU |
| `BackoffIdleStrategy` | Progressive backoff | General purpose |

## Interval Pattern with Configurable Interval

Make the interval configurable via `Setting` rather than hardcoding:

```java
// Setting.java
private int intervalMs = 5_000;   // default, overridable in application.yml

// application.yml
settings:
  interval-ms: 5000

// Agent constructor
public MyAgent(Setting setting) {
    this.intervalMs = setting.getIntervalMs();
}
```

## Quick Reference

| Class | Package | Purpose |
|-------|---------|---------|
| `Agent` | `org.agrona.concurrent` | Interface to implement |
| `AgentRunner` | `org.agrona.concurrent` | Manages agent lifecycle on a thread |
| `CompositeAgent` | `org.agrona.concurrent` | Runs multiple agents on one thread |
| `SleepingIdleStrategy` | `org.agrona.concurrent` | Default idle strategy |
| `SystemEpochClock` | `org.agrona.concurrent` | Wall-clock time in milliseconds |
| `ShutdownSignalBarrier` | `org.agrona.concurrent` | Blocks main thread until SIGINT |
| `SigInt` | `org.agrona.concurrent` | Registers SIGINT handler |
