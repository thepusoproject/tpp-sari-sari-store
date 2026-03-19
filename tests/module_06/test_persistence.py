import json
import os
import pytest

from tpp.persistence import load_state, save_sales

if os.getenv("RUN_MODULE_06") != "1":
    pytest.skip("Set RUN_MODULE_06=1 to enable Module 06 tests.", allow_module_level=True)


def test_save_sales_writes_csv(tmp_path):
    entries = [
        {"sku": "COKE500ML", "qty": 2, "price": 25.0},
        {"sku": "ENERGENCHOCO", "qty": 1, "price": 12.5},
    ]
    csv_path = save_sales(entries, tmp_path / "sales.csv")

    assert csv_path.exists(), "save_sales must return an existing CSV path."
    data = csv_path.read_text().strip().splitlines()
    assert data[0] == "sku,qty,price,total"
    assert "COKE500ML,2,25.0,50.0" in data[1]
    assert "ENERGENCHOCO,1,12.5,12.5" in data[2]


def test_load_state_reads_json(tmp_path):
    state = {
        "cash": 500.0,
        "inventory": [
            {"sku": "COKE500ML", "qty": 5},
            {"sku": "ENERGENCHOCO", "qty": 12},
        ],
    }
    path = tmp_path / "store_state.json"
    path.write_text(json.dumps(state, indent=2))

    loaded = load_state(path)
    assert loaded == state
