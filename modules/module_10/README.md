# Module 10 — APIs & JSON

**Focus:** HTTP requests, JSON APIs, and external data mash-ups.

## Store upgrade
- Fetch FX rates (USD→PHP) para sa imported items.
- Pull weather data para mag-trigger “rainy day” bundles.
- Publish a simple `/metrics` endpoint (FastAPI/Flask optional) or generate JSON reports.

## Learning goals
- `requests` basics, handling timeouts + retries.
- JSON schema design for exporting store metrics.
- Securely handling API keys via `.env` (never commit!).

## Acceptance idea
- Tests can stub HTTP responses (use `responses` library) to ensure proper parsing.
- CLI command `python main.py --fx <amount>` should show converted values using cached data.

## Stretch ideas
- Chain multiple APIs (e.g., barangay list + weather + FX) into one recommendation.
- Push metrics to a dashboard (even just writing JSON for the Gradeboard). 
