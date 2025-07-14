# Reference
- [kx dashboard](https://code.kx.com/dashboards/gettingstarted/)
- [kx developer](https://code.kx.com/developer/getting-started/)

## cmd
- q)tables `. : returns a list of all tables in the root namespace
- .u.w is a dictionary


## update stock 
 -  stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$())

    row: flip `time`sym`price! (enlist .z.p; enlist `AAPL; enlist 189.3)

    stocks upsert row

stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$())
`stocks insert (.z.p; `APPL; 170.11)

---
stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$())
/ initialize tick if needed
\l tick/u.q
.u.init[]  / optional depending on setup

/ define the update function used by dashboards
.u.upd:{[table; data] insert[table; flip data]; u.pub[table; flip data];}
.u.snap:{stocks}

\t 1000  / every second call .z.ts
.z.ts:{ .u.pub[`stocks; .u.snap[`stocks]] }

// only contains latest 10 mins in the memory
q).z.ts:{ `stocks set delete from value `stocks where time < .z.p - 00:10:00.000 }
q)
q).z.ts:{ `stocks set delete from `stocks where time < .z.p - 00:10:00.000 }
q).z.ts[]   / manually call the function once
`stocks
q)\t 1000   / call every 1s

.z.ts:{  `stocks set select from stocks where i > (count  stocks) - 10 }
## update stock with java: polling

=== "java publisher"
     - java retrieve
         ```java
         private static void printStocks(c c) throws c.KException, IOException {
             // KDB+ query: select from stocks where time < .z.p, sorted by time descending
             String query = "xdesc[`time] select from stocks where time < .z.p";

             // Send query and receive result
             Object result_kdb = c.k(query);

             // Print result (will be a Dict or Table)
             System.out.println(result_kdb);

             Flip table = (Flip) result_kdb;
             String[] columnNames = table.x;
             Object[] columnData = table.y;

             int rowCount = Array.getLength(columnData[0]);

             for (int i = 0; i < rowCount; i++) {
             StringBuilder row = new StringBuilder();
             for (int j = 0; j < columnNames.length; j++) {
                 Object col = columnData[j];
                 Object value = Array.get(col, i);  // ✅ Use reflection-safe Array.get
                 row.append(columnNames[j]).append("=").append(value).append(" ");
             }
             System.out.println(row.toString());
             }
         }
         ```
     - java insert:
         ```java
         private  static void insertStock(c c, String sym, double price) throws c.KException, IOException {
             String query = String.format("`stocks insert (.z.p; `%s; %f)", sym, price);
             // Send query and receive result
             c.ks(query);
         }
         ```

=== "q subscriber"
    1.  start the q process with the port: `q -p 1234`
    2. 
    ```q
    / only need to define stream schema which is stock table
    stocks:([] time:`timestamp$(); sym:`symbol$(); price:`float$())
    /  timer (.z.ts) does trim stocks to the last 10 rows.
    .z.ts:{  `stocks set select from stocks where i > (count  stocks) - 10 }
    \t 1000 / this sets and activates timer (1 second interval)
    ```

=== "kx dashabord"
    1.  connect to the q process
    2. under `DataSource->kdb+/q` 
    ```q
    / retrieve data from the data source with only latest 10 records
    `time xdesc  10# select from stocks where time < .z.p
    ```
    3. choose `Subscription: Polling`; `Subscription: Force Reset`; Interval: `1s`; key: `Row Num`