#!/usr/bin/env python3
"""
tools/translate_batch.py
Batch translator for Monster Gate (GBA).
Translates items, magic spells, weapons, casino messages, and system prompts.
"""

import json
import os

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_cards(items_path):
    cards = load_file(items_path)
    
    # Standard item and spell card dictionary
    CARD_NAMES = {
        0: ("Potion {VAR:40}", "Recovers {VAR:40} HP."),
        2: ("Potion MAX", "Fully recovers HP."),
        4: ("Potion SP", "Fully recovers party HP."),
        6: ("Fire", "Deals {VAR:40} dmg to enemy. Range: Far."),
        8: ("Multi-Fire", "Deals {VAR:40} dmg to all visible enemies!"),
        10: ("Thunder", "Deals {VAR:40} dmg to enemy. Range: Far."),
        12: ("Multi-Thunder", "Deals {VAR:40} dmg to all visible enemies!"),
        14: ("Meteor", "Deals {VAR:40} dmg to enemy. Range: Far."),
        16: ("Multi-Meteor", "Deals {VAR:40} dmg to all visible enemies!"),
        18: ("Spark", "Attacks all enemies in the room."),
        20: ("Sleep", "Puts enemy to sleep. Range: Far."),
        22: ("Multi-Sleep", "Puts all visible enemies to sleep."),
        24: ("Poison", "Poisons enemy. Range: Far."),
        26: ("Multi-Poison", "Poisons all visible enemies."),
        28: ("Slow", "Slows enemy speed. Range: Far."),
        30: ("Multi-Slow", "Slows all visible enemies."),
        32: ("Multi-Panic", "Confuses all visible enemies."),
        34: ("Light", "Illuminates dark floors."),
        36: ("Map", "Reveals the floor map."),
        38: ("Search", "Reveals enemy locations on floor."),
        40: ("Speed Up", "Increases movement speed."),
        42: ("Barrier", "Grants invincibility for X turns."),
        44: ("Heal 100", "Regenerates HP for {VAR:40} turns."),
        46: ("Heal 200", "Regenerates HP for {VAR:40} turns."),
        48: ("Heal 300", "Regenerates HP for {VAR:40} turns."),
        50: ("Long Sword", "Weapon card: Attack power up!"),
        52: ("Great Sword", "Weapon card: Great attack power up!"),
        54: ("Tower Shield", "Shield card: Defense up!"),
        56: ("Great Shield", "Shield card: Great defense up!"),
        58: ("Hunter Ring", "Ring: Makes finding cards easier."),
        60: ("Power Ring", "Ring: Increases attack power."),
        62: ("Guard Ring", "Ring: Increases defense."),
        64: ("Speed Ring", "Ring: Increases movement speed."),
        66: ("Escape Card", "Escape from the dungeon safely.")
    }

    count = 0
    for i in range(0, len(cards) - 1, 2):
        cid = cards[i]["id"]
        if cid in CARD_NAMES:
            cname, cdesc = CARD_NAMES[cid]
            cards[i]["english"] = cname
            cards[i + 1]["english"] = cdesc
            count += 2

    save_file(items_path, cards)
    print(f"Translated {count} card names and descriptions in {items_path}.")

def translate_monsters(monsters_path):
    monsters = load_file(monsters_path)
    
    SYSTEM_MESSAGES = {
        499: "Seek the Orbs of Sealing and conquer the dungeons!",
        500: "Equip your cards and conquer the dungeon!",
        501: "Collect Orb Fragments and enter the Monster Gate!",
        502: "Challenge dungeons anytime and beat the best time!",
        503: "Play games at the Slot Machine!",
        504: "Check and manage cards in your Card Holder.",
        505: "Change character class and job rank.",
        506: "Return to the World Gate map.",
        507: "Not enough coins!",
        508: "Quit Casino and return to menu. Is this OK?",
        509: "Quit Casino and return to title. Is this OK?",
        510: "  Yes    No",
        511: "Acquired a card!",
        512: "Cards you cannot carry are sent to the Holder.",
        513: "Obtained cards have been sent to the Holder.",
        514: "Line Bet: Change bet",
        515: "Start Slot",
        516: "Quit Casino",
        517: "Line up matching symbols on pay lines.",
        518: "Win payout based on odds table.",
        519: "WILD symbols substitute for any symbol.",
        520: "Winning lines award Magic Cards!",
        521: "If your hand is full, new cards go to Holder."
    }

    count = 0
    for s in monsters:
        sid = s["id"]
        if sid in SYSTEM_MESSAGES:
            s["english"] = SYSTEM_MESSAGES[sid]
            count += 1

    save_file(monsters_path, monsters)
    print(f"Translated {count} casino/system prompts in {monsters_path}.")

def main():
    translate_cards("text/translations/01_items_cards.json")
    translate_monsters("text/translations/02_monsters.json")

if __name__ == "__main__":
    main()
