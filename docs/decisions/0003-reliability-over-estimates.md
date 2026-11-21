# 0003: Recommend route reliability first, estimates third

**Status:** accepted, 0.1.0

## Context

The obvious answer was better delivery estimates. The simulation showed they barely move lateness at equal promise length.

## Decision

Rank actions by bad reviews they can remove: reliability on the worst routes, proactive messages on failed deliveries, then route-based estimates, then multi-parcel messaging.

## Tradeoff

- Puts the hardest, highest-value work first.
- Reliability work needs carriers and operations, not only the product team.
- Each action comes with its own metric and guardrail.
