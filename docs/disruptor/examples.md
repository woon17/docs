# Conduit Framework - Example Applications

This page provides real-world examples and complete applications using the Conduit framework.

## Example 1: Market Data Processing

A financial trading system that processes market data from multiple sources.

### Scenario

- Receive price updates from multiple exchanges
- Process order book updates
- Calculate spread and liquidity metrics
- Trigger trading signals

### Implementation

```java
import io.lightning.conduit.dispatcher.EventDispatcher;
import io.lightning.conduit.node.DisruptorNode3;

// Domain objects
record Price(String symbol, double bid, double ask, long timestamp) {}
record OrderBook(String symbol, List<Order> bids, List<Order> asks) {}
record Trade(String symbol, double price, long volume, long timestamp) {}

// Processing node
public class MarketDataProcessor extends DisruptorNode3<Price, OrderBook, Trade> {
    private final Map<String, Price> currentPrices = new HashMap<>();
    private final Map<String, OrderBook> currentBooks = new HashMap<>();
    private final EventDispatcher<TradingSignal> signalDispatcher;

    public MarketDataProcessor(EventDispatcher<TradingSignal> signalDispatcher) {
        this.signalDispatcher = signalDispatcher;
    }

    @Override
    protected void onEvent1(Price price) {
        currentPrices.put(price.symbol(), price);

        double spread = price.ask() - price.bid();
        double midPrice = (price.bid() + price.ask()) / 2.0;

        // Check for trading opportunities
        if (spread < 0.01) { // Tight spread
            TradingSignal signal = new TradingSignal(
                price.symbol(),
                midPrice,
                "TIGHT_SPREAD"
            );
            signalDispatcher.dispatch(signal);
        }
    }

    @Override
    protected void onEvent2(OrderBook book) {
        currentBooks.put(book.symbol(), book);

        // Calculate liquidity
        double bidLiquidity = book.bids().stream()
            .mapToDouble(Order::volume)
            .sum();
        double askLiquidity = book.asks().stream()
            .mapToDouble(Order::volume)
            .sum();

        System.out.printf("Liquidity %s: Bid=%.0f Ask=%.0f%n",
            book.symbol(), bidLiquidity, askLiquidity);
    }

    @Override
    protected void onEvent3(Trade trade) {
        Price currentPrice = currentPrices.get(trade.symbol());
        if (currentPrice != null) {
            double midPrice = (currentPrice.bid() + currentPrice.ask()) / 2.0;

            // Detect large trades
            if (trade.volume() > 10000) {
                System.out.printf("Large trade detected: %s %,.0f @ %.2f%n",
                    trade.symbol(), trade.volume(), trade.price());

                // Dispatch alert
                TradingSignal signal = new TradingSignal(
                    trade.symbol(),
                    trade.price(),
                    "LARGE_TRADE"
                );
                signalDispatcher.dispatch(signal);
            }
        }
    }
}

// Main application
public class TradingApplication {
    public static void main(String[] args) throws Exception {
        // Create dispatchers
        EventDispatcher<Price> priceDispatcher = EventDispatcher.create();
        EventDispatcher<OrderBook> bookDispatcher = EventDispatcher.create();
        EventDispatcher<Trade> tradeDispatcher = EventDispatcher.create();
        EventDispatcher<TradingSignal> signalDispatcher = EventDispatcher.create();

        // Create and start processor
        MarketDataProcessor processor = new MarketDataProcessor(signalDispatcher);
        processor.subscribe1(priceDispatcher)
                 .subscribe2(bookDispatcher)
                 .subscribe3(tradeDispatcher);
        processor.start();

        // Create signal handler
        DisruptorNode1<TradingSignal> signalHandler = new SignalHandler();
        signalHandler.subscribe1(signalDispatcher);
        signalHandler.start();

        // Simulate market data (in real app, this comes from market feeds)
        new Thread(() -> {
            while (true) {
                Price price = new Price("AAPL", 150.25, 150.27, System.nanoTime());
                priceDispatcher.dispatch(price);
                sleep(100);
            }
        }).start();

        Thread.sleep(Long.MAX_VALUE); // Keep running
    }

    private static void sleep(long ms) {
        try { Thread.sleep(ms); } catch (InterruptedException e) {}
    }
}
```

