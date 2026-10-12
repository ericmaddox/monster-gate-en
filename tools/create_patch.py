#!/usr/bin/env python3
"""
tools/create_patch.py
Generates distributable IPS and BPS translation patches from base.gba to monster_gate_en.gba.
"""

import os
import struct
import zlib

BASE_PATH = "rom/base.gba"
TARGET_PATH = "rom/monster_gate_en.gba"
PATCH_DIR = "patches"

def create_ips_patch(base_data, target_data, out_path):
    """Creates a standard IPS patch."""
    records = []
    i = 0
    while i < len(target_data):
        # Find differences
        if i >= len(base_data) or base_data[i] != target_data[i]:
            start = i
            while i < len(target_data) and (i >= len(base_data) or base_data[i] != target_data[i]) and (i - start) < 65535:
                i += 1
            diff_chunk = target_data[start:i]
            # Offset must fit in 3 bytes
            if start < 0x1000000:
                records.append((start, diff_chunk))
        else:
            i += 1

    with open(out_path, "wb") as f:
        f.write(b"PATCH")
        for offset, chunk in records:
            # 3-byte offset, 2-byte length
            f.write(struct.pack(">I", offset)[1:])
            f.write(struct.pack(">H", len(chunk)))
            f.write(chunk)
        f.write(b"EOF")
    print(f"Created IPS patch: {out_path} ({len(records)} diff chunks, {os.path.getsize(out_path)} bytes)")

def encode_vli(val):
    """BPS variable-length integer encoding."""
    res = bytearray()
    while True:
        b = val & 0x7F
        val >>= 7
        if val == 0:
            res.append(0x80 | b)
            break
        res.append(b)
        val -= 1
    return bytes(res)

def create_bps_patch(base_data, target_data, out_path):
    """Creates a standard BPS patch."""
    out = bytearray(b"BPS1")
    out.extend(encode_vli(len(base_data)))
    out.extend(encode_vli(len(target_data)))
    out.extend(encode_vli(0))  # metadata length = 0

    # For simple BPS creation, record TargetRead chunks
    # TargetRead command: action = 0, length = len(chunk)
    # command = (length - 1) << 2 | 0
    # In blocks of up to 65536 bytes:
    i = 0
    source_offset = 0
    target_offset = 0

    while target_offset < len(target_data):
        # Check matching length
        match_len = 0
        while (source_offset + match_len < len(base_data) and
               target_offset + match_len < len(target_data) and
               base_data[source_offset + match_len] == target_data[target_offset + match_len]):
            match_len += 1

        if match_len > 16:
            # SourceRead action = 1: command = ((match_len - 1) << 2) | 1
            cmd = ((match_len - 1) << 2) | 1
            out.extend(encode_vli(cmd))
            source_offset += match_len
            target_offset += match_len
        else:
            # Find how much is diff
            diff_len = 0
            while (target_offset + diff_len < len(target_data) and
                   (source_offset + diff_len >= len(base_data) or
                    base_data[source_offset + diff_len] != target_data[target_offset + diff_len])):
                diff_len += 1
                if diff_len >= 32768: break

            if diff_len == 0:
                diff_len = 1

            # TargetRead action = 0
            cmd = ((diff_len - 1) << 2) | 0
            out.extend(encode_vli(cmd))
            out.extend(target_data[target_offset : target_offset + diff_len])
            target_offset += diff_len
            source_offset += diff_len

    # Add CRC32s
    crc_source = zlib.crc32(base_data) & 0xFFFFFFFF
    crc_target = zlib.crc32(target_data) & 0xFFFFFFFF
    crc_patch = zlib.crc32(out) & 0xFFFFFFFF
    out.extend(struct.pack("<III", crc_source, crc_target, crc_patch))

    with open(out_path, "wb") as f:
        f.write(out)
    print(f"Created BPS patch: {out_path} ({os.path.getsize(out_path)} bytes)")

def main():
    if not os.path.exists(BASE_PATH) or not os.path.exists(TARGET_PATH):
        print("Error: Base or Target ROM missing.")
        return

    os.makedirs(PATCH_DIR, exist_ok=True)

    with open(BASE_PATH, "rb") as f:
        base = f.read()
    with open(TARGET_PATH, "rb") as f:
        target = f.read()

    create_ips_patch(base, target, os.path.join(PATCH_DIR, "monster_gate_en.ips"))
    create_bps_patch(base, target, os.path.join(PATCH_DIR, "monster_gate_en.bps"))

if __name__ == "__main__":
    main()
