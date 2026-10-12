# Monster Gate (Game Boy Advance) - English Translation v1.0

This release provides the first complete, 100% English fan translation for **Monster Gate** (*モンスターゲート*, 2002, Game Code `ANFJ`) developed by Konami / KCE Studios for the Game Boy Advance.

---

### Features & Highlights

- **100% Script Translation:**
  - All **2,752 text strings** across all **554 script descriptors** translated into English.
  - Complete story campaigns for all character classes (Warrior, Rogue, Wizard).
  - All 499 items, weapons, shields, magic spells, and monster summon cards.
  - All 38 dungeons, fortress campaigns, slot machine rules, and town facilities.
  - Complete 45-step beginner tutorial guide and card blending recipes.
- **Custom Font Engine:**
  - Injected full lowercase `a`–`z` alphabet into the game's font table.
  - Custom glyph blitting preserving original Latin uppercase, numerals, and punctuation.
- **16 MB ROM Expansion:**
  - Expanded ROM safely from 8 MB to 16 MB (`0x08800000`–`0x08FFFFFF`) for zero-overwrite, crash-free stability.
  - Recalculated and verified GBA header complement checksum (`0xBD`).

---

### Patching Instructions

Apply either the **BPS** patch (recommended) or **IPS** patch to your original Japanese ROM:

- **Target ROM:** `0499 - Monster Gate (J)(Independent).gba`
- **Header Checksum:** `0xBD`
- **Original ROM Size:** 8,388,608 bytes (8 MB)
- **Patched ROM Size:** 16,777,216 bytes (16 MB)

You can use any standard patching tool, such as:
- **Online:** [Romhacking.net Patcher](https://www.romhacking.net/patch/) or [Marc Robledo's Online Patcher](https://www.marcrobledo.com/RomPatcher.js/)
- **Desktop:** FLIPS (Floating IPS), Lunar IPS, or beat

---

### Included Release Files

- `monster_gate_en.bps`: Recommended BPS patch file.
- `monster_gate_en.ips`: Standard IPS patch file.
- `monster_gate_en_v1.0.zip`: All-in-one package containing both patches and documentation.