## Example 2: Real-Time Analytics Pipeline

Process sensor data from IoT devices and calculate real-time metrics.

### Scenario

- Receive temperature readings
- Receive humidity readings
- Receive motion detection events
- Calculate comfort index and trigger alerts

### Implementation

```java
import io.lightning.conduit.dispatcher.EventDispatcher;
import io.lightning.conduit.node.DisruptorNode3;

// Sensor data types
record Temperature(String sensorId, double celsius, long timestamp) {}
record Humidity(String sensorId, double percentage, long timestamp) {}
record Motion(String sensorId, boolean detected, long timestamp) {}

// Alert type
record Alert(String type, String message, String sensorId) {}

public class IoTAnalytics extends DisruptorNode3<Temperature, Humidity, Motion> {
    private final Map<String, Double> temperatures = new ConcurrentHashMap<>();
    private final Map<String, Double> humidity = new ConcurrentHashMap<>();
    private final EventDispatcher<Alert> alertDispatcher;

    public IoTAnalytics(EventDispatcher<Alert> alertDispatcher) {
        this.alertDispatcher = alertDispatcher;
    }

    @Override
    protected void onEvent1(Temperature temp) {
        temperatures.put(temp.sensorId(), temp.celsius());

        // Check for extreme temperature
        if (temp.celsius() > 35.0) {
            Alert alert = new Alert(
                "HIGH_TEMPERATURE",
                String.format("Temperature %.1f°C exceeds threshold", temp.celsius()),
                temp.sensorId()
            );
            alertDispatcher.dispatch(alert);
        }

        // Calculate comfort index if we have both temp and humidity
        Double h = humidity.get(temp.sensorId());
        if (h != null) {
            double comfortIndex = calculateComfortIndex(temp.celsius(), h);
            System.out.printf("Comfort index for %s: %.1f%n",
                temp.sensorId(), comfortIndex);
        }
    }

    @Override
    protected void onEvent2(Humidity hum) {
        humidity.put(hum.sensorId(), hum.percentage());

        // Check for high humidity
        if (hum.percentage() > 70.0) {
            Alert alert = new Alert(
                "HIGH_HUMIDITY",
                String.format("Humidity %.1f%% exceeds threshold", hum.percentage()),
                hum.sensorId()
            );
            alertDispatcher.dispatch(alert);
        }
    }

    @Override
    protected void onEvent3(Motion motion) {
        if (motion.detected()) {
            System.out.printf("Motion detected: %s at %d%n",
                motion.sensorId(), motion.timestamp());

            // Correlate with temperature for occupancy comfort
            Double temp = temperatures.get(motion.sensorId());
            if (temp != null && (temp < 18 || temp > 26)) {
                Alert alert = new Alert(
                    "UNCOMFORTABLE_OCCUPANCY",
                    String.format("Motion detected but temperature %.1f°C is uncomfortable", temp),
                    motion.sensorId()
                );
                alertDispatcher.dispatch(alert);
            }
        }
    }

    private double calculateComfortIndex(double tempC, double humidity) {
        // Simplified comfort index calculation
        return tempC - (0.55 - 0.0055 * humidity) * (tempC - 14.5);
    }
}

// Alert handler
public class AlertHandler extends DisruptorNode1<Alert> {
    @Override
    protected void onEvent1(Alert alert) {
        System.err.printf("[ALERT] %s: %s (Sensor: %s)%n",
            alert.type(), alert.message(), alert.sensorId());

        // In real application: send email, SMS, push notification, etc.
        sendNotification(alert);
    }

    private void sendNotification(Alert alert) {
        // Implementation for sending notifications
    }
}

// Main application
public class IoTApplication {
    public static void main(String[] args) throws Exception {
        // Create dispatchers
        EventDispatcher<Temperature> tempDispatcher = EventDispatcher.create();
        EventDispatcher<Humidity> humidityDispatcher = EventDispatcher.create();
        EventDispatcher<Motion> motionDispatcher = EventDispatcher.create();
        EventDispatcher<Alert> alertDispatcher = EventDispatcher.create();

        // Create and start analytics
        IoTAnalytics analytics = new IoTAnalytics(alertDispatcher);
        analytics.subscribe1(tempDispatcher)
                 .subscribe2(humidityDispatcher)
                 .subscribe3(motionDispatcher);
        analytics.start();

        // Create and start alert handler
        AlertHandler alertHandler = new AlertHandler();
        alertHandler.subscribe1(alertDispatcher);
        alertHandler.start();

        // Simulate sensor data
        simulateSensorData(tempDispatcher, humidityDispatcher, motionDispatcher);
    }

    private static void simulateSensorData(
            EventDispatcher<Temperature> tempDispatcher,
            EventDispatcher<Humidity> humidityDispatcher,
            EventDispatcher<Motion> motionDispatcher) {

        Random random = new Random();

        while (true) {
            String sensorId = "sensor-" + (random.nextInt(5) + 1);

            // Temperature reading
            double temp = 20 + random.nextDouble() * 10;
            tempDispatcher.dispatch(new Temperature(sensorId, temp, System.nanoTime()));

            // Humidity reading
            double humidity = 40 + random.nextDouble() * 30;
            humidityDispatcher.dispatch(new Humidity(sensorId, humidity, System.nanoTime()));

            // Motion detection (20% chance)
            if (random.nextDouble() < 0.2) {
                motionDispatcher.dispatch(new Motion(sensorId, true, System.nanoTime()));
            }

            sleep(1000);
        }
    }

    private static void sleep(long ms) {
        try { Thread.sleep(ms); } catch (InterruptedException e) {}
    }
}
```

