#!/usr/bin/env python3
"""
tools/fix_checksum.py
Recalculates and updates the GBA cartridge header complement check at offset 0xBD.
"""

import sys

def fix_checksum(rom_path):
    with open(rom_path, "r+b") as f:
        header = f.read(0xC0)
        chk = 0
        for b in header[0xA0:0xBD]:
            chk = (chk - b) & 0xFF
        chk = (chk - 0x19) & 0xFF
        f.seek(0xBD)
        f.write(bytes([chk]))
        print(f"Updated header checksum for {rom_path} at 0xBD: 0x{chk:02X}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "rom/monster_gate_en.gba"
    fix_checksum(target)
