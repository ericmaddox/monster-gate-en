#!/usr/bin/env python3
"""
tools/dump_font.py
Extracts the 640 font glyphs (16x16 2bpp) from Monster Gate (GBA) at ROM offset 0x4EDD1C.
Generates:
  - font/font_sheet.png (contact sheet of all 640 glyphs)
  - font/glyphs/*.png (individual glyphs)
  - font/raw_font.bin (extracted 40,960 bytes of font data)
"""

import os
from PIL import Image

FONT_OFFSET = 0x4EDD1C
NUM_GLYPHS = 640
BYTES_PER_GLYPH = 64  # 16 rows * 4 bytes/row (16x16 2bpp)

PALETTE = [
    (15, 15, 25),     # 0: Dark background
    (100, 100, 140),  # 1: Low highlight
    (180, 180, 220),  # 2: Mid highlight
    (255, 255, 255)   # 3: Bright text
]

def decode_glyph_2bpp(glyph_bytes):
    """Decodes 64 bytes of 16x16 2bpp data into a 16x16 list of pixel values (0-3)."""
    pixels = []
    for r in range(16):
        row_bytes = glyph_bytes[r * 4 : (r + 1) * 4]
        for b in row_bytes:
            for shift in (6, 4, 2, 0):
                pixels.append((b >> shift) & 3)
    return pixels

def main():
    os.makedirs("font/glyphs", exist_ok=True)
    
    rom_path = "rom/base.gba"
    if not os.path.exists(rom_path):
        rom_path = "0499 - Monster Gate (J)(Independent).gba"
        
    with open(rom_path, "rb") as f:
        f.seek(FONT_OFFSET)
        font_data = f.read(NUM_GLYPHS * BYTES_PER_GLYPH)

    with open("font/raw_font.bin", "wb") as f:
        f.write(font_data)

    print(f"Extracted {len(font_data)} bytes of font data ({NUM_GLYPHS} glyphs).")

    # Generate contact sheet: 32 columns x 20 rows
    cols = 32
    rows = (NUM_GLYPHS + cols - 1) // cols
    cell_w = 16
    cell_h = 16
    margin = 2
    
    sheet_w = cols * (cell_w + margin) + margin
    sheet_h = rows * (cell_h + margin) + margin
    
    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(30, 30, 40))

    for gid in range(NUM_GLYPHS):
        gbytes = font_data[gid * BYTES_PER_GLYPH : (gid + 1) * BYTES_PER_GLYPH]
        pix_vals = decode_glyph_2bpp(gbytes)

        g_img = Image.new("RGB", (16, 16))
        rgb_data = [PALETTE[p] for p in pix_vals]
        g_img.putdata(rgb_data)
        
        # Save individual glyph
        g_img.save(f"font/glyphs/{gid:03d}.png")

        # Paste onto contact sheet
        col = gid % cols
        row = gid // cols
        x = margin + col * (cell_w + margin)
        y = margin + row * (cell_h + margin)
        sheet.paste(g_img, (x, y))

    sheet.save("font/font_sheet.png")
    print("Saved font contact sheet to font/font_sheet.png")

if __name__ == "__main__":
    main()
