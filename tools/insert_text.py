#!/usr/bin/env python3
"""
tools/insert_text.py
Compiles English translations, allocates new descriptors and string tables in expanded 16 MB ROM space,
injects the patched font, and updates master pointers.
Outputs:
  - rom/monster_gate_en.gba (16 MB translated ROM)
"""

import json
import os
import re
import struct
from fix_checksum import fix_checksum

BASE_ROM_PATH = "rom/base.gba"
OUTPUT_ROM_PATH = "rom/monster_gate_en.gba"
PATCHED_FONT_PATH = "font/patched_font.bin"
CHARMAP_PATH = "font/glyph_table.json"
RAW_DUMP_PATH = "text/raw_dump.json"
TRANSLATIONS_PATH = "text/translations/all_strings.json"

FONT_OFFSET = 0x4EDD1C
EXPANDED_START = 0x800000  # 8 MB mark (ROM address 0x08800000)
ROM_SIZE_16MB = 16 * 1024 * 1024

def load_reverse_charmap():
    with open(CHARMAP_PATH, "r", encoding="utf-8") as f:
        table = json.load(f)
    rev = {}
    for gid_str, ch in table.items():
        gid = int(gid_str)
        if ch not in rev:
            rev[ch] = gid
    return rev

def encode_text_string(text, rev_charmap):
    """
    Parses a string with tags ({BREAK}, {NEWLINE}, {VAR:XX}) into
    a list of global glyph IDs and control codes.
    Returns: list of tokens (either ('GLYPH', gid) or ('CTRL', byte))
    """
    tokens = []
    # Pattern to match {TAG} or single characters
    pos = 0
    tag_pattern = re.compile(r"\{([^}]+)\}")
    while pos < len(text):
        m = tag_pattern.match(text, pos)
        if m:
            tag = m.group(1).upper()
            pos = m.end()
            if tag == "BREAK":
                tokens.append(("CTRL", 0xF0))
            elif tag == "NEWLINE":
                tokens.append(("CTRL", 0xF1))
            elif tag.startswith("VAR:"):
                var_byte = int(tag.split(":")[1], 16)
                tokens.append(("CTRL", 0xF5))
                tokens.append(("CTRL", var_byte))
            elif tag.startswith("CTRL:"):
                ctrl_byte = int(tag.split(":")[1], 16)
                tokens.append(("CTRL", ctrl_byte))
            elif tag.startswith("G:"):
                # Explicit glyph ID: {G:165}
                gid = int(tag.split(":")[1])
                tokens.append(("GLYPH", gid))
            else:
                tokens.append(("CTRL", 0xF0))
        else:
            ch = text[pos]
            pos += 1
            if ch in rev_charmap:
                tokens.append(("GLYPH", rev_charmap[ch]))
            elif ch == " ":
                tokens.append(("GLYPH", 197))
            else:
                # Fallback to space or question mark
                tokens.append(("GLYPH", 200 if ch == "?" else 197))
    # Ensure string ends with BREAK (0xF0)
    if not tokens or tokens[-1] != ("CTRL", 0xF0):
        tokens.append(("CTRL", 0xF0))
    return tokens

