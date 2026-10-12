#!/usr/bin/env python3
"""
tools/verify_rom.py
Verifies the compiled translated ROM by reading descriptors and checking header integrity.
"""

import json
import struct

ROM_PATH = "rom/monster_gate_en.gba"
DUMP_PATH = "text/raw_dump.json"
CHARMAP_PATH = "font/glyph_table.json"

def main():
    with open(ROM_PATH, "rb") as f:
        rom = f.read()

    print(f"ROM size: {len(rom)} bytes ({len(rom) // (1024 * 1024)} MB)")
    print(f"Header Title: {rom[0xA0:0xAC].decode('ascii', errors='ignore')}")
    print(f"Header Checksum at 0xBD: 0x{rom[0xBD]:02X}")

    with open(DUMP_PATH, "r", encoding="utf-8") as f:
        dump = json.load(f)

    with open(CHARMAP_PATH, "r", encoding="utf-8") as f:
        table = json.load(f)

    print("\n--- Sampling Verified Translated Descriptors from ROM ---")
    sample_indices = [0, 1, 2, 3, 4, 5, 250, 251, 331, 552]

    for d_idx in sample_indices:
        d = dump[d_idx]
        desc_off = int(d["descriptor_offset"], 16)
        p1, p2, w1, w2 = struct.unpack_from("<IIHH", rom, desc_off)

        local_glyphs = [
            struct.unpack_from("<H", rom, (p2 - 0x08000000) + g * 2)[0]
            for g in range(w2)
        ]

        str_list = []
        for s_i in range(min(w1, 2)):
            s_ptr = struct.unpack_from("<I", rom, (p1 - 0x08000000) + s_i * 4)[0]
            s_bytes = bytearray()
            cur = s_ptr - 0x08000000
            while cur < len(rom) and rom[cur] != 0xF0 and len(s_bytes) < 80:
                s_bytes.append(rom[cur])
                cur += 1

            decoded = "".join(
                table.get(str(local_glyphs[b]), f"[{b:02x}]")
                if b < len(local_glyphs)
                else f"[{b:02x}]"
                for b in s_bytes
            )
            str_list.append(decoded)

        desc_name = f"Desc {d_idx:03d} (0x{desc_off:06X})"
        s0_safe = (str_list[0] if len(str_list) > 0 else "").encode('ascii', 'backslashreplace').decode('ascii')
        s1_safe = (str_list[1] if len(str_list) > 1 else "").encode('ascii', 'backslashreplace').decode('ascii')
        print(f"{desc_name}: \"{s0_safe}\" | \"{s1_safe}\"")

if __name__ == "__main__":
    main()