## Example 3: Event Sourcing System

Build an event-sourced application with CQRS pattern.

### Scenario

- Receive commands (create, update, delete)
- Generate events
- Update read models
- Maintain event log

### Implementation

```java
import io.lightning.conduit.dispatcher.EventDispatcher;
import io.lightning.conduit.node.DisruptorNode2;

// Commands
sealed interface Command permits CreateUser, UpdateUser, DeleteUser {}
record CreateUser(String userId, String name, String email) implements Command {}
record UpdateUser(String userId, String name, String email) implements Command {}
record DeleteUser(String userId) implements Command {}

// Events
sealed interface Event permits UserCreated, UserUpdated, UserDeleted {}
record UserCreated(String userId, String name, String email, long timestamp) implements Event {}
record UserUpdated(String userId, String name, String email, long timestamp) implements Event {}
record UserDeleted(String userId, long timestamp) implements Event {}

// Command Handler - generates events from commands
public class CommandHandler extends DisruptorNode1<Command> {
    private final EventDispatcher<Event> eventDispatcher;
    private final Map<String, User> currentState = new HashMap<>();

    public CommandHandler(EventDispatcher<Event> eventDispatcher) {
        this.eventDispatcher = eventDispatcher;
    }

    @Override
    protected void onEvent1(Command command) {
        switch (command) {
            case CreateUser cmd -> {
                if (!currentState.containsKey(cmd.userId())) {
                    UserCreated event = new UserCreated(
                        cmd.userId(), cmd.name(), cmd.email(), System.currentTimeMillis()
                    );
                    eventDispatcher.dispatch(event);
                }
            }
            case UpdateUser cmd -> {
                if (currentState.containsKey(cmd.userId())) {
                    UserUpdated event = new UserUpdated(
                        cmd.userId(), cmd.name(), cmd.email(), System.currentTimeMillis()
                    );
                    eventDispatcher.dispatch(event);
                }
            }
            case DeleteUser cmd -> {
                if (currentState.containsKey(cmd.userId())) {
                    UserDeleted event = new UserDeleted(
                        cmd.userId(), System.currentTimeMillis()
                    );
                    eventDispatcher.dispatch(event);
                }
            }
        }
    }
}

// Event Processor - updates read model and event log
public class EventProcessor extends DisruptorNode1<Event> {
    private final Map<String, User> readModel = new ConcurrentHashMap<>();
    private final List<Event> eventLog = new ArrayList<>();

    @Override
    protected void onEvent1(Event event) {
        // Append to event log
        synchronized (eventLog) {
            eventLog.add(event);
        }

        // Update read model
        switch (event) {
            case UserCreated e -> {
                User user = new User(e.userId(), e.name(), e.email());
                readModel.put(e.userId(), user);
                System.out.printf("User created: %s%n", user);
            }
            case UserUpdated e -> {
                User user = new User(e.userId(), e.name(), e.email());
                readModel.put(e.userId(), user);
                System.out.printf("User updated: %s%n", user);
            }
            case UserDeleted e -> {
                readModel.remove(e.userId());
                System.out.printf("User deleted: %s%n", e.userId());
            }
        }
    }

    public Map<String, User> getReadModel() {
        return Collections.unmodifiableMap(readModel);
    }

    public List<Event> getEventLog() {
        synchronized (eventLog) {
            return new ArrayList<>(eventLog);
        }
    }
}

// User entity
record User(String userId, String name, String email) {}

// Main application
public class EventSourcingApp {
    public static void main(String[] args) throws Exception {
        // Create dispatchers
        EventDispatcher<Command> commandDispatcher = EventDispatcher.create();
        EventDispatcher<Event> eventDispatcher = EventDispatcher.create();

        // Create command handler
        CommandHandler commandHandler = new CommandHandler(eventDispatcher);
        commandHandler.subscribe1(commandDispatcher);
        commandHandler.start();

        // Create event processor
        EventProcessor eventProcessor = new EventProcessor();
        eventProcessor.subscribe1(eventDispatcher);
        eventProcessor.start();

        // Execute commands
        commandDispatcher.dispatch(new CreateUser("user1", "Alice", "alice@example.com"));
        commandDispatcher.dispatch(new CreateUser("user2", "Bob", "bob@example.com"));
        Thread.sleep(100);

        commandDispatcher.dispatch(new UpdateUser("user1", "Alice Smith", "alice.smith@example.com"));
        Thread.sleep(100);

        commandDispatcher.dispatch(new DeleteUser("user2"));
        Thread.sleep(100);

        // Query read model
        System.out.println("\nCurrent State:");
        eventProcessor.getReadModel().forEach((id, user) ->
            System.out.printf("  %s: %s (%s)%n", id, user.name(), user.email())
        );

        // View event log
        System.out.println("\nEvent Log:");
        eventProcessor.getEventLog().forEach(event ->
            System.out.printf("  %s%n", event)
        );
    }
}
```

