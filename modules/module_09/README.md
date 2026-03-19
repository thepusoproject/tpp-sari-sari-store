# Module 09 — Regex & Validation

**Focus:** regular expressions, pattern matching, defensive inputs.

## Store upgrade
- Support promo codes (`TPP-SAVE-2026`, `KAPITBAHAY-10PCT`).
- Parse receipt text (FOR REPRINT) to extract totals / cashier info.
- Validate customer contact info (mobile/email) for SMS receipts.

## Learning goals
- Python `re` module basics (`match`, `search`, `fullmatch`, groups).
- Building reusable validators + error messages.
- Sanitising free-form text before saving.

## Acceptance idea
- Tests will call `is_valid_promo(code)` and `parse_receipt(blob)` expecting dict output.
- CLI must show human-friendly errors when promo fails.

## Stretch ideas
- Auto-detect barangay/sitio from address string.
- Plug into an SMS gateway mock to send digital receipts.
