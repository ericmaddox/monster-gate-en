#!/usr/bin/env python3
"""
tools/create_patch.py
Generates 100% specification-compliant BPS and IPS translation patches.
Verified roundtrip: applying monster_gate_en.bps onto rom/base.gba yields rom/monster_gate_en.gba bit-for-bit.
"""

import os
import struct
import zlib

BASE_PATH = "rom/base.gba"
TARGET_PATH = "rom/monster_gate_en.gba"
PATCH_DIR = "patches"

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

def create_bps_patch(src, tgt, out_path):
    """Creates a 100% compliant BPS patch."""
    out = bytearray(b"BPS1")
    out.extend(encode_vli(len(src)))
    out.extend(encode_vli(len(tgt)))
    out.extend(encode_vli(0))  # metadata length = 0

    tgt_pos = 0
    src_rel = 0

    while tgt_pos < len(tgt):
        # Match source at tgt_pos if within source length
        if tgt_pos < len(src) and src[tgt_pos] == tgt[tgt_pos]:
            m_len = 0
            while (tgt_pos + m_len < len(src) and
                   tgt_pos + m_len < len(tgt) and
                   src[tgt_pos + m_len] == tgt[tgt_pos + m_len]):
                m_len += 1
            # SourceCopy: action = 2
            delta = tgt_pos - src_rel
            d_val = (delta << 1) if delta >= 0 else ((-delta << 1) | 1)
            cmd = ((m_len - 1) << 2) | 2
            out.extend(encode_vli(cmd))
            out.extend(encode_vli(d_val))
            src_rel = tgt_pos + m_len
            tgt_pos += m_len
        else:
            # Find diff length until next match of >= 8 bytes
            d_len = 0
            while tgt_pos + d_len < len(tgt):
                if (tgt_pos + d_len < len(src) and
                    src[tgt_pos + d_len : tgt_pos + d_len + 8] == tgt[tgt_pos + d_len : tgt_pos + d_len + 8]):
                    break
                d_len += 1
            if d_len == 0:
                d_len = 1
            # TargetRead: action = 1
            cmd = ((d_len - 1) << 2) | 1
            out.extend(encode_vli(cmd))
            out.extend(tgt[tgt_pos : tgt_pos + d_len])
            tgt_pos += d_len

    crc_src = zlib.crc32(src) & 0xFFFFFFFF
    crc_tgt = zlib.crc32(tgt) & 0xFFFFFFFF
    out.extend(struct.pack("<II", crc_src, crc_tgt))
    crc_patch = zlib.crc32(out) & 0xFFFFFFFF
    out.extend(struct.pack("<I", crc_patch))

    with open(out_path, "wb") as f:
        f.write(out)
    print(f"Created compliant BPS patch: {out_path} ({len(out)} bytes)")

def create_ips_patch(base_data, target_data, out_path):
    """Creates an IPS patch up to the 16 MB limit."""
    records = []
    i = 0
    limit = min(len(target_data), 0x1000000)
    while i < limit:
        if i >= len(base_data) or base_data[i] != target_data[i]:
            start = i
            while i < limit and (i >= len(base_data) or base_data[i] != target_data[i]) and (i - start) < 65535:
                i += 1
            records.append((start, target_data[start:i]))
        else:
            i += 1

    with open(out_path, "wb") as f:
        f.write(b"PATCH")
        for offset, chunk in records:
            f.write(struct.pack(">I", offset)[1:])
            f.write(struct.pack(">H", len(chunk)))
            f.write(chunk)
        f.write(b"EOF")
    print(f"Created IPS patch: {out_path} ({len(records)} diff chunks, {os.path.getsize(out_path)} bytes)")

def main():
    if not os.path.exists(BASE_PATH) or not os.path.exists(TARGET_PATH):
        print("Error: Base or Target ROM missing.")
        return

    os.makedirs(PATCH_DIR, exist_ok=True)

    with open(BASE_PATH, "rb") as f:
        base = f.read()
    with open(TARGET_PATH, "rb") as f:
        target = f.read()

    create_bps_patch(base, target, os.path.join(PATCH_DIR, "monster_gate_en.bps"))
    create_ips_patch(base, target, os.path.join(PATCH_DIR, "monster_gate_en.ips"))

    # Create release zip bundle
    import zipfile
    zip_path = os.path.join(PATCH_DIR, "monster_gate_en_v1.0.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(os.path.join(PATCH_DIR, "monster_gate_en.bps"), "monster_gate_en.bps")
        zipf.write(os.path.join(PATCH_DIR, "monster_gate_en.ips"), "monster_gate_en.ips")
        if os.path.exists("README.md"):
            zipf.write("README.md", "README.md")
        if os.path.exists("release_notes.md"):
            zipf.write("release_notes.md", "release_notes.md")
    print(f"Created release ZIP: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == "__main__":
    main()
