#!/usr/bin/env python3
"""
tools/split_translations.py
Splits text/translations/all_strings.json into modular category files:
  - text/translations/01_items_cards.json (Descriptors 0 - 250: Potions, Magic, Items, Cards)
  - text/translations/02_monsters.json (Descriptors 251 - 403: Monster cards, summons, classes)
  - text/translations/03_dialogue.json (Descriptors 404 - 549: NPC cutscenes, Gatekeeper, floor dialogue)
  - text/translations/04_system_ui.json (Descriptors 550 - 553 + UI descriptors: Menus, prompts, stats)
"""

import json
import os

ALL_STRINGS_PATH = "text/translations/all_strings.json"

def main():
    if not os.path.exists(ALL_STRINGS_PATH):
        print(f"Error: {ALL_STRINGS_PATH} missing.")
        return

    with open(ALL_STRINGS_PATH, "r", encoding="utf-8") as f:
        strings = json.load(f)

    items_cards = []
    monsters = []
    dialogue = []
    system_ui = []

    for s in strings:
        d_idx = s["descriptor_index"]
        if d_idx <= 250:
            items_cards.append(s)
        elif d_idx <= 403:
            monsters.append(s)
        elif d_idx <= 549:
            dialogue.append(s)
        else:
            system_ui.append(s)

    with open("text/translations/01_items_cards.json", "w", encoding="utf-8") as f:
        json.dump(items_cards, f, ensure_ascii=False, indent=2)

    with open("text/translations/02_monsters.json", "w", encoding="utf-8") as f:
        json.dump(monsters, f, ensure_ascii=False, indent=2)

    with open("text/translations/03_dialogue.json", "w", encoding="utf-8") as f:
        json.dump(dialogue, f, ensure_ascii=False, indent=2)

    with open("text/translations/04_system_ui.json", "w", encoding="utf-8") as f:
        json.dump(system_ui, f, ensure_ascii=False, indent=2)

    print("Splitting completed:")
    print(f"  01_items_cards.json: {len(items_cards)} strings")
    print(f"  02_monsters.json:    {len(monsters)} strings")
    print(f"  03_dialogue.json:    {len(dialogue)} strings")
    print(f"  04_system_ui.json:   {len(system_ui)} strings")

if __name__ == "__main__":
    main()
