from __future__ import annotations

from io import StringIO
import pkgutil


def data_path(file_name: str):
    return pkgutil.get_data(__name__, f"data/{file_name}")


rom_symbols = {}


def _get_symbols():
    symbol_data = data_path("mzm_us_ap.map").decode("utf-8")
    with StringIO(symbol_data) as stream:
        while not next(stream).startswith(".rodata"):
            pass

        while not (line := next(stream)).startswith("OUTPUT"):
            splits = line.split()
            if len(splits) != 2:
                continue

            address, name = splits
            address = int(address[2:], base=16)
            rom_symbols[name] = address


_get_symbols()


def get_rom_symbol(symbol: str, offset: int = 0) -> int:
    """Convert a label name and offset to an address in GBA ROM."""

    return rom_symbols[symbol] + offset


def encode_str(msg: str) -> bytes:
    """Encode a string into Zero Mission's text format."""

    # TODO: Implement. Currently using UTF-16 LE as a placeholder
    return msg.encode("utf-16-le")
