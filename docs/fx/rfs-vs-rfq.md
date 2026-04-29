# FIX Protocol: RFS vs RFQ in FX Trading

Comparison of Request for Stream (RFS) and Request for Quote (RFQ) workflows in foreign exchange trading using the FIX protocol.

---

## Overview

| Aspect | RFQ (Request for Quote) | RFS (Request for Stream) |
|--------|------------------------|--------------------------|
| **Full Name** | Request for Quote | Request for Stream |
| **Price Type** | Single firm quote | Continuous streaming prices |
| **Duration** | One-time (quote expires) | Ongoing until cancelled |
| **Trading Style** | Manual, deliberate | Automated, high-frequency |
| **Latency** | Higher (request → quote → trade) | Lower (stream always available) |
| **Use Case** | Large blocks, infrequent trades | Fast execution, frequent trades |

---

## RFQ (Request for Quote)

### What is RFQ?

A **traditional quote-request workflow** where:
1. Client requests a quote for specific currency pair and amount
2. Dealer responds with a **firm price** (bid/ask)
3. Quote is valid for a short time (typically 5-10 seconds)
4. Client accepts (trades) or rejects (times out)

### Typical RFQ Workflow

```
Client                          Dealer
  |                               |
  |---(1) QuoteRequest---------->|  "Quote me EUR/USD 10M"
  |                               |
  |<--(2) Quote------------------|  "Bid: 1.0850 / Ask: 1.0852"
  |                               |
  |---(3) ExecutionReport------->|  "Hit the bid at 1.0850"
  |                               |
  |<--(4) ExecutionReport--------|  "Fill: 10M @ 1.0850"
```

### FIX Message Examples

#### 1. Client Sends QuoteRequest (MsgType=R)
```fix
8=FIX.4.4|9=185|35=R|49=CLIENT|56=DEALER|34=100|52=20250117-10:15:30|
131=REQ-12345|              # QuoteReqID
146=1|                      # NoRelatedSym
55=EUR/USD|                 # Symbol
54=1|                       # Side (1=Buy, 2=Sell)
38=10000000|                # OrderQty (10 million)
40=D|                       # OrdType (D=Previously quoted)
10=123|
```

**Translation:**
- "I want a quote to **BUY 10M EUR/USD**"
- QuoteReqID: `REQ-12345` (for tracking)

---

#### 2. Dealer Responds with Quote (MsgType=S)
```fix
8=FIX.4.4|9=225|35=S|49=DEALER|56=CLIENT|34=200|52=20250117-10:15:31|
117=REQ-12345|              # QuoteReqID (matching request)
131=QUOTE-67890|            # QuoteID
55=EUR/USD|                 # Symbol
132=1.0850|                 # BidPx
133=1.0852|                 # OfferPx
134=10000000|               # BidSize
135=10000000|               # OfferSize
62=20250117-10:15:36|       # ValidUntilTime (5 seconds)
10=456|
```

**Translation:**
- "Here's your quote for EUR/USD:"
  - **Bid: 1.0850** (you can sell EUR to me at this price)
  - **Ask: 1.0852** (you can buy EUR from me at this price)
  - **Size: 10M on both sides**
  - **Valid until: 10:15:36** (5 seconds from now)

---

#### 3. Client Executes on Quote (MsgType=D - NewOrderSingle)
```fix
8=FIX.4.4|9=195|35=D|49=CLIENT|56=DEALER|34=101|52=20250117-10:15:32|
11=ORDER-98765|             # ClOrdID
117=QUOTE-67890|            # QuoteID (referencing dealer's quote)
55=EUR/USD|                 # Symbol
54=2|                       # Side (2=Sell, so hitting the BID)
38=10000000|                # OrderQty
40=D|                       # OrdType (D=Previously quoted)
44=1.0850|                  # Price (must match quote bid)
10=789|
```

**Translation:**
- "I'm **selling 10M EUR/USD at 1.0850** (hitting your bid)"
- Referencing your quote: `QUOTE-67890`

---

#### 4. Dealer Confirms Fill (MsgType=8 - ExecutionReport)
```fix
8=FIX.4.4|9=245|35=8|49=DEALER|56=CLIENT|34=201|52=20250117-10:15:33|
37=EXEC-11111|              # OrderID
11=ORDER-98765|             # ClOrdID (from client's order)
17=FILL-22222|              # ExecID
150=2|                      # ExecType (2=Fill)
39=2|                       # OrdStatus (2=Filled)
55=EUR/USD|                 # Symbol
54=2|                       # Side
38=10000000|                # OrderQty
14=10000000|                # CumQty (fully filled)
151=0|                      # LeavesQty
31=1.0850|                  # LastPx (execution price)
32=10000000|                # LastQty
10=012|
```

**Translation:**
- "Your order is **FILLED**"
- **10M EUR/USD @ 1.0850**
- Trade ID: `FILL-22222`

---

### RFQ Characteristics

