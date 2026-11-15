# Monster Gate (GBA) — English Translation

> [!NOTE]
> **Playtesting / QA:** All 2,752 game strings (554 text descriptors), 8x16 & 8x8 English fonts, the character naming screen, and pre-rendered UI graphics (menus, intro/ending cutscenes, tutorial tabs, card/monster previews, castle nameplates, and ranking screens) have been translated and verified. Playtesting is ongoing—please report any remaining visual clipping or phrasing issues.

An unofficial English fan-translation project for Konami's *Monster Gate* (*モンスターゲート*, 2002, Game Code `ANFJ`) on the Game Boy Advance.

---

## Repository Contents

- `build.py` — Build orchestrator (`dump`, `translate`, `build`, `patch`, `verify`, `all`)
- `text/` — Raw Japanese text dump (`raw_dump.json`) and categorized English translations (`01_items_cards.json`, `02_monsters.json`, `03_dialogue.json`, `04_system_ui.json`, `all_strings.json`)
- `font/` — Extracted/patched 8x16 and 8x8 font binaries, glyph tables, and contact sheet
- `graphics/` — Generated English naming-screen tile bank (`keyboard_tiles.bin`)
- `patches/monster_gate_en_v1.0.zip` — Release archive containing `.bps` and `.ips` patches
- `release_notes.md` — Changelog and technical notes

---

## Playing (Patching a Clean ROM)

If you just want to play, extract `patches/monster_gate_en_v1.0.zip` and apply the `.bps` (or `.ips`) patch to a clean Japanese *Monster Gate* (`ANFJ`) GBA ROM using [Flips](https://www.romhacking.net/utilities/1040/) or an online BPS patcher, then open the patched `.gba` in an emulator such as [mGBA](https://mgba.io/).

---

## Building from Source

### Prerequisites

- Python 3.10+
- Pillow (`pip install Pillow`)
- A clean Japanese *Monster Gate* (`ANFJ`) ROM placed at `rom/base.gba`
- Local toolchain scripts in `tools/` (gitignored; required by `build.py`)

### Commands

- **Build ROM from current translation & font assets:**
  ```bash
  python build.py build
  ```
- **Run full pipeline** (font dump/patch, text merge/insert, naming screen & UI graphics patching, BPS/IPS generation, and ROM verification):
  ```bash
  python build.py all
  ```
- **Generate `.bps`, `.ips`, and release `.zip` in `patches/`:**
  ```bash
  python build.py patch
  ```
- **Verify the built ROM (`rom/monster_gate_en.gba`):**
  ```bash
  python build.py verify
  ```
