#!/usr/bin/env python3

import itertools
from pathlib import Path
from PIL import Image


# This script converts a PNG image into the uncompressed 4bpp indexed format
# the GBA uses. To do that, it creates a .gfx file that contains the tile data
# and a .pal file that contains the palette.
#
# The image is converted into 8x8 pixel tiles, which are then stored in a 1D
# array format in row major order, as in the simplified example here:
#
# 00000000 44444444
# 11111111 55555555
# 22222222 66666666
# 33333333 77777777
#
# 88888888 CCCCCCCC
# 99999999 DDDDDDDD
# AAAAAAAA EEEEEEEE
# BBBBBBBB FFFFFFFF


def pixels_to_tiles(pixels: int):
    if pixels % 8 != 0:
        raise ValueError(f"Converting {pixels}px into 8px tiles")
    return pixels // 8


def gba_color(rgb_or_rgba: list[int]):
    r, g, b, *_ = map(lambda c: c >> 3, rgb_or_rgba)
    return r | g << 5 | b << 10


# https://docs.python.org/3.11/library/itertools.html
def batches(iterable, n):
    if n < 1:
        raise ValueError
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def convert_file(in_file: Path) -> tuple[bytes, bytes]:
    source_image = Image.open(in_file)

    if source_image.palette is None:
        raise ValueError(f"Image is not in indexed color format")
    max_color = max(source_image.palette.colors.values())
    if max_color >= 16:
        raise ValueError(f"Image has {max_color + 1} colors")

    width, height = map(pixels_to_tiles, source_image.size)
    pixels = []
    for row in range(height):
        for column in range(width):
            for y in range(8):
                for x in range(8):
                    color = source_image.getpixel((8 * column + x, 8 * row + y))
                    pixels.append(color)

    palette = map(gba_color, source_image.palette.colors.keys())

    gfx = bytes(map(lambda p: p[1] << 4 | p[0], batches(pixels, 2)))
    pal = b"".join(color.to_bytes(2, "little") for color in palette)
    pal += b"\x00" * (32 - len(pal))
    return gfx, pal


def main():
    graphics_dir = Path(__file__).parents[1] / "patcher/data/item_sprites"
    for file in graphics_dir.glob("*.png"):
        try:
            gfx, pal = convert_file(file)
            with open(file.with_suffix(".gfx"), "wb") as stream:
                stream.write(gfx)
            with open(file.with_suffix(".pal"), "wb") as stream:
                stream.write(pal)
        except Exception as e:
            print(f"Could not convert {file}: {e}")

    # TODO: Handle AP logo and unneeded palettes better than this

    with open(graphics_dir / "ap_logo.gfx", "rb") as stream:
        ap_logo_gfx = stream.read()
    with open(graphics_dir / "ap_logo.gfx", "wb") as stream:
        stream.write(ap_logo_gfx[:512])
    with open(graphics_dir / "ap_logo_progression.gfx", "wb") as stream:
        stream.write(ap_logo_gfx[512:1024])
    with open(graphics_dir / "ap_logo_useful.gfx", "wb") as stream:
        stream.write(ap_logo_gfx[1024:])

    (graphics_dir / "reserve_tank.pal").unlink()


if __name__ == "__main__":
    main()
