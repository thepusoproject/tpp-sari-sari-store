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
- Tests under `tests/module_06/test_persistence.py` will create temp dirs; expect functions `save_sales(entries, path)` and `load_state(path)`.
- CLI must print a success message showing the save location.

## Stretch ideas
- Auto-archive old logs after X days.
- Allow exporting totals to Google Sheets via CSV.
