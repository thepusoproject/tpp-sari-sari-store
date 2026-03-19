# Module 07 — Lists & Dictionaries

**Focus:** richer in-memory structures, aggregation, and lookups.

## Store upgrade
- Represent the cart as a list of dicts (`[{"sku": "CP-01", "qty": 2, ...}]`).
- Track suppliers + lead time in dictionaries for quick reference.
- Provide helper functions para mag-compute ng promos per cart line.

## Learning goals
- Nested structures + iteration patterns.
- Copy vs reference semantics (shallow vs deep copies).
- Comprehensions para gumawa ng filtered views (e.g., “low stock” list).

## Acceptance idea
- Tests may call `build_cart(items)` and `group_by_supplier(stock)`.
- Expect sorted output (use tuples or `OrderedDict`).

## Stretch ideas
- Allow bundling (buy 3, pay 2) computed via list transforms.
- Provide CLI command to print supplier reorder checklist.
