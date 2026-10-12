#!/usr/bin/env python3
"""
tools/merge_translations.py
Merges translated category files back into text/translations/all_strings.json.
Reads:
  - text/translations/01_items_cards.json
  - text/translations/02_monsters.json
  - text/translations/03_dialogue.json
  - text/translations/04_system_ui.json
Outputs:
  - text/translations/all_strings.json
"""

import json
import os

CATEGORY_FILES = [
    "text/translations/01_items_cards.json",
    "text/translations/02_monsters.json",
    "text/translations/03_dialogue.json",
    "text/translations/04_system_ui.json"
]

OUTPUT_FILE = "text/translations/all_strings.json"

def main():
    combined = []
    for fpath in CATEGORY_FILES:
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                combined.extend(data)
        else:
            print(f"Warning: {fpath} not found.")

    # Sort by string ID
    combined.sort(key=lambda s: s["id"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    translated_count = sum(1 for s in combined if s.get("english"))
    print(f"Merged {len(combined)} strings ({translated_count} translated) into {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
