# Module 08 — Tuples & Sorting

**Focus:** stable sorting, ranking, immutability for trusted data.

## Store upgrade
- Gumawa ng leaderboard ng top 5 items per profitability.
- Freeze price rules using tuples (e.g., `(sku, promo_name, priority)`).
- Highlight “slow movers” (lowest sales in last 7 days).

## Learning goals
- `sorted(..., key=...)`, `heapq`, custom tuple ordering.
- When to prefer tuples vs lists (e.g., lock promo definitions).
- Format ranked output with ties handled gracefully.

## Acceptance idea
- Tests will feed synthetic sales data and expect lists of tuples.
- CLI command `python main.py --top` should print the ordered table.

## Stretch ideas
- Export the leaderboard to CSV for social posting.
- Allow user to choose metric (profit, quantity, margin).