def main():
    if not os.path.exists(BASE_ROM_PATH):
        print(f"Error: {BASE_ROM_PATH} missing.")
        return

    with open(BASE_ROM_PATH, "rb") as f:
        base_data = f.read()

    # Expand to 16 MB
    rom = bytearray(base_data)
    if len(rom) < ROM_SIZE_16MB:
        rom.extend(b"\xFF" * (ROM_SIZE_16MB - len(rom)))
    print(f"Expanded ROM to {len(rom)} bytes (16 MB).")

    # Inject patched font table
    if os.path.exists(PATCHED_FONT_PATH):
        with open(PATCHED_FONT_PATH, "rb") as f:
            font_bytes = f.read()
        rom[FONT_OFFSET : FONT_OFFSET + len(font_bytes)] = font_bytes
        print(f"Injected patched font at 0x{FONT_OFFSET:06X} ({len(font_bytes)} bytes).")

    rev_charmap = load_reverse_charmap()

    with open(RAW_DUMP_PATH, "r", encoding="utf-8") as f:
        raw_dump = json.load(f)

    with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
        translated_strings = json.load(f)

    # Index translations by (descriptor_index, string_index)
    trans_map = {}
    for s in translated_strings:
        key = (s["descriptor_index"], s["string_index"])
        trans_map[key] = s

    # Allocation pointer in expanded ROM
    alloc_ptr = EXPANDED_START

    # Align allocation to 4 bytes
    def alloc(n_bytes):
        nonlocal alloc_ptr
        addr = alloc_ptr
        alloc_ptr = (alloc_ptr + n_bytes + 3) & ~3
        return addr

    compiled_descriptors = 0
    total_strings_compiled = 0

    for d in raw_dump:
        d_idx = d["descriptor_index"]
        desc_rom_off = int(d["descriptor_offset"], 16)
        num_strings = d["num_strings"]

        # Process each string for this descriptor
        desc_tokens_list = []
        needed_glyphs = []
        glyph_set = set()

        for s_idx in range(num_strings):
            key = (d_idx, s_idx)
            item = trans_map.get(key)
            # Use English if provided, otherwise fallback to decoded Japanese
            text_to_encode = (
                item["english"]
                if item and item.get("english")
                else (item["japanese"] if item else "")
            )
            tokens = encode_text_string(text_to_encode, rev_charmap)
            desc_tokens_list.append(tokens)

            for t_type, val in tokens:
                if t_type == "GLYPH" and val not in glyph_set:
                    glyph_set.add(val)
                    needed_glyphs.append(val)

        # Build local glyph map
        glyph_to_local_idx = {gid: idx for idx, gid in enumerate(needed_glyphs)}

        # Encode strings into byte arrays using local indices
        encoded_string_bytes_list = []
        for tokens in desc_tokens_list:
            s_bytes = bytearray()
            for t_type, val in tokens:
                if t_type == "GLYPH":
                    s_bytes.append(glyph_to_local_idx[val])
                else:
                    s_bytes.append(val)
            # Append trailing null for safety
            s_bytes.append(0x00)
            encoded_string_bytes_list.append(bytes(s_bytes))

        # 1. Allocate string data in expanded space
        string_rom_ptrs = []
        for s_bytes in encoded_string_bytes_list:
            s_addr = alloc(len(s_bytes))
            rom[s_addr : s_addr + len(s_bytes)] = s_bytes
            string_rom_ptrs.append(0x08000000 + s_addr)
            total_strings_compiled += 1

        # 2. Allocate string pointer table (uint32[num_strings])
        ptr_table_size = len(string_rom_ptrs) * 4
        ptr_table_addr = alloc(ptr_table_size)
        for i, s_ptr in enumerate(string_rom_ptrs):
            struct.pack_into("<I", rom, ptr_table_addr + i * 4, s_ptr)

        # 3. Allocate local glyph map (uint16[len(needed_glyphs)])
        glyph_map_size = len(needed_glyphs) * 2
        glyph_map_addr = alloc(glyph_map_size)
        for i, gid in enumerate(needed_glyphs):
            struct.pack_into("<H", rom, glyph_map_addr + i * 2, gid)

        # 4. Update the descriptor header in original ROM location (12 bytes)
        # Struct: [ptr_string_table, ptr_glyph_map, uint16 num_strings, uint16 num_glyphs]
        new_ptr1 = 0x08000000 + ptr_table_addr
        new_ptr2 = 0x08000000 + glyph_map_addr
        struct.pack_into(
            "<IIHH",
            rom,
            desc_rom_off,
            new_ptr1,
            new_ptr2,
            num_strings,
            len(needed_glyphs)
        )
        compiled_descriptors += 1

    # Write output ROM
    with open(OUTPUT_ROM_PATH, "wb") as f:
        f.write(rom)

    # Recalculate checksum
    fix_checksum(OUTPUT_ROM_PATH)

    expanded_used = alloc_ptr - EXPANDED_START
    print(f"\nSuccessfully compiled {compiled_descriptors} descriptors and {total_strings_compiled} strings.")
    print(f"Expanded region utilized: {expanded_used} bytes ({expanded_used / 1024:.1f} KB) / 8 MB.")
    print(f"Output ROM written to {OUTPUT_ROM_PATH}.")

if __name__ == "__main__":
    main()