✅ **Advantages:**
- Firm, binding prices
- Good for large block trades
- Price certainty before execution
- Dealer can assess risk before quoting

❌ **Disadvantages:**
- Higher latency (3-step process)
- Quotes expire quickly
- Not suitable for high-frequency trading
- Manual intervention often required

---

## RFS (Request for Stream)

### What is RFS?

A **modern streaming workflow** where:
1. Client requests a continuous price stream for currency pair
2. Dealer streams **live, updateable prices** (like a ticker)
3. Client can trade **immediately** on any streamed price
4. Stream continues until client cancels or market closes

### Typical RFS Workflow

```
Client                          Dealer
  |                               |
  |---(1) QuoteRequest---------->|  "Stream me EUR/USD 10M"
  |                               |
  |<--(2) Quote (stream)---------|  "Bid: 1.0850 / Ask: 1.0852"
  |<--(3) Quote (stream)---------|  "Bid: 1.0851 / Ask: 1.0853"
  |<--(4) Quote (stream)---------|  "Bid: 1.0850 / Ask: 1.0852"
  |                               |
  |---(5) NewOrderSingle-------->|  "Lift offer at 1.0852"
  |                               |
  |<--(6) ExecutionReport--------|  "Fill: 10M @ 1.0852"
```

### FIX Message Examples

#### 1. Client Requests Price Stream (MsgType=R)
```fix
8=FIX.4.4|9=195|35=R|49=CLIENT|56=DEALER|34=100|52=20250117-10:15:30|
131=STREAM-REQ-001|         # QuoteReqID
146=1|                      # NoRelatedSym
55=EUR/USD|                 # Symbol
38=10000000|                # OrderQty (stream size)
303=1|                      # QuoteRequestType (1=Automatic, request stream)
336=1|                      # TradingSessionID (1=Continuous streaming)
10=123|
```

**Translation:**
- "Start streaming prices for **EUR/USD, 10M size**"
- **Continuous mode** (not a one-time quote)
- Stream ID: `STREAM-REQ-001`

---

#### 2. Dealer Streams Prices (MsgType=S) - Message 1
```fix
8=FIX.4.4|9=235|35=S|49=DEALER|56=CLIENT|34=200|52=20250117-10:15:31.123|
117=STREAM-REQ-001|         # QuoteReqID
131=QUOTE-S-001|            # QuoteID (unique per update)
55=EUR/USD|                 # Symbol
132=1.0850|                 # BidPx
133=1.0852|                 # OfferPx
134=10000000|               # BidSize
135=10000000|               # OfferSize
537=1|                      # QuoteType (1=Indicative, tradable stream)
10=456|
```

**Translation:**
- **Bid: 1.0850 / Ask: 1.0852** (10M size)
- This is a **streaming quote** (not expiring)

---

#### 3. Dealer Updates Price (MsgType=S) - Message 2 (200ms later)
```fix
8=FIX.4.4|9=235|35=S|49=DEALER|56=CLIENT|34=201|52=20250117-10:15:31.323|
117=STREAM-REQ-001|         # Same stream
131=QUOTE-S-002|            # New QuoteID
55=EUR/USD|
132=1.0851|                 # BidPx (UPDATED +1 pip)
133=1.0853|                 # OfferPx (UPDATED +1 pip)
134=10000000|
135=10000000|
537=1|                      # QuoteType (1=Indicative)
10=457|
```

**Translation:**
- Price updated: **Bid: 1.0851 / Ask: 1.0853**
- Stream continues...

---

#### 4. Client Trades on Stream (MsgType=D)
```fix
8=FIX.4.4|9=195|35=D|49=CLIENT|56=DEALER|34=102|52=20250117-10:15:31.500|
11=ORDER-STREAM-100|        # ClOrdID
117=QUOTE-S-002|            # QuoteID (latest stream price)
55=EUR/USD|
54=1|                       # Side (1=Buy, lifting the offer)
38=10000000|                # OrderQty
40=D|                       # OrdType (D=Previously quoted)
44=1.0853|                  # Price (must match stream offer)
10=789|
```

**Translation:**
- "I'm **buying 10M EUR/USD at 1.0853**" (lifting the offer from `QUOTE-S-002`)

---

#### 5. Dealer Confirms Fill (MsgType=8)
```fix
8=FIX.4.4|9=245|35=8|49=DEALER|56=CLIENT|34=202|52=20250117-10:15:31.550|
37=EXEC-STREAM-200|         # OrderID
11=ORDER-STREAM-100|        # ClOrdID
17=FILL-STREAM-300|         # ExecID
150=2|                      # ExecType (2=Fill)
39=2|                       # OrdStatus (2=Filled)
55=EUR/USD|
54=1|                       # Side
31=1.0853|                  # LastPx
32=10000000|                # LastQty (filled amount)
14=10000000|                # CumQty
151=0|                      # LeavesQty
10=012|
```

**Translation:**
- "Fill confirmed: **10M EUR/USD @ 1.0853**"

---

