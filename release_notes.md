# Monster Gate (Game Boy Advance) - English Translation (WIP)

> [!WARNING]
> **Work in Progress:** This is an active work-in-progress build and is **not** production-ready. Translation coverage, text formatting, and UI polish are still ongoing.

An unofficial English fan-translation project for **Monster Gate** (*モンスターゲート*, 2002, Game Code `ANFJ`) developed by Konami / KCE Studios for the Game Boy Advance.

---

### Current Focus

- **Text & Dialogue:** Translating and formatting 2,752 strings across 554 script descriptors to fit GBA text box limits (`<= 13` characters per line).
- **Font Engine:** Patched 8×16 (`0x4EDD1C`) and 8×8 outlined (`0x4F7D48`) 4bpp fonts with lowercase `a`–`z` and English punctuation.
- **Character Naming Screen:** Custom English keyboard tilemap/matrix and translated default names.
- **16 MB ROM Expansion:** Expanded from 8 MB to 16 MB (`0x08800000`–`0x08FFFFFF`) with updated GBA header checksum (`0x43`).

---

### Patching Instructions

Apply either the **BPS** patch (recommended) or **IPS** patch to your original Japanese ROM:

- **Target ROM:** `0499 - Monster Gate (J)(Independent).gba`
- **Original ROM Size:** 8,388,608 bytes (8 MB)
- **Patched ROM Size:** 16,777,216 bytes (16 MB)

You can use any standard patching tool, such as:
- **Online:** [Romhacking.net Patcher](https://www.romhacking.net/patch/) or [Marc Robledo's Online Patcher](https://www.marcrobledo.com/RomPatcher.js/)
- **Desktop:** FLIPS (Floating IPS), Lunar IPS, or beat

---

### Included Files

- `monster_gate_en.bps`: BPS patch file.
- `monster_gate_en.ips`: IPS patch file.
- `monster_gate_en_v1.0.zip`: Release bundle containing both patches and documentation.
