#!/usr/bin/env python3
"""
tools/patch_naming_screen.py
Translates the character naming screen to English:
1. Injects English keyboard graphics into the GBA tile bank (uppercase, lowercase, symbols).
2. Blanks out Japanese dakuten and handakuten side buttons.
3. Updates BG0 tilemap (0x0C9780) and clears BG1 tilemap (0x0C9C80).
4. Sets tile bank transfer to uncompressed (algo = 0) at 0x0C9258.
5. Injects the 60-byte English keyboard lookup matrix at 0x09F1AC.
6. Injects 30 default English player names at 0x09F21A.
7. Recalculates ROM checksum.
"""

import os
import struct
import sys
from PIL import Image
from fix_checksum import fix_checksum

BASE_ROM_PATH = "rom/base.gba"
TARGET_ROM_PATH = "rom/monster_gate_en.gba"
KEYBOARD_TILES_PATH = "graphics/keyboard_tiles.bin"

TILES_EXPANDED_OFFSET = 0x880000  # ROM file offset 0x880000
TILES_GBA_ADDR = 0x08000000 + TILES_EXPANDED_OFFSET

DESCRIPTOR_OFFSET = 0x0C9258
BG0_TILEMAP_OFFSET = 0x0C9780
BG1_TILEMAP_OFFSET = 0x0C9C80
KEYBOARD_MATRIX_OFFSET = 0x09F1AC
DEFAULT_NAMES_OFFSET = 0x09F21A

BANK_SIZE = 29536  # 923 tiles * 32 bytes

FONT_5x7 = {
    'A': [' ### ', '#   #', '#   #', '#####', '#   #', '#   #', '#   #'],
    'B': ['#### ', '#   #', '#   #', '#### ', '#   #', '#   #', '#### '],
    'C': [' ####', '#    ', '#    ', '#    ', '#    ', '#    ', ' ####'],
    'D': ['#### ', '#   #', '#   #', '#   #', '#   #', '#   #', '#### '],
    'E': ['#####', '#    ', '#    ', '#### ', '#    ', '#    ', '#####'],
    'F': ['#####', '#    ', '#    ', '#### ', '#    ', '#    ', '#    '],
    'G': [' ####', '#    ', '#    ', '# ###', '#   #', '#   #', ' ### '],
    'H': ['#   #', '#   #', '#   #', '#####', '#   #', '#   #', '#   #'],
    'I': ['#####', '  #  ', '  #  ', '  #  ', '  #  ', '  #  ', '#####'],
    'J': ['  ###', '    #', '    #', '    #', '#   #', '#   #', ' ### '],
    'K': ['#   #', '#  # ', '# #  ', '##   ', '# #  ', '#  # ', '#   #'],
    'L': ['#    ', '#    ', '#    ', '#    ', '#    ', '#    ', '#####'],
    'M': ['#   #', '## ##', '# # #', '#   #', '#   #', '#   #', '#   #'],
    'N': ['#   #', '##  #', '# # #', '#  ##', '#   #', '#   #', '#   #'],
    'O': [' ### ', '#   #', '#   #', '#   #', '#   #', '#   #', ' ### '],
    'P': ['#### ', '#   #', '#   #', '#### ', '#    ', '#    ', '#    '],
    'Q': [' ### ', '#   #', '#   #', '#   #', '# # #', '#  # ', ' ## #'],
    'R': ['#### ', '#   #', '#   #', '#### ', '# #  ', '#  # ', '#   #'],
    'S': [' ####', '#    ', '#    ', ' ### ', '    #', '    #', '#### '],
    'T': ['#####', '  #  ', '  #  ', '  #  ', '  #  ', '  #  ', '  #  '],
    'U': ['#   #', '#   #', '#   #', '#   #', '#   #', '#   #', ' ### '],
    'V': ['#   #', '#   #', '#   #', '#   #', ' # # ', ' # # ', '  #  '],
    'W': ['#   #', '#   #', '#   #', '# # #', '# # #', '## ##', '#   #'],
    'X': ['#   #', ' # # ', '  #  ', '  #  ', '  #  ', ' # # ', '#   #'],
    'Y': ['#   #', '#   #', ' # # ', '  #  ', '  #  ', '  #  ', '  #  '],
    'Z': ['#####', '    #', '   # ', '  #  ', ' #   ', '#    ', '#####'],
    'a': ['     ', ' ### ', '    #', ' ####', '#   #', '#   #', ' ####'],
    'b': ['#    ', '#    ', '#### ', '#   #', '#   #', '#   #', '#### '],
    'c': ['     ', '     ', ' ####', '#    ', '#    ', '#    ', ' ####'],
    'd': ['    #', '    #', ' ####', '#   #', '#   #', '#   #', ' ####'],
    'e': ['     ', ' ### ', '#   #', '#####', '#    ', '#    ', ' ####'],
    'f': ['  ## ', ' #   ', '###  ', ' #   ', ' #   ', ' #   ', ' #   '],
    'g': ['     ', ' ####', '#   #', '#   #', ' ####', '    #', '#### '],
    'h': ['#    ', '#    ', '#### ', '#   #', '#   #', '#   #', '#   #'],
    'i': ['  #  ', '     ', ' ##  ', '  #  ', '  #  ', '  #  ', ' ### '],
    'j': ['   # ', '     ', '   # ', '   # ', '   # ', '#  # ', ' ##  '],
    'k': ['#    ', '#  # ', '# #  ', '##   ', '# #  ', '#  # ', '#   #'],
    'l': [' ##  ', '  #  ', '  #  ', '  #  ', '  #  ', '  #  ', ' ### '],
    'm': ['     ', '     ', '## # ', '# # #', '# # #', '#   #', '#   #'],
    'n': ['     ', '     ', '#### ', '#   #', '#   #', '#   #', '#   #'],
    'o': ['     ', '     ', ' ### ', '#   #', '#   #', '#   #', ' ### '],
    'p': ['     ', '#### ', '#   #', '#   #', '#### ', '#    ', '#    '],
    'q': ['     ', ' ####', '#   #', '#   #', ' ####', '    #', '    #'],
    'r': ['     ', '     ', '# ## ', '##  #', '#    ', '#    ', '#    '],
    's': ['     ', ' ####', '#    ', ' ### ', '    #', '    #', '#### '],
    't': [' #   ', '###  ', ' #   ', ' #   ', ' #   ', ' #  #', '  ## '],
    'u': ['     ', '     ', '#   #', '#   #', '#   #', '#   #', ' ### '],
    'v': ['     ', '     ', '#   #', '#   #', ' # # ', ' # # ', '  #  '],
    'w': ['     ', '     ', '#   #', '# # #', '# # #', '## ##', '#   #'],
    'x': ['     ', '     ', '#   #', ' # # ', '  #  ', ' # # ', '#   #'],
    'y': ['     ', '#   #', '#   #', ' ####', '    #', '#   #', ' ### '],
    'z': ['     ', '#####', '   # ', '  #  ', ' #   ', '#    ', '#####'],
    '-': ['     ', '     ', '     ', '#####', '     ', '     ', '     '],
    '!': ['  #  ', '  #  ', '  #  ', '  #  ', '  #  ', '     ', '  #  '],
    '?': [' ### ', '#   #', '    #', '  ## ', '  #  ', '     ', '  #  '],
    '.': ['     ', '     ', '     ', '     ', '     ', ' ##  ', ' ##  '],
    ',': ['     ', '     ', '     ', '     ', '     ', '  #  ', ' #   '],
    ':': ['     ', ' ##  ', ' ##  ', '     ', ' ##  ', ' ##  ', '     '],
    '/': ['    #', '   # ', '   # ', '  #  ', ' #   ', ' #   ', '#    '],
    ' ': ['     ', '     ', '     ', '     ', '     ', '     ', '     '],
}

