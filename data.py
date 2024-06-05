from __future__ import annotations

from io import StringIO
import itertools
import json
import pkgutil


def data_path(file_name: str):
    return pkgutil.get_data(__name__, f"data/{file_name}")


char_table = {}

ram_symbols = None
rom_symbols = None


def _get_symbols():
    global ram_symbols, rom_symbols

    symbol_data = data_path("extracted_symbols.json").decode("utf-8")
    symbols = json.loads(symbol_data)
    ram_symbols = symbols["iwram"]
    rom_symbols = symbols["rom"]


def _get_charmap():
    char_data = data_path("charmap.txt").decode("utf-8")
    with StringIO(char_data) as stream:
        for line in stream:
            splits = line.rsplit("=", 1)
            if len(splits) == 1:
                continue
            char, enc = map(str.strip, splits)
            if "'" not in char:
                continue
            char = char[1:-1]
            if char.startswith("\\"):
                char = char[1:]
            if len(char) != 1:
                continue  # TODO: Check if there are any multi-codepoint sequences and if we want to encode those
            enc = int(enc, 16).to_bytes(2, "little")
            char_table[char] = enc


_get_symbols()
_get_charmap()


def get_rom_symbol(symbol: str, offset: int = 0) -> int:
    """Convert a label name and offset to an address in GBA ROM."""

    return rom_symbols[symbol] + offset


def encode_str(msg: str) -> bytes:
    """Encode a string into Zero Mission's text format."""

    return bytes(itertools.chain.from_iterable(char_table.get(c, " ") for c in msg))
