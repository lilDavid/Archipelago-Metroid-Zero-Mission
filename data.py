from __future__ import annotations

import hashlib
import json
import pkgutil


def data_path(file_name: str):
    data_bytes = pkgutil.get_data(__name__, f"data/{file_name}")
    assert data_bytes
    return data_bytes


symbols_hash = None
ram_symbols = None
rom_symbols = None


def _get_symbols():
    global ram_symbols, rom_symbols, symbols_hash

    symbol_data = data_path("extracted_symbols.json")
    hasher = hashlib.md5()
    hasher.update(symbol_data)
    symbols_hash = hasher.hexdigest()

    symbols = json.loads(symbol_data.decode("utf-8"))
    ram_symbols = symbols["ewram"] | symbols["iwram"]
    rom_symbols = symbols["rom"]


_get_symbols()
symbols = ram_symbols | rom_symbols


def get_symbol(symbol: str, offset: int = 0) -> int:
    """Convert a label name and offset to an address in GBA address space."""

    return symbols[symbol] + offset


def get_rom_address(ptr: str | int, offset=0):
    if isinstance(ptr, str):
        address = get_symbol(ptr, offset)
    else:
        address = ptr + offset
    if not address & 0x8000000:
        raise ValueError(f"{ptr}+{offset} is not in ROM (address: {address:07x})")
    return address & 0x8000000 - 1


APWORLD_VERSION: str | None = None