## Example 4: Log Aggregation System

Aggregate and process log entries from multiple services.

### Scenario

- Receive application logs
- Receive system logs
- Parse and categorize logs
- Generate metrics and alerts

### Implementation

```java
import io.lightning.conduit.dispatcher.EventDispatcher;
import io.lightning.conduit.node.DisruptorNode2;

// Log types
record AppLog(String service, String level, String message, long timestamp) {}
record SystemLog(String host, String subsystem, String message, long timestamp) {}

// Metrics
record LogMetrics(String source, Map<String, Long> levelCounts) {}

public class LogAggregator extends DisruptorNode2<AppLog, SystemLog> {
    private final Map<String, AtomicLong> errorCounts = new ConcurrentHashMap<>();
    private final EventDispatcher<Alert> alertDispatcher;

    public LogAggregator(EventDispatcher<Alert> alertDispatcher) {
        this.alertDispatcher = alertDispatcher;
    }

    @Override
    protected void onEvent1(AppLog log) {
        // Count errors by service
        if ("ERROR".equals(log.level()) || "FATAL".equals(log.level())) {
            errorCounts.computeIfAbsent(log.service(), k -> new AtomicLong())
                       .incrementAndGet();

            // Alert on high error rate
            if (errorCounts.get(log.service()).get() % 10 == 0) {
                Alert alert = new Alert(
                    "HIGH_ERROR_RATE",
                    String.format("%s has logged %d errors",
                        log.service(), errorCounts.get(log.service()).get()),
                    log.service()
                );
                alertDispatcher.dispatch(alert);
            }
        }

        // Log processing
        System.out.printf("[%s] %s: %s%n", log.level(), log.service(), log.message());
    }

    @Override
    protected void onEvent2(SystemLog log) {
        // Process system logs
        System.out.printf("[SYSTEM] %s/%s: %s%n",
            log.host(), log.subsystem(), log.message());

        // Check for critical system events
        if (log.message().contains("Out of memory") ||
            log.message().contains("Disk full")) {
            Alert alert = new Alert(
                "SYSTEM_CRITICAL",
                log.message(),
                log.host()
            );
            alertDispatcher.dispatch(alert);
        }
    }
}

public class LogApplication {
    public static void main(String[] args) throws Exception {
        EventDispatcher<AppLog> appLogDispatcher = EventDispatcher.create();
        EventDispatcher<SystemLog> sysLogDispatcher = EventDispatcher.create();
        EventDispatcher<Alert> alertDispatcher = EventDispatcher.create();

        LogAggregator aggregator = new LogAggregator(alertDispatcher);
        aggregator.subscribe1(appLogDispatcher)
                  .subscribe2(sysLogDispatcher);
        aggregator.start();

        AlertHandler alertHandler = new AlertHandler();
        alertHandler.subscribe1(alertDispatcher);
        alertHandler.start();

        // Simulate logs
        simulateLogs(appLogDispatcher, sysLogDispatcher);
    }
}
```

