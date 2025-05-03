# Adding sprites

In order to convert properly and appear as expected, ensure the item sprites are saved as follows:

- 8-bit indexed color PNG format
- 16x64 size with four animation frames arranged vertically
- No alpha
  - This is due to a GIMP bug that adds an extra color to the palette when loading and exporting a transparent indexed PNG
- The palette is in the order it will appear in the patched ROM
  - No more than 16 colors
  - The order of the colors doesn't matter, except that the first color will be used as transparent
