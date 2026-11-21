# 0002: Test the promise rule on later orders than it was built on

**Status:** accepted, 0.1.0

## Context

A delivery rule fitted and scored on the same orders always looks better than it is.

## Decision

Fit route percentiles on 2016 to 2017 orders, score them on 2018 orders, and compare at equal promise length.

## Tradeoff

- The gain reported is the gain on unseen orders, and it is small, which changed the recommendation.
- Percentiles need Python, so this one step is not live SQL. The script is linked.
