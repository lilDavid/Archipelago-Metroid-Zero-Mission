from __future__ import annotations

import json
import pkgutil


def data_path(file_name: str):
    data_bytes = pkgutil.get_data(__name__, f"data/{file_name}")
    assert data_bytes
    return data_bytes


ram_symbols = None
rom_symbols = None


def _get_symbols():
    global ram_symbols, rom_symbols

    symbol_data = data_path("extracted_symbols.json")
    symbols = json.loads(symbol_data.decode("utf-8"))
    ram_symbols = symbols["ewram"] | symbols["iwram"]
    rom_symbols = symbols["rom"]


_get_symbols()
symbols = ram_symbols | rom_symbols


def get_symbol(symbol: str, offset: int = 0) -> int:
    """Convert a label name and offset to an address in GBA address space."""

    return symbols[symbol] + offset


APWORLD_VERSION: str | None = None