## Testing Your Conduit Application

### Unit Testing

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class MarketDataProcessorTest {
    private EventDispatcher<Price> priceDispatcher;
    private EventDispatcher<TradingSignal> signalDispatcher;
    private MarketDataProcessor processor;
    private List<TradingSignal> capturedSignals;

    @BeforeEach
    void setup() {
        priceDispatcher = EventDispatcher.create();
        signalDispatcher = EventDispatcher.create();
        capturedSignals = new ArrayList<>();

        // Capture signals
        signalDispatcher.register(signal -> capturedSignals.add(signal));

        processor = new MarketDataProcessor(signalDispatcher);
        processor.subscribe1(priceDispatcher);
        processor.start();
    }

    @Test
    void shouldDetectTightSpread() throws Exception {
        Price price = new Price("AAPL", 150.00, 150.01, System.nanoTime());
        priceDispatcher.dispatch(price);

        Thread.sleep(100); // Wait for processing

        assertEquals(1, capturedSignals.size());
        assertEquals("TIGHT_SPREAD", capturedSignals.get(0).type());
    }
}
```

## Performance Tips

1. **Keep event handlers lightweight** - Process quickly and return
2. **Use object pooling** - Reuse objects to reduce GC pressure
3. **Choose appropriate ring buffer size** - Power of 2, typically 1024-8192
4. **Monitor backpressure** - Watch for ring buffer fullness
5. **Offload I/O** - Use separate thread pools for blocking operations

## Next Steps

- [LMAX Disruptor Overview](index.md)
- [Conduit Framework Guide](conduit-framework.md)
- [Performance Analysis](performance.md)
