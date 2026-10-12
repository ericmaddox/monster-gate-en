#!/usr/bin/env python3
"""
tools/build_charmap.py
Generates the initial font/glyph_table.json mapping glyph IDs (0-639) to Unicode characters.
Populates:
  - 0-45: Hiragana (あ-ん)
  - 46-48: Small kana (ぁ-ぅ)
  - 49-68: Dakuten (が-ぼ)
  - 69-73: Handakuten (ぱ-ぽ)
  - 74-79: Small kana (ゃ, ゅ, ょ, っ, ぁ, ぃ)
  - 80-125: Katakana (ア-ン)
  - 126-159: Katakana dakuten, handakuten, small katakana
  - 161-186: Latin Uppercase A-Z
  - 187-196: Digits 0-9
  - 197: Space
  - 198-207: Punctuation (+, -, ?, !, ., ,, ', :, /, etc.)
  - 208-639: Kanji and special symbols
"""

import json
import os

CHARMAP = {}

# 0-45: Hiragana
HIRAGANA_BASIC = [
    'あ', 'い', 'う', 'え', 'お',
    'か', 'き', 'く', 'け', 'こ',
    'さ', 'し', 'す', 'せ', 'そ',
    'た', 'ち', 'つ', 'て', 'と',
    'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ひ', 'ふ', 'へ', 'ほ',
    'ま', 'み', 'む', 'め', 'も',
    'や', 'ゆ', 'よ',
    'ら', 'り', 'る', 'れ', 'ろ',
    'わ', 'を', 'ん'
]

for idx, ch in enumerate(HIRAGANA_BASIC):
    CHARMAP[idx] = ch

# 46-48: small kana
CHARMAP[46] = 'ぁ'
CHARMAP[47] = 'ぃ'
CHARMAP[48] = 'ぅ'

# 49-68: Hiragana Dakuten
HIRAGANA_DAKUTEN = [
    'が', 'ぎ', 'ぐ', 'げ', 'ご',
    'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
    'だ', 'ぢ', 'づ', 'で', 'ど',
    'ば', 'び', 'ぶ', 'べ', 'ぼ'
]
for idx, ch in enumerate(HIRAGANA_DAKUTEN):
    CHARMAP[49 + idx] = ch

# 69-73: Hiragana Handakuten
HIRAGANA_HANDAKUTEN = ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ']
for idx, ch in enumerate(HIRAGANA_HANDAKUTEN):
    CHARMAP[69 + idx] = ch

# 74-79: Small hiragana
SMALL_HIRAGANA = ['ゃ', 'ゅ', 'ょ', 'っ', 'ぇ', 'ぉ']
for idx, ch in enumerate(SMALL_HIRAGANA):
    CHARMAP[74 + idx] = ch

# 80-125: Katakana
KATAKANA_BASIC = [
    'フ', 'ヘ', 'ホ',
    'マ', 'ミ', 'ム', 'メ', 'モ',
    'ヤ', 'ユ', 'ヨ',
    'ラ', 'リ', 'ル', 'レ', 'ロ',
    'ワ', 'ヲ', 'ン', 'ッ',
    'ア', 'イ', 'ウ', 'エ', 'オ',
    'カ', 'キ', 'ク', 'ケ', 'コ',
    'サ', 'シ', 'ス', 'セ', 'ソ',
    'タ', 'チ', 'ツ', 'テ', 'ト',
    'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
    'ハ', 'ヒ'
]
for idx, ch in enumerate(KATAKANA_BASIC):
    CHARMAP[80 + idx] = ch

# Katakana Dakuten, Handakuten, symbols
CHARMAP[108] = 'ー'  # prolonged sound
CHARMAP[109] = '・'  # middle dot
CHARMAP[110] = 'ガ'
CHARMAP[111] = 'ギ'
CHARMAP[112] = 'グ'
CHARMAP[113] = 'ゲ'
CHARMAP[114] = 'ゴ'
CHARMAP[115] = 'ザ'
CHARMAP[116] = 'ジ'
CHARMAP[117] = 'ズ'
CHARMAP[118] = 'ゼ'
CHARMAP[119] = 'ゾ'
CHARMAP[120] = 'ダ'
CHARMAP[121] = 'ヂ'
CHARMAP[122] = 'ヅ'
CHARMAP[123] = 'デ'
CHARMAP[124] = 'ド'
CHARMAP[125] = 'バ'
CHARMAP[126] = 'ビ'
CHARMAP[127] = 'ブ'
CHARMAP[128] = 'ベ'
CHARMAP[129] = 'ボ'
CHARMAP[130] = 'パ'
CHARMAP[131] = 'ピ'
CHARMAP[132] = 'プ'
CHARMAP[133] = 'ペ'
CHARMAP[134] = 'ポ'
CHARMAP[135] = 'ァ'
CHARMAP[136] = 'ィ'
CHARMAP[137] = 'ゥ'
CHARMAP[138] = 'ェ'
CHARMAP[139] = 'ォ'
CHARMAP[140] = 'ャ'
CHARMAP[141] = 'ュ'
CHARMAP[142] = 'ョ'

# 161-186: Latin Uppercase A-Z
for i in range(26):
    CHARMAP[161 + i] = chr(ord('A') + i)

# 187-196: Digits 0-9
for i in range(10):
    CHARMAP[187 + i] = str(i)

# 197: Space
CHARMAP[197] = ' '

# 198-207: Punctuation
CHARMAP[198] = '+'
CHARMAP[199] = '-'
CHARMAP[200] = '?'
CHARMAP[201] = '!'
CHARMAP[202] = '.'
CHARMAP[203] = ','
CHARMAP[204] = ':'
CHARMAP[205] = '/'
CHARMAP[206] = '%'
CHARMAP[207] = '~'

def main():
    os.makedirs("font", exist_ok=True)
    
    # Fill remaining slots up to 639 as unknown placeholder if not set
    full_table = {}
    for gid in range(640):
        if gid in CHARMAP:
            full_table[str(gid)] = CHARMAP[gid]
        else:
            full_table[str(gid)] = f"[G:{gid:03d}]"

    with open("font/glyph_table.json", "w", encoding="utf-8") as f:
        json.dump(full_table, f, ensure_ascii=False, indent=2)

    print(f"Generated font/glyph_table.json with {len(full_table)} entries.")

if __name__ == "__main__":
    main()