KEYBOARD_GRID = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
    ['M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
    ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'],
    ['w', 'x', 'y', 'z', '-', '!', '?', '.', ',', ':', '/', ' '],
]

DEFAULT_NAMES = [
    'CLAUD', 'MINA',  'ZAIN',  'SAPH',  'ARES',
    'ANIS',  'FEATH', 'LEAF',  'VELIS', 'VAL',
    'RAI',   'LAILA', 'LARK',  'LILY',  'RICK',
    'ILUA',  'ALLEN', 'FLUTE', 'GOLD',  'ROSA',
    'ZEOT',  'RAIN',  'KEN',   'FUMM',  'PULSE',
    'KARIN', 'RYSEL', 'SELTA', 'JUSTA', 'SILK'
]

def glyph_of(ch):
    if 'A' <= ch <= 'Z':
        return 161 + ord(ch) - ord('A')
    if 'a' <= ch <= 'z':
        return 208 + ord(ch) - ord('a')
    syms = {
        '-': 199,
        '!': 201,
        '?': 200,
        '.': 202,
        ',': 203,
        ':': 204,
        '/': 205,
        ' ': 197
    }
    return syms[ch]

def decompress_keyboard_tiles_unicorn():
    import unicorn
    from unicorn import arm_const
    with open(BASE_ROM_PATH, 'rb') as f:
        rom_data = f.read()

    uc = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_THUMB)
    ROM_BASE = 0x08000000
    uc.mem_map(ROM_BASE, 16 * 1024 * 1024)
    uc.mem_write(ROM_BASE, rom_data)
    uc.mem_map(0x02000000, 256 * 1024)
    uc.mem_map(0x03000000, 32 * 1024)
    uc.mem_map(0x04000000, 4 * 1024)
    uc.mem_map(0x05000000, 4 * 1024)
    uc.mem_map(0x06000000, 128 * 1024)
    uc.mem_map(0x07000000, 4 * 1024)
    uc.reg_write(arm_const.UC_ARM_REG_SP, 0x03007FA0)
    uc.reg_write(arm_const.UC_ARM_REG_LR, 0x08000001)
    uc.hook_add(unicorn.UC_HOOK_INTR, lambda u, i, d: None)
    uc.reg_write(arm_const.UC_ARM_REG_R0, 0x080C9258)
    uc.reg_write(arm_const.UC_ARM_REG_R1, 0x06000000)
    uc.emu_start(0x0801B8F0 | 1, 0x08000000, timeout=10000000)
    tiles = uc.mem_read(0x06000000, BANK_SIZE)
    os.makedirs(os.path.dirname(KEYBOARD_TILES_PATH), exist_ok=True)
    with open(KEYBOARD_TILES_PATH, 'wb') as f:
        f.write(tiles)
    return tiles

