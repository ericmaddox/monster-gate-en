# Monster Gate (Game Boy Advance) - English Translation Project

A complete, 100% English translation of Konami's tactical roguelike deck-building RPG ***Monster Gate*** (*モンスターゲート*, 2002, Game Code `ANFJ`) for the Game Boy Advance.

---

## 1. Project Overview

*Monster Gate* is a dungeon crawler and deck-building RPG developed by Konami / KCE Studios based on the popular arcade medal game franchise. Prior to this project, the game was exclusive to Japan with no English release or fan translation patch.

This project delivers:
- **100% Script Translation:** All 2,752 game strings across all 554 script descriptors translated into natural English:
  - Complete story cutscenes for all 12 playable character campaigns (Warrior, Rogue, Gambler, Sorceress, Male & Female Cursed Knights, Boy & Girl Apprentices, Werewolf Boy, Were-tiger Girl, Prince & Princess of Rodrigue).
  - All 499 items, weapons, shields, magic spells, and monster summon cards.
  - All 334 monster lore entries, class attributes, and casino minigames.
  - All 38 dungeons, fortress campaigns, slot machine rules, and town facilities.
  - Complete 45-step beginner tutorial guide and card blending recipes.
- **Engine-Compliant Text Window Formatting:** All dialogue boxes strictly formatted to $\le 13$ characters per line with native control codes (`{CTRL:F9}` speaker labels, `{CTRL:F3}` page breaks) to eliminate text cutoff or box clipping.
- **Font & Glyph Engine Adaptation:** Injected full lowercase `a`–`z` alphabet into the game's font table while preserving native Latin uppercase (`A`–`Z`), digits, and punctuation.
- **Clean 16 MB ROM Expansion:** Expanded the original 8 MB ROM to 16 MB (`0x08800000`–`0x08FFFFFF`) to store relocated descriptors, pointer tables, and extended English text strings with zero overwrite risk.
- **Automated Toolchain & Distributable Patches:** Complete Python-based extraction, compilation, verification, and IPS/BPS patch generation pipeline.

---

## 2. Directory Structure

```
monster-gate-en/
├─ build.py                         # Master build orchestrator (dump, font, build, patch, all)
├─ rom/
│  ├─ base.gba                      # Original Japanese GBA ROM (8 MB, SHA-1 verified)
│  └─ monster_gate_en.gba           # Fully translated English ROM (16 MB)
├─ tools/
│  ├─ dump_font.py                  # Extracts 640 font glyphs to PNG and contact sheet
│  ├─ build_charmap.py              # Generates bidirectional glyph <-> character table
│  ├─ patch_font.py                 # Generates and injects lowercase letters a-z
│  ├─ dump_text.py                  # Extracts all 554 descriptors and 2,752 strings to JSON
│  ├─ split_translations.py         # Splits strings into modular category files
│  ├─ merge_translations.py         # Reassembles category files into all_strings.json
│  ├─ translate_full_game.py        # Translates all cards, monsters, dialogue, and UI
│  ├─ insert_text.py                # Compiles English text into expanded 16 MB ROM space
│  ├─ fix_checksum.py               # Recalculates GBA header complement checksum (0xBD)
│  ├─ verify_rom.py                 # Decodes and validates sample descriptors from output ROM
│  └─ create_patch.py               # Generates IPS and BPS patches
├─ font/
│  ├─ glyph_table.json              # 640-entry bidirectional character table
│  ├─ font_sheet.png                # Contact sheet of all original 640 glyphs
│  ├─ raw_font.bin                  # Original font binary (40,960 bytes)
│  └─ patched_font.bin              # Patched font binary with lowercase a-z
├─ text/
│  ├─ raw_dump.json                 # Low-level memory descriptor dump
│  └─ translations/
│     ├─ all_strings.json           # Master translation dataset (2,752 strings)
│     ├─ 01_items_cards.json        # 499 strings: Potions, spells, weapons, items
│     ├─ 02_monsters.json           # 334 strings: Monster summon cards, classes, Casino
│     ├─ 03_dialogue.json           # 1,906 strings: NPC dialogue, tutorials, cutscenes
│     └─ 04_system_ui.json          # 13 strings: Timers, floor descent, rank announcements
└─ patches/
   ├─ monster_gate_en.bps           # Distributable BPS patch
   └─ monster_gate_en.ips           # Distributable IPS patch
```

---

## 3. How to Build the Translated ROM

### Prerequisites
- Python 3.10+
- Pillow (`pip install Pillow`)
- Clean Japanese ROM placed at `rom/base.gba` (`0499 - Monster Gate (J)(Independent).gba`)

### Quick Build
To compile the translated ROM from the translation datasets:
```bash
python build.py build
```

This generates `rom/monster_gate_en.gba` (16 MB) with a valid GBA cartridge header complement check (`0x43`).

### Complete Re-Extraction & Build
To run the entire pipeline from scratch (font dump, text extraction, translation merge, compilation, and patch creation):
```bash
python build.py all
```

### Creating Distributable Patches
To generate standalone `.bps` and `.ips` patches:
```bash
python build.py patch
```
Patches will be written to `patches/monster_gate_en.bps` and `patches/monster_gate_en.ips`.

---

## 4. How to Play

1. **Option A (Direct ROM):**
   - Open `rom/monster_gate_en.gba` in any GBA emulator (mGBA, VisualBoyAdvance, NanoBoyAdvance) or flash cart (EZ-Flash Omega, EverDrive GBA X5).
2. **Option B (Patching):**
   - Use an online patcher (like [Romhacking.net Patcher](https://www.romhacking.net/patch/)) or [Flips](https://www.romhacking.net/utilities/1040/).
   - Select your clean Japanese ROM (`0499 - Monster Gate (J).gba`).
   - Apply `patches/monster_gate_en.bps`.
