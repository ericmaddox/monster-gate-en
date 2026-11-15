# Monster Gate (GBA) — English Translation Release Notes (`v1.0.0`)

An unofficial English fan-translation for **Monster Gate** (*モンスターゲート*, 2002, Game Code `ANFJ`), developed by Konami / KCE Studios for the Game Boy Advance.

---

## What's Included in `v1.0.0`

- **Complete Script Translation:** All **2,752 strings across 554 descriptors** (items, cards, monsters, dungeons, menus, NPC dialogue, and cutscenes) translated and formatted to fit GBA text box constraints.
- **Font Engine:** Patched 8×16 (`0x4EDD1C`) and 8×8 outlined (`0x4F7D48`) 4bpp fonts with full English uppercase, lowercase (`a`–`z`), and punctuation.
- **Character Naming Screen:** Custom English keyboard tile bank (`0x880000`), updated BG tilemaps/matrix, and translated default names.
- **Pre-Rendered UI Graphics:** Translated OBJ sprite sheets and BG tile banks for mode/character/file select, options, intro/ending cutscenes, card shop, pre-dungeon deck setup, castle nameplates, tutorial `ADVICE` tab, all 133 card & monster preview headers, pause/battle-over banners, and ranking screens.
- **16 MB ROM Expansion:** Expanded from 8 MB to 16 MB (`0x08800000`–`0x08FFFFFF`) with updated GBA header checksum (`0x43`).

---

## ROM Checksums

- **Required Clean Base ROM:** `8,388,608` bytes (8 MB)
  - **CRC32:** `5B8AAA03`
  - **MD5:** `BA1F2CD7D4EB41792103BF0A95FC0C09`
  - **SHA-1:** `4649710EB75181573D10AD059B3BC6270508CE3D`
- **Patched English ROM (`v1.0.0`):** `16,777,216` bytes (16 MB)
  - **CRC32:** `B7B55EFB`
  - **MD5:** `9D454ECEBE3A68B8670F3DD59251BD37`
  - **SHA-1:** `8CCBB5B87C95761A23E030EAC0E74D92ED1AC089`

---

## Patching Instructions

Apply **`monster_gate_en.bps`** (recommended) or `monster_gate_en.ips` to your clean Japanese `ANFJ` ROM using:
- **Desktop:** [Flips (Floating IPS)](https://www.romhacking.net/utilities/1040/)
- **Online:** [Marc Robledo's RomPatcher.js](https://www.marcrobledo.com/RomPatcher.js/) or [Romhacking.net Patcher](https://www.romhacking.net/patch/)

---

## Playtesting & Bug Reports

Playtesting is ongoing. If you spot any bugs, text clipping, or untranslated elements, please open an issue on the [GitHub Issues page](https://github.com/ericmaddox/monster-gate-en/issues) with a screenshot or save state if possible.
