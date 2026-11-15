# Monster Gate (GBA) - English Translation

> [!WARNING]
> **Work in Progress:** This project is under active development and is **not** production-ready. The translation is incomplete, text formatting and UI elements are still being refined, and bugs or untranslated text may be encountered.

An unofficial English fan-translation project and ROM-hacking toolchain for Konami's *Monster Gate* (*モンスターゲート*, 2002, Game Code `ANFJ`) on the Game Boy Advance.

---

## Prerequisites

- Python 3.10+
- Pillow (`pip install Pillow`)
- A clean Japanese ROM placed at `rom/base.gba`

## Building

Compile the ROM from the current translation files:

```bash
python build.py build
```

Run the full pipeline (font extraction, text dump, merge, ROM build, and patch generation):

```bash
python build.py all
```

Generate standalone `.bps` and `.ips` patches in `patches/`:

```bash
python build.py patch
```

## Testing / Playing

- **Direct ROM:** Open `rom/monster_gate_en.gba` in a GBA emulator (e.g., mGBA).
- **Patching:** Apply `patches/monster_gate_en.bps` to a clean Japanese ROM (`rom/base.gba`) using [Flips](https://www.romhacking.net/utilities/1040/) or an online BPS patcher.
