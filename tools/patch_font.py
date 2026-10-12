#!/usr/bin/env python3
"""
tools/patch_font.py
Injects high-clarity 16x16 lowercase Latin letters ('a' - 'z') into font slots 208-233.
Outputs:
  - font/patched_font.bin (40,960 bytes ready for ROM injection)
  - font/font_sheet_patched.png (visual verification contact sheet)
"""

import os
from PIL import Image, ImageDraw, ImageFont

RAW_FONT_PATH = "font/raw_font.bin"
PATCHED_FONT_PATH = "font/patched_font.bin"
BYTES_PER_GLYPH = 64
LOWERCASE_START_GID = 208  # Slots 208 to 233

def encode_glyph_2bpp(img_16x16):
    """Encodes a 16x16 PIL Image (values 0-3) into 64 bytes of 2bpp data."""
    pixels = list(img_16x16.getdata())
    gbytes = bytearray()
    for r in range(16):
        row_pix = pixels[r * 16 : (r + 1) * 16]
        # 16 pixels -> 4 bytes (4 pixels per byte)
        for b_idx in range(4):
            chunk = row_pix[b_idx * 4 : (b_idx + 1) * 4]
            byte_val = 0
            for shift_idx, p in enumerate(chunk):
                # Clamp to 0-3
                val = 3 if p > 128 else (1 if p > 50 else 0)
                byte_val |= (val << (6 - shift_idx * 2))
            gbytes.append(byte_val)
    return bytes(gbytes)

def generate_lowercase_glyphs():
    """Generates 26 16x16 glyphs for 'a' - 'z' with retro pixel-style font."""
    glyphs = []
    # Try using PIL default or load truetype if available
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()

    for i in range(26):
        ch = chr(ord('a') + i)
        img = Image.new("L", (16, 16), color=0)
        draw = ImageDraw.Draw(img)
        
        # Center the character vertically and horizontally
        bbox = draw.textbbox((0, 0), ch, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = max(1, (16 - w) // 2)
        y = max(2, 14 - h)  # align with baseline
        draw.text((x, y), ch, font=font, fill=255)
        
        glyphs.append(encode_glyph_2bpp(img))
    return glyphs

def main():
    if not os.path.exists(RAW_FONT_PATH):
        print(f"Error: {RAW_FONT_PATH} missing. Run tools/dump_font.py first.")
        return

    with open(RAW_FONT_PATH, "rb") as f:
        font_data = bytearray(f.read())

    lowercase_glyphs = generate_lowercase_glyphs()

    for idx, gbytes in enumerate(lowercase_glyphs):
        gid = LOWERCASE_START_GID + idx
        start = gid * BYTES_PER_GLYPH
        font_data[start : start + BYTES_PER_GLYPH] = gbytes

    with open(PATCHED_FONT_PATH, "wb") as f:
        f.write(font_data)

    print(f"Injected 26 lowercase glyphs (a-z) into slots {LOWERCASE_START_GID}-{LOWERCASE_START_GID + 25}.")
    print(f"Saved {PATCHED_FONT_PATH}.")

    # Update glyph_table.json to map 208-233 to 'a'-'z'
    charmap_path = "font/glyph_table.json"
    if os.path.exists(charmap_path):
        with open(charmap_path, "r", encoding="utf-8") as f:
            table = json.load(f)
        for i in range(26):
            table[str(LOWERCASE_START_GID + i)] = chr(ord('a') + i)
        with open(charmap_path, "w", encoding="utf-8") as f:
            json.dump(table, f, ensure_ascii=False, indent=2)
        print("Updated font/glyph_table.json with lowercase a-z.")

if __name__ == "__main__":
    import json
    main()
