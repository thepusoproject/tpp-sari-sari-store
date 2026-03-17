import re
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = PROJECT_ROOT / "main.py"


def run_app(fake_input: str) -> str:
    """Execute python main.py with the provided stdin and return stdout."""
    if not ENTRYPOINT.exists():
        pytest.fail("main.py is missing — template expects it at the repo root.")

    completed = subprocess.run(
        [sys.executable, str(ENTRYPOINT)],
        input=fake_input,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout


def extract_number(label: str, text: str) -> float:
    pattern = rf"{label}\s*:\s*([-+]?\d+(?:\.\d+)?)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    assert match, f"Could not find numeric value for '{label}' in output."
    return float(match.group(1))


def test_receipt_flow_basic():
    output = run_app("Coke\n20\n3\n100\n")

    assert "receipt" in output.lower(), "Receipt header missing."
    assert "Item: Coke" in output, "Item name not echoed back." 

    price = extract_number("Price", output)
    qty = extract_number("Qty", output)
    total = extract_number("Total", output)
    cash = extract_number("Cash", output)
    change = extract_number("Change", output)

    assert price == pytest.approx(20.0)
    assert qty == pytest.approx(3.0)
    assert total == pytest.approx(price * qty)
    assert cash == pytest.approx(100.0)
    assert change == pytest.approx(cash - total)


def test_receipt_supports_decimals():
    output = run_app("Red Horse\n12.5\n2\n100\n")

    total = extract_number("Total", output)
    change = extract_number("Change", output)

    assert total == pytest.approx(25.0)
    assert change == pytest.approx(75.0)

    # Friendly formatting checks
    assert "Item: Red Horse" in output, "Item label missing or incorrect."
    assert "---" in output or "receipt" in output.lower(), "Receipt section not obvious."
