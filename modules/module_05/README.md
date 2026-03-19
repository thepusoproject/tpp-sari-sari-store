# Module 05 — Strings & Cleaning

**Focus:** string methods, slicing, formatting, and user-facing prompts.

## Store upgrade
- Gawing “friendly” ang CLI menu (consistent casing, accent handling, emoji-safe output).
- Normalise SKU codes (no spaces, upper-case) para madaling i-compare sa inventory.
- Maglagay ng helper na nagbibigay ng Taglish hints kapag may typo ang user input.

## Learning goals
- `strip()`, `replace()`, `startswith()` at iba pang string tools.
- f-strings vs `.format()` para sa resibo at menus.
- Simple sanitizers (`slugify_item(name)`, `format_price(amount)`).

## Acceptance idea (when unlocked)
- `python -m tests.module_05.test_menu` will expect helpers inside `menu.py` + `validators.py`.
- Menu preview must be 100% deterministic (use fixtures for sample inventory).

## Stretch ideas
- Auto-suggest similar item names kapag may typo.
- Lokalise menu labels (English/Tagalog) via config file.