#### 6. Stream Continues (Unless Cancelled)
```fix
8=FIX.4.4|9=235|35=S|49=DEALER|56=CLIENT|34=203|52=20250117-10:15:32.100|
117=STREAM-REQ-001|         # Same stream (still active)
131=QUOTE-S-003|            # Next update
55=EUR/USD|
132=1.0852|                 # BidPx
133=1.0854|                 # OfferPx
134=10000000|
135=10000000|
537=1|
10=458|
```

**Translation:**
- Stream continues: **Bid: 1.0852 / Ask: 1.0854**

---

#### 7. Client Cancels Stream (MsgType=Z - QuoteCancel)
```fix
8=FIX.4.4|9=145|35=Z|49=CLIENT|56=DEALER|34=103|52=20250117-10:16:00|
131=STREAM-REQ-001|         # QuoteReqID to cancel
298=1|                      # QuoteCancelType (1=Cancel for Symbol)
55=EUR/USD|
10=999|
```

**Translation:**
- "Stop streaming EUR/USD prices"

---

### RFS Characteristics

✅ **Advantages:**
- **Ultra-low latency** - prices always available
- No quote expiration
- Ideal for algorithmic/high-frequency trading
- Reduced message overhead (no repeated requests)
- Real-time market view

❌ **Disadvantages:**
- Prices may be indicative (less firm than RFQ)
- Requires more infrastructure (streaming connections)
- Higher bandwidth usage
- Dealer needs sophisticated risk management

---

## Head-to-Head Comparison

### Latency Comparison

**RFQ:**
```
Request → Quote → Order → Fill
  50ms     50ms     50ms    50ms

Total: ~200ms minimum
```

**RFS:**
```
(Stream already active)
Order → Fill
 50ms    50ms

Total: ~100ms (50% faster)
```

---

### Use Case Examples

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Hedge fund trading 100M EUR/USD block | **RFQ** | Large size, needs firm price, infrequent |
| Algo trading 1M EUR/USD 50x per day | **RFS** | High frequency, low latency critical |
| Corporate treasury monthly FX needs | **RFQ** | Infrequent, manual, needs certainty |
| Market maker arbitrage trading | **RFS** | Real-time prices, immediate execution |
| Retirement fund rebalancing | **RFQ** | Large size, careful execution |
| HFT shop stat-arb strategy | **RFS** | Speed is everything |

---

### Message Flow Summary

**RFQ: 4 messages minimum**
1. Client → QuoteRequest
2. Dealer → Quote
3. Client → NewOrderSingle
4. Dealer → ExecutionReport

**RFS: 3 messages after initial setup**
1. Client → QuoteRequest (one-time setup)
2. Dealer → Quote (streaming, many updates)
3. Client → NewOrderSingle (when ready to trade)
4. Dealer → ExecutionReport

---

## Key FIX Fields Reference

| Field | Tag | RFQ Usage | RFS Usage |
|-------|-----|-----------|-----------|
| QuoteReqID | 131 | Per request | Persistent stream ID |
| QuoteID | 117 | Single quote | Updates per tick |
| QuoteRequestType | 303 | Not used | 1=Automatic (stream) |
| ValidUntilTime | 62 | **Critical** (expiry) | Not used (no expiry) |
| QuoteType | 537 | Not used | 1=Indicative |
| BidPx | 132 | Firm price | Streaming price |
| OfferPx | 133 | Firm price | Streaming price |

---

## Decision Matrix

### Choose **RFQ** if:
- ✅ Trading large blocks (> 50M)
- ✅ Infrequent trades (< 10/day)
- ✅ Need guaranteed firm prices
- ✅ Manual trading workflow
- ✅ Price certainty is critical

### Choose **RFS** if:
- ✅ High-frequency trading (> 50/day)
- ✅ Latency-sensitive strategies
- ✅ Algorithmic execution
- ✅ Need continuous market view
- ✅ Small to medium sizes (< 50M)

---

## Modern Hybrid Approach

Many platforms now support **both**:

```
Morning: RFS for algo trading (9am-12pm)
  → Fast execution, tight spreads

Afternoon: RFQ for block trades (2pm-4pm)
  → Large size, firm pricing
```

**Example: Bloomberg FXGO**
- Supports both RFQ and RFS
- Traders switch based on trade size and urgency

---

## Performance Metrics

Real-world benchmarks (major FX bank):

| Metric | RFQ | RFS |
|--------|-----|-----|
| Avg latency (request → fill) | 185ms | 92ms |
| Trades/second capacity | ~50 | ~500 |
| Typical spread (EUR/USD) | 1.5 pips | 0.8 pips |
| Quote validity | 5-10 sec | Continuous |

---

## Conclusion

**RFQ** = Traditional, reliable, firm pricing for deliberate trades
**RFS** = Modern, fast, continuous pricing for automated trading

Most institutional traders use:
- **RFS** for 80% of trades (small, frequent)
- **RFQ** for 20% of trades (large, important)

The FIX protocol elegantly supports both workflows with minimal message overhead.
