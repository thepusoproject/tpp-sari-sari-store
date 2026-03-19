# Module 06 — Files & Persistence

**Focus:** reading/writing CSV/JSON and designing simple save/load flows.

## Store upgrade
- Gumawa ng `data/` folder na may daily sales log (`YYYY-MM-DD-sales.csv`).
- Save the inventory snapshot + cash-on-hand to `store_state.json` para puwedeng i-resume bukas.
- Add CLI commands: `python main.py --save` / `--restore`.

## Learning goals
- `pathlib` basics + safe file paths.
- CSV writer/reader vs JSON dumps/loads.
- Error handling kapag nawawala ang file o corrupt ang data.

## Acceptance idea (when unlocked)
- `python -m tests.module_06.test_persistence` targets `save_sales()` and `load_state()` inside `tpp/persistence.py`.
- Tests use temp folders, so functions must accept `pathlib.Path` objects and return the final path.
- CLI can wrap these helpers, but the helpers themselves must be pure/side-effect free except for filesystem writes.

## Stretch ideas
- Auto-archive old logs after X days.
- Allow exporting totals to Google Sheets via CSV.
