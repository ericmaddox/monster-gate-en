#!/usr/bin/env python3
"""
build.py
Master build script for Monster Gate (GBA) English translation.
Commands:
  python build.py dump     - Extracts font and all game strings from rom/base.gba
  python build.py font     - Generates and patches font with lowercase a-z
  python build.py build    - Merges translations and compiles rom/monster_gate_en.gba
  python build.py all      - Runs font, dump, split, merge, and build in sequence
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
        run("python tools/merge_translations.py")
        run("python tools/insert_text.py")
    elif target == "all":
        run("python tools/dump_font.py")
        run("python tools/build_charmap.py")
        run("python tools/patch_font.py")
        run("python tools/dump_text.py")
        run("python tools/split_translations.py")
        run("python tools/merge_translations.py")
        run("python tools/insert_text.py")
    else:
        print(f"Unknown command: {target}. Available: dump, font, build, all")

if __name__ == "__main__":
    main()
