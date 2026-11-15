#!/usr/bin/env python3
"""
build.py
Master build script for Monster Gate (GBA) English translation.
Commands:
  python build.py dump     - Extracts font and all game strings from rom/base.gba
  python build.py font     - Generates and patches 8x16 and 8x8 fonts
  python build.py build    - Merges translations, compiles ROM, patches naming screen, and verifies
  python build.py patch    - Creates BPS/IPS patches and verifies roundtrip
  python build.py verify   - Runs comprehensive ROM and patch verification
  python build.py all      - Runs font, build, patch, and verify in sequence
"""

import subprocess
import sys

def run(cmd):
    print(f"\n>>> Running: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"Error running command: {cmd}")
        sys.exit(res.returncode)

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "build"

    if target == "dump":
        run("python tools/dump_font.py")
        run("python tools/build_charmap.py")
        run("python tools/dump_text.py")
        run("python tools/split_translations.py")
    elif target == "font":
        run("python tools/dump_font.py")
        run("python tools/build_charmap.py")
        run("python tools/patch_font.py")
    elif target == "build":
        run("python tools/translate_everything_perfect.py")
        run("python tools/insert_text.py")
        run("python tools/patch_naming_screen.py")
        run("python tools/patch_ui_graphics.py")
        run("python tools/verify_rom.py")
    elif target == "patch":
        run("python tools/create_patch.py")
        run("python tools/verify_rom.py")
    elif target == "verify":
        run("python tools/verify_rom.py")
    elif target == "all":
        run("python tools/dump_font.py")
        run("python tools/build_charmap.py")
        run("python tools/patch_font.py")
        run("python tools/translate_everything_perfect.py")
        run("python tools/insert_text.py")
        run("python tools/patch_naming_screen.py")
        run("python tools/patch_ui_graphics.py")
        run("python tools/create_patch.py")
        run("python tools/verify_rom.py")
    else:
        print(f"Unknown command: {target}. Available: dump, font, build, patch, verify, all")

if __name__ == "__main__":
    main()
