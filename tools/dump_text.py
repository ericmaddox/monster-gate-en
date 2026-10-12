#!/usr/bin/env python3
"""
tools/dump_text.py
Dumps all 554 text script descriptors and 2,752 strings from Monster Gate (GBA).
Outputs:
  - text/raw_dump.json (complete technical dump with pointers and glyph mappings)
  - text/translations/all_strings.json (structured translation file)
"""

import json
import os
import struct

ROM_PATH = "rom/base.gba"
CHARMAP_PATH = "font/glyph_table.json"

def load_charmap():
    if os.path.exists(CHARMAP_PATH):
        with open(CHARMAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def decode_string_bytes(s_bytes, local_glyphs, charmap):
    """Converts a raw string byte sequence into a readable Unicode text with control tags."""
    chars = []
    i = 0
    while i < len(s_bytes):
        b = s_bytes[i]
        if b < 0xE0:
            if b < len(local_glyphs):
                gid = local_glyphs[b]
                ch = charmap.get(str(gid), f"[G:{gid:03d}]")
                chars.append(ch)
            else:
                chars.append(f"\\x{b:02x}")
            i += 1
        elif b == 0xF0:
            chars.append("{BREAK}")
            i += 1
            break  # End of message string
        elif b == 0xF1:
            chars.append("{NEWLINE}")
            i += 1
        elif b == 0xF5:
            # 2-byte parameter/variable
            if i + 1 < len(s_bytes):
                param = s_bytes[i + 1]
                chars.append(f"{{VAR:{param:02X}}}")
                i += 2
            else:
                chars.append("{VAR}")
                i += 1
        else:
            chars.append(f"{{CTRL:{b:02X}}}")
            i += 1
    return "".join(chars)

def main():
    if not os.path.exists(ROM_PATH):
        print(f"Error: {ROM_PATH} not found.")
        return

    with open(ROM_PATH, "rb") as f:
        rom_data = f.read()

    charmap = load_charmap()

    # Scan all valid descriptors
    descriptors = []
    for off in range(0, len(rom_data) - 12, 4):
        p1, p2, w1, w2 = struct.unpack_from("<IIHH", rom_data, off)
        if 0x08000000 <= p1 < 0x08800000 and 0x08000000 <= p2 < 0x08800000:
            rom_p1 = p1 - 0x08000000
            rom_p2 = p2 - 0x08000000
            if 0 < w1 < 500 and 0 < w2 < 500:
                # Check if p1 really points to ROM pointers
                valid_ptrs = True
                for k in range(min(w1, 4)):
                    tgt = struct.unpack_from("<I", rom_data, rom_p1 + k * 4)[0]
                    if not (0x08000000 <= tgt < 0x08800000):
                        valid_ptrs = False
                        break
                if valid_ptrs:
                    descriptors.append((off, p1, p2, w1, w2))

    print(f"Discovered {len(descriptors)} text descriptors in ROM.")

    all_strings = []
    raw_descriptors_dump = []
    global_string_id = 0

    for d_idx, (desc_off, p1, p2, num_strings, num_glyphs) in enumerate(descriptors):
        rom_p1 = p1 - 0x08000000
        rom_p2 = p2 - 0x08000000

        # Read local glyph map
        local_glyphs = [
            struct.unpack_from("<H", rom_data, rom_p2 + g * 2)[0]
            for g in range(num_glyphs)
        ]

        desc_entry = {
            "descriptor_index": d_idx,
            "descriptor_offset": f"0x{desc_off:06X}",
            "string_table_ptr": f"0x{p1:08X}",
            "glyph_map_ptr": f"0x{p2:08X}",
            "num_strings": num_strings,
            "num_glyphs": num_glyphs,
            "local_glyphs": local_glyphs,
            "strings": []
        }

        # Read strings in this descriptor
        for s_idx in range(num_strings):
            s_ptr = struct.unpack_from("<I", rom_data, rom_p1 + s_idx * 4)[0]
            s_rom_off = s_ptr - 0x08000000

            # Read until 0xF0 or max 256 bytes
            s_bytes = bytearray()
            curr = s_rom_off
            while curr < len(rom_data):
                b = rom_data[curr]
                s_bytes.append(b)
                curr += 1
                if b == 0xF0 or len(s_bytes) >= 256:
                    break

            decoded_text = decode_string_bytes(s_bytes, local_glyphs, charmap)

            str_item = {
                "id": global_string_id,
                "descriptor_index": d_idx,
                "string_index": s_idx,
                "rom_offset": f"0x{s_rom_off:06X}",
                "japanese": decoded_text,
                "english": "",  # Field for translation
                "raw_hex": s_bytes.hex()
            }

            desc_entry["strings"].append(str_item)
            all_strings.append(str_item)
            global_string_id += 1

        raw_descriptors_dump.append(desc_entry)

    os.makedirs("text/translations", exist_ok=True)

    with open("text/raw_dump.json", "w", encoding="utf-8") as f:
        json.dump(raw_descriptors_dump, f, ensure_ascii=False, indent=2)

    with open("text/translations/all_strings.json", "w", encoding="utf-8") as f:
        json.dump(all_strings, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(all_strings)} strings across {len(descriptors)} descriptors.")
    print("Saved text/raw_dump.json and text/translations/all_strings.json.")

if __name__ == "__main__":
    main()
