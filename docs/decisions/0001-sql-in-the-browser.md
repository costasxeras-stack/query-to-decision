# 0001: Run the real SQL in the browser, not screenshots of results

**Status:** accepted, 0.1.0

## Context

A SQL portfolio piece is usually a notebook or screenshots. Readers cannot check or change anything.

## Decision

Ship a compressed SQLite file (5.2 MB) and sql.js, so every query runs live and can be edited. The same SQL file feeds the Python checks.

## Tradeoff

- Anyone can verify every number, or ask a different question.
- A 5 MB download on first visit. The page shows progress, and the file is cached after.
- To fit, review text and payments were dropped. That rules out text analysis of the other 57% of bad reviews in this version.
