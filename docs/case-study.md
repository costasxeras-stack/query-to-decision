# Case study: Query to Decision

## The question

Olist connects small Brazilian shops to large online marketplaces. About one review in seven is 1 or 2 stars. A product team with limited capacity needs to know which problem, fixed first, removes the most bad experiences.

## Approach

Start from the outcome a marketplace cares about (bad reviews), split it by the biggest operational variable (did the order arrive on time), size each segment, then look for where the problem concentrates: time, place, seller, order type. Every number comes from a query on the page. One step, the promise simulation, uses Python because SQLite has no percentile function.

## Findings

### 1. Delivery decides the rating (confirmed)

Late orders get a bad review 62.4% of the time, on-time orders 9.3%. Late and undelivered orders are 9.4% of reviewed orders but 42.8% of bad reviews.

### 2. Speed is not the problem (confirmed)

Promises average 24.4 days, deliveries 12.5. Arriving 3 or more weeks early scores 4.29, no better than 1 to 2 weeks early (4.30).

### 3. Broken promises cluster by place, not by bad sellers (confirmed)

Rio de Janeiro has 12.8% of delivered orders and 22.9% of late ones. The 5% of sellers with most late orders handle 49.9% of orders and 58.7% of late orders, so lateness mostly follows volume.

### 4. Better estimates help only a little (confirmed)

On 2018 orders, a route-based promise of about the same length (23.2 against 23.4 days) is late 7.3% of the time against 7.7%. Cutting today's promises by 2 days raises lateness to 11.3%.

### 5. Multi-seller orders are a small, sharp problem (confirmed)

1.3% of orders, 47.4% bad reviews against 13.7% for single-seller orders.

### 6. Size of the prize (estimate)

If late orders were rated like on-time ones, bad reviews would fall from 14,486 to about 11,095 (−23%) and the average from 4.09 to 4.22. An upper bound that assumes lateness causes the bad rating.

### 7. Shorter, accurate promises may raise conversion (hypothesis)

The data has no checkout events, so this needs an A/B test.

## Decisions

### Run the real SQL in the browser, not screenshots of results

A SQL portfolio piece is usually a notebook or screenshots. Readers cannot check or change anything.

**Decision:** Ship a compressed SQLite file (5.2 MB) and sql.js, so every query runs live and can be edited. The same SQL file feeds the Python checks.

Full record: [decisions/0001-sql-in-the-browser.md](decisions/0001-sql-in-the-browser.md)

### Test the promise rule on later orders than it was built on

A delivery rule fitted and scored on the same orders always looks better than it is.

**Decision:** Fit route percentiles on 2016 to 2017 orders, score them on 2018 orders, and compare at equal promise length.

Full record: [decisions/0002-fit-on-past-test-on-future.md](decisions/0002-fit-on-past-test-on-future.md)

### Recommend route reliability first, estimates third

The obvious answer was better delivery estimates. The simulation showed they barely move lateness at equal promise length.

**Decision:** Rank actions by bad reviews they can remove: reliability on the worst routes, proactive messages on failed deliveries, then route-based estimates, then multi-parcel messaging.

Full record: [decisions/0003-reliability-over-estimates.md](decisions/0003-reliability-over-estimates.md)

## What I learned as a PM

- The first obvious fix (better estimates) was the weakest once tested on future orders. Testing before recommending changed the ranking.
- Rate and volume tell different stories. North-east states have the worst late rates, but Rio de Janeiro holds the most late orders.
- Ruling out a cause (bad sellers) is a finding too, and it saves a team from the wrong project.

## Limits

- Data from 2016 to 2018.
- Dates kept to the day, so late means a later calendar day than promised.
- Correlation: late delivery very likely causes bad ratings, but this data cannot prove it alone.
- No checkout data, so conversion effects are hypotheses.

## What I would do next

1. Bring back review text and classify the 57% of bad reviews on on-time orders
2. Add carrier data to separate route problems from seller dispatch delays
3. Design the A/B test for shorter, accurate promises at checkout

## My role

I framed the problem, made the product calls, checked every number and wrote the conclusions. 
