# KDB+ Documentation

Welcome to KDB+ (Q) documentation covering setup, operations, and integration examples for this high-performance time-series database.

## Overview

KDB+ is a high-performance column-oriented database with a built-in expressive query and programming language called Q. It's particularly well-suited for financial time-series data and real-time analytics.

## Getting Started

### Prerequisites
- KDB+ installation (see [setup guide](setup.md))
- Basic understanding of columnar databases
- Familiarity with functional programming concepts

### Quick Start
1. **[Setup KDB+ on M3](setup.md)** - Installation guide for ARM-based Macs
2. **[Connect manually](connect.md)** - Basic connection methods
3. **[Simple Demo](demo.md)** - Working examples and tutorials

## Core Concepts

### Essential Commands
```q
// List all tables in root namespace
q)tables `.

// Check dictionary structure
q).u.w  // tick subscription dictionary
```

### Table Operations

#### Creating Tables
```q
// Define stock table schema
stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$())

// Insert single record
`stocks insert (.z.p; `AAPL; 170.11)

// Upsert with structured data
row: flip `time`sym`price! (enlist .z.p; enlist `AAPL; enlist 189.3)
stocks upsert row
```

## Integration Patterns

### Java Integration
For Java applications connecting to KDB+:

#### Reading Data
```java
private static void printStocks(c c) throws c.KException, IOException {
    // KDB+ query: select from stocks where time < .z.p, sorted by time descending
    String query = "xdesc[`time] select from stocks where time < .z.p";
    
    // Send query and receive result
    Object result_kdb = c.k(query);
    
    Flip table = (Flip) result_kdb;
    String[] columnNames = table.x;
    Object[] columnData = table.y;
    
    int rowCount = Array.getLength(columnData[0]);
    
    for (int i = 0; i < rowCount; i++) {
        StringBuilder row = new StringBuilder();
        for (int j = 0; j < columnNames.length; j++) {
            Object col = columnData[j];
            Object value = Array.get(col, i);
            row.append(columnNames[j]).append("=").append(value).append(" ");
        }
        System.out.println(row.toString());
    }
}
```

#### Writing Data
```java
private static void insertStock(c c, String sym, double price) throws c.KException, IOException {
    String query = String.format("`stocks insert (.z.p; `%s; %f)", sym, price);
    c.ks(query);
}
```

### Real-time Data Streaming

#### Q Process Setup
```bash
# Start Q process with port
q -p 1234
```

```q
// Define stream schema
stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$());

// Load tick utilities
\l tick/u.q
.u.init[]

// Memory management - keep only last minute of data
.z.ts:{ `stocks set select from stocks where time > .z.p - 00:01:00.000 };
\t 1000  // Execute every second
```

#### Dashboard Integration
For KX Dashboard connections:

1. **Data Source Configuration**: Use `DataSource->kdb+/q`
2. **Query for latest data**:
   ```q
   `time xdesc select from stocks where time < .z.p
   ```
3. **Subscription Settings**:
   - Polling: Enabled
   - Force Reset: Enabled  
   - Interval: 1s
   - Key: Row Num

## Advanced Topics

### Memory Management
```q
// Keep only latest 10 records
.z.ts:{ `stocks set select from stocks where i > (count stocks) - 10 }

// Time-based retention (10 minutes)
.z.ts:{ `stocks set delete from stocks where time < .z.p - 00:10:00.000 }
```

### Tick Integration
```q
// Initialize tick publishing
\l tick/u.q
.u.init[]

// Define update function for dashboards
.u.upd:{[table; data] insert[table; flip data]; .u.pub[table; flip data];}
.u.snap:{stocks}

// Publish updates every second
\t 1000
.z.ts:{ .u.pub[`stocks; .u.snap[`stocks]] }
```

## Additional Resources

### Documentation Links
- [KX Dashboard Getting Started](https://code.kx.com/dashboards/gettingstarted/)
- [KX Developer Guide](https://code.kx.com/developer/getting-started/)
- [KDB Java API Guide](https://www.timestored.com/kdb-guides/kdb-java-api)

### Related Topics
- **[Dashboard Configuration](kxDashboard.md)** - KX Dashboard data source setup
- **[Connection Examples](connect.md)** - Manual connection methods
- **[M3 Setup Guide](setup.md)** - Installation on ARM-based systems

---

!!! note "Performance Considerations"
    KDB+ excels at time-series operations. Design your schemas and queries with columnar access patterns in mind for optimal performance.