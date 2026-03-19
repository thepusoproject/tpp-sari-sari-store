import os
import pytest

if os.getenv("RUN_MODULE_05") != "1":
    pytest.skip("Set RUN_MODULE_05=1 to enable Module 05 tests.", allow_module_level=True)

from tpp.strings import format_menu, sanitize_sku


def test_sanitize_sku_trims_and_uppercases():
    assert sanitize_sku("   Coke 500ml   ") == "COKE500ML"


def test_sanitize_sku_keeps_dashes_and_numbers():
    assert sanitize_sku("PiNE-apple Juice 1.5L!") == "PINE-APPLEJUICE15L"


def test_format_menu_renders_multiline_menu():
    menu = format_menu([
        {"name": "Coke 500ml", "price": 25.0},
        {"name": "Energen Chocolate", "price": 12.5},
    ])
    lines = [line for line in menu.splitlines() if line.strip()]
    assert lines[0] == "1) Coke 500ml — ₱25.00 (SKU: COKE500ML)"
    assert lines[1] == "2) Energen Chocolate — ₱12.50 (SKU: ENERGENCHOCOLATE)"
