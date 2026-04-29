# Reference: spring-boot-setup

**Source file:** `.claude/java-architect/references/spring-boot-setup.md`

# Spring Boot Service Setup

## Package Convention

`<domain>.explore` — e.g. `market.explore`, `demo.explore`, `coinbase.explore`

## Module Structure

```
explore-<name>-service/
├── pom.xml
└── src/
    ├── main/
    │   ├── java/<domain>/explore/
    │   │   ├── <Name>ServiceApplication.java
    │   │   ├── agent/          # Agrona Agent implementations
    │   │   ├── service/        # Spring @Component services
    │   │   ├── setting/        # Setting.java
    │   │   └── utils/          # ThreadFactoryUtils.java
    │   └── resources/
    │       └── application.yml
    └── test/
        └── java/<domain>/explore/
            └── <Name>ServiceApplicationTests.java  (commented out)
```

## pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>example</groupId>
        <artifactId>mmm</artifactId>
        <version>0.0.1-SNAPSHOT</version>
        <relativePath>../pom.xml</relativePath>
    </parent>

    <groupId>example1</groupId>
    <artifactId>explore-<name>-service</artifactId>
    <version>1.0.0</version>
    <name>explore-<name>-service</name>
    <description>explore-<name>-service</description>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
        <dependency>
            <groupId>io.aeron</groupId>
            <artifactId>aeron-all</artifactId>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
        </dependency>
    </dependencies>

</project>
```

Register the new module in root `pom.xml` under `<modules>`.

## application.yml

```yaml
spring:
  application:
    name: explore-<name>-service

settings:
```

Add service-specific config keys under `settings:` and bind them in `Setting.java`.

## Main Application Class

```java
@SpringBootApplication
@AllArgsConstructor
@EnableConfigurationProperties(Setting.class)
@Slf4j
public class <Name>ServiceApplication implements CommandLineRunner {
    private final Setting setting;
    private final TestService testService;

    public static void main(String[] args) {
        SpringApplication.run(<Name>ServiceApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        testService.getTestMessage();

        AgentRunner runner = new AgentRunner(
                new SleepingIdleStrategy(),
                Throwable::printStackTrace,
                null,
                new MyAgent()   // replace with actual agent(s)
        );
        AgentRunner.startOnThread(runner, ThreadFactoryUtils.getNonDaemonThreadFactory());

        ShutdownSignalBarrier barrier = new ShutdownSignalBarrier();
        SigInt.register(() -> {
            barrier.signal();
            log.info("Shutdown signal received");
        });

        barrier.await();
        log.info("Main thread terminated");
        runner.close();
    }
}
```

## Setting.java

```java
@Component
@ConfigurationProperties("settings")
@Data
@Slf4j
public class Setting {
    // add typed fields that mirror keys under settings: in application.yml
}
```

## TestService.java

```java
@Component
@Slf4j
public class TestService {

    public void getTestMessage() {
        log.info("Test message from TestService");
    }
}
```

## ThreadFactoryUtils.java

```java
public class ThreadFactoryUtils {
    public static final String THREAD_PREFIX = "unamed-thread";

    private ThreadFactoryUtils() {}

    public static ThreadFactory getDaemonThreadFactory() {
        return getThreadFactory(THREAD_PREFIX, true);
    }

    public static ThreadFactory getNonDaemonThreadFactory() {
        return getThreadFactory(THREAD_PREFIX, true);
    }

    public static ThreadFactory getNamedDeamonTHreadFactory(String prefix) {
        return getThreadFactory(prefix, true);
    }

    public static ThreadFactory getThreadFactory(String prefix, boolean daemon) {
        return new ThreadFactory() {
            private final AtomicLong count = new AtomicLong();

            @Override
            public Thread newThread(Runnable r) {
                Thread thread = new Thread(r);
                thread.setDaemon(daemon);
                thread.setName(prefix + "-" + count.incrementAndGet());
                return thread;
            }
        };
    }
}
```

## Test Class (commented out — project convention)

```java
//package <domain>.explore;
//
//import org.junit.jupiter.api.Test;
//import org.springframework.boot.test.context.SpringBootTest;
//
//@SpringBootTest
//class <Name>ServiceApplicationTests {
//
//    @Test
//    void contextLoads() {
//    }
//
//}
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `@SpringBootApplication` | Main application entry point |
| `@EnableConfigurationProperties` | Activates `@ConfigurationProperties` beans |
| `@ConfigurationProperties("settings")` | Binds `settings.*` from yml to typed class |
| `CommandLineRunner` | Entry point after Spring context is ready |
| `@AllArgsConstructor` + `@Slf4j` | Lombok constructor injection and logger |
| `ShutdownSignalBarrier` + `SigInt` | Agrona graceful shutdown on SIGINT |
| `AgentRunner.startOnThread` | Starts agent loop on a dedicated thread |
| `runner.close()` | Triggers `Agent.onClose()` on shutdown |