def patch_naming_screen():
    print("=== Patching Character Naming Screen to English ===")

    if not os.path.exists(KEYBOARD_TILES_PATH):
        print(f"Extracting keyboard tiles with Unicorn from {BASE_ROM_PATH}...")
        raw_tiles = decompress_keyboard_tiles_unicorn()
    else:
        with open(KEYBOARD_TILES_PATH, 'rb') as f:
            raw_tiles = f.read()

    with open(BASE_ROM_PATH, 'rb') as f:
        base_rom = f.read()

    # Load palette 3
    pal_raw = base_rom[0x0C59C4:0x0C59C4+128]
    colors = struct.unpack('<64H', pal_raw)
    pal_rgb = []
    for c in colors:
        r = (c & 0x1F) << 3
        g = ((c >> 5) & 0x1F) << 3
        b = ((c >> 10) & 0x1F) << 3
        pal_rgb.append((r, g, b))
    pal3 = pal_rgb[3*16:4*16]

    # Render base BG0 image
    tm0_orig = struct.unpack('<640H', base_rom[0x0C9780:0x0C9780+1280])
    bg0 = Image.new('RGB', (256, 160))
    pixels = bg0.load()
    for r in range(20):
        for c in range(32):
            entry = tm0_orig[r * 32 + c]
            t_idx = entry & 0x3FF
            hflip = bool(entry & 0x400)
            vflip = bool(entry & 0x800)
            pal_num = (entry >> 12) & 0x0F
            if t_idx < len(raw_tiles) // 32:
                t_bytes = raw_tiles[t_idx*32:(t_idx+1)*32]
                for py in range(8):
                    y = 7 - py if vflip else py
                    for px in range(8):
                        x = 7 - px if hflip else px
                        byte = t_bytes[py * 4 + px // 2]
                        color_num = (byte >> 4) if (px % 2 == 1) else (byte & 0x0F)
                        if color_num != 0:
                            pixels[c * 8 + x, r * 8 + y] = pal_rgb[pal_num * 16 + color_num]

    # Blank button template in BG0 (16x16) at Row 4, Col 11 (X=184, Y=136)
    blank_btn = bg0.crop((184, 136, 200, 152))

    # Create edited keyboard graphic
    final_img = bg0.copy()

    # 1. Stamp 60 buttons with English font
    for r in range(5):
        for c in range(12):
            bx = c * 16 + 8
            by = r * 20 + 56
            final_img.paste(blank_btn, (bx, by))
            ch = KEYBOARD_GRID[r][c]
            glyph = FONT_5x7[ch]
            for gy, row_str in enumerate(glyph):
                for gx, ch_pix in enumerate(row_str):
                    if ch_pix == '#':
                        final_img.putpixel((bx + 5 + gx, by + 8 + gy), (0, 0, 0))

    # 2. Blank dakuten and handakuten side buttons
    face_col = pal3[4]  # RGB(248, 168, 40)
    for y in range(64, 76):
        for x in range(214, 227):
            final_img.putpixel((x, y), face_col)

    for y in range(88, 100):
        for x in range(214, 227):
            final_img.putpixel((x, y), face_col)

    # 3. Decompose image into 4bpp 8x8 tiles and generate new BG0 tilemap
    def rgb_to_idx(rgb):
        for idx, c in enumerate(pal3):
            if c == rgb:
                return idx
        dists = [sum((a - b)**2 for a, b in zip(rgb, c)) for c in pal3]
        return dists.index(min(dists))

    unique_tiles = [bytes(32)]
    tile_dict = {bytes(32): 0}
    new_tm0 = []

    for r in range(20):
        for c in range(32):
            block = final_img.crop((c*8, r*8, (c+1)*8, (r+1)*8))
            tbytes = bytearray(32)
            for py in range(8):
                for px in range(0, 8, 2):
                    low = rgb_to_idx(block.getpixel((px, py))) & 0x0F
                    high = rgb_to_idx(block.getpixel((px + 1, py))) & 0x0F
                    tbytes[py * 4 + px // 2] = low | (high << 4)
            tbytes = bytes(tbytes)
            if tbytes not in tile_dict:
                tile_dict[tbytes] = len(unique_tiles)
                unique_tiles.append(tbytes)
            pal_num = 2 if r < 7 and tile_dict[tbytes] != 0 else 3
            new_tm0.append(tile_dict[tbytes] | (pal_num << 12))

    print(f"Generated {len(unique_tiles)} unique tiles for English keyboard.")

    # Prepare uncompressed 29,536-byte tile bank
    bank_data = bytearray(BANK_SIZE)
    for i, t in enumerate(unique_tiles):
        bank_data[i*32:(i+1)*32] = t

    # 4. Generate 60-byte keyboard matrix table
    matrix_data = bytearray(60)
    for c in range(12):
        for r in range(5):
            ch = KEYBOARD_GRID[r][c]
            matrix_data[c * 5 + r] = glyph_of(ch)

    # 5. Generate 150-byte default names table
    names_data = bytearray()
    for name in DEFAULT_NAMES:
        entry = bytearray(5)
        for i, ch in enumerate(name):
            entry[i] = 161 + ord(ch.upper()) - ord('A')
        for i in range(len(name), 5):
            entry[i] = 0xFF
        names_data.extend(entry)

    # 6. Apply patches to TARGET_ROM_PATH
    if not os.path.exists(TARGET_ROM_PATH):
        print(f"Error: {TARGET_ROM_PATH} not found.")
        sys.exit(1)

    with open(TARGET_ROM_PATH, 'rb') as f:
        rom = bytearray(f.read())

    # Ensure expanded space is allocated
    if len(rom) < TILES_EXPANDED_OFFSET + BANK_SIZE:
        rom.extend(b'\xFF' * (TILES_EXPANDED_OFFSET + BANK_SIZE - len(rom)))

    # Inject uncompressed tile bank
    rom[TILES_EXPANDED_OFFSET:TILES_EXPANDED_OFFSET + len(bank_data)] = bank_data
    print(f"Injected {len(bank_data)} bytes of keyboard tile bank at offset 0x{TILES_EXPANDED_OFFSET:06X} (ROM 0x{TILES_GBA_ADDR:08X}).")

    # Update descriptor at 0x0C9258
    struct.pack_into('<III', rom, DESCRIPTOR_OFFSET, TILES_GBA_ADDR, BANK_SIZE, 0)
    print(f"Updated graphic descriptor at 0x{DESCRIPTOR_OFFSET:06X}: source=0x{TILES_GBA_ADDR:08X}, size={BANK_SIZE}, algo=0.")

    # Write new BG0 tilemap (1280 bytes)
    tm0_bytes = struct.pack(f'<{len(new_tm0)}H', *new_tm0)
    rom[BG0_TILEMAP_OFFSET:BG0_TILEMAP_OFFSET + len(tm0_bytes)] = tm0_bytes
    print(f"Updated BG0 tilemap at 0x{BG0_TILEMAP_OFFSET:06X} ({len(tm0_bytes)} bytes).")

    # Clear BG1 tilemap (1280 bytes)
    rom[BG1_TILEMAP_OFFSET:BG1_TILEMAP_OFFSET + 1280] = b'\x00' * 1280
    print(f"Cleared BG1 tilemap at 0x{BG1_TILEMAP_OFFSET:06X} (1280 bytes of 0x00).")

    # Write keyboard matrix
    rom[KEYBOARD_MATRIX_OFFSET:KEYBOARD_MATRIX_OFFSET + len(matrix_data)] = matrix_data
    print(f"Injected 60-byte English keyboard matrix at 0x{KEYBOARD_MATRIX_OFFSET:06X}.")

    # Write default names
    rom[DEFAULT_NAMES_OFFSET:DEFAULT_NAMES_OFFSET + len(names_data)] = names_data
    print(f"Injected 30 default English names at 0x{DEFAULT_NAMES_OFFSET:06X} ({len(names_data)} bytes).")

    # Save patched ROM
    with open(TARGET_ROM_PATH, 'wb') as f:
        f.write(rom)

    # Recalculate checksum
    fix_checksum(TARGET_ROM_PATH)
    print(f"Successfully patched naming screen in {TARGET_ROM_PATH}!\n")

if __name__ == '__main__':
    patch_naming_screen()
