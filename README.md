# Monster Gate (GBA) — English Translation

> [!NOTE]
> **Playtesting / QA:** All 2,752 game strings (554 text descriptors), 8x16 & 8x8 English fonts, the character naming screen, and pre-rendered UI graphics (menus, intro/ending cutscenes, tutorial tabs, card/monster previews, castle nameplates, and ranking screens) have been translated and verified. Playtesting is ongoing—please report any bugs, text clipping, or untranslated elements on the [Issues page](https://github.com/ericmaddox/monster-gate-en/issues).

An unofficial English fan-translation project for Konami's *Monster Gate* (*モンスターゲート*, 2002, Game Code `ANFJ`) on the Game Boy Advance.

---

## Repository Contents

- `patches/monster_gate_en_v1.0.zip` — Release archive containing `.bps` and `.ips` patches
- `text/` — Raw Japanese text dump (`raw_dump.json`) and categorized English translations (`01_items_cards.json`, `02_monsters.json`, `03_dialogue.json`, `04_system_ui.json`, `all_strings.json`)
- `font/` — Extracted/patched 8x16 and 8x8 font binaries, glyph tables, and contact sheet
- `graphics/` — Generated English naming-screen tile bank (`keyboard_tiles.bin`)
- `release_notes.md` — Changelog and technical notes

---

## Playing (Patching a Clean ROM)

1. Download the latest release from [Releases](https://github.com/ericmaddox/monster-gate-en/releases) (or extract `patches/monster_gate_en_v1.0.zip`).
2. Apply `monster_gate_en.bps` (recommended) or `monster_gate_en.ips` to a clean 8 MB Japanese *Monster Gate* (`ANFJ`) GBA ROM using [Flips](https://www.romhacking.net/utilities/1040/) or [RomPatcher.js](https://www.marcrobledo.com/RomPatcher.js/).
3. Open the patched `.gba` ROM in a GBA emulator such as [mGBA](https://mgba.io/).
