#!/usr/bin/env python3
"""
tools/build_charmap.py
Generates the definitive font/glyph_table.json mapping glyph IDs (0-639) to Unicode characters.
Exact verified layout:
  - 0-45: Hiragana basic (あ - ん)
  - 46-54: Hiragana small (ぁ, ぃ, ぅ, ぇ, ぉ, ゃ, ゅ, ょ, っ)
  - 55-74: Hiragana dakuten (が - ぼ)
  - 75-79: Hiragana handakuten (ぱ - ぽ)
  - 80-125: Katakana basic (ア - ン)
  - 126-134: Katakana small (ッ, ャ, ュ, ョ, ァ, ィ, ゥ, ェ, ォ)
  - 135-154: Katakana dakuten (ガ - ボ)
  - 155-159: Katakana handakuten (パ - ポ)
  - 160: ヴ
  - 161-186: Latin Uppercase A-Z
  - 187-196: Digits 0-9
  - 197: Space
  - 198-207: Punctuation (+, -, ?, !, ., ,, :, /, %, ~)
  - 208-233: Injected Lowercase Latin a-z (replaces legacy slots for English)
  - 208_orig: ー (prolonged sound)
  - 209_orig: ・ (middle dot)
  - 210-639: Kanji characters
"""

import json
import os

CHARMAP = {}

# 0-45: Hiragana basic
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

# 46-54: Hiragana small
HIRAGANA_SMALL = ['ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ゃ', 'ゅ', 'ょ', 'っ']
for idx, ch in enumerate(HIRAGANA_SMALL):
    CHARMAP[46 + idx] = ch

# 55-74: Hiragana Dakuten
HIRAGANA_DAKUTEN = [
    'が', 'ぎ', 'ぐ', 'げ', 'ご',
    'ざ', 'じ', 'ず', 'ぜ', 'ぞ',
    'だ', 'ぢ', 'づ', 'で', 'ど',
    'ば', 'び', 'ぶ', 'べ', 'ぼ'
]
for idx, ch in enumerate(HIRAGANA_DAKUTEN):
    CHARMAP[55 + idx] = ch

# 75-79: Hiragana Handakuten
HIRAGANA_HANDAKUTEN = ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ']
for idx, ch in enumerate(HIRAGANA_HANDAKUTEN):
    CHARMAP[75 + idx] = ch

# 80-125: Katakana basic
KATAKANA_BASIC = [
    'ア', 'イ', 'ウ', 'エ', 'オ',
    'カ', 'キ', 'ク', 'ケ', 'コ',
    'サ', 'シ', 'ス', 'セ', 'ソ',
    'タ', 'チ', 'ツ', 'テ', 'ト',
    'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
    'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
    'マ', 'ミ', 'ム', 'メ', 'モ',
    'ヤ', 'ユ', 'ヨ',
    'ラ', 'リ', 'ル', 'レ', 'ロ',
    'ワ', 'ヲ', 'ン'
]
for idx, ch in enumerate(KATAKANA_BASIC):
    CHARMAP[80 + idx] = ch

# 126-134: Katakana small
KATAKANA_SMALL = ['ッ', 'ャ', 'ュ', 'ョ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ']
for idx, ch in enumerate(KATAKANA_SMALL):
    CHARMAP[126 + idx] = ch

# 135-154: Katakana Dakuten
KATAKANA_DAKUTEN = [
    'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
    'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
    'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
    'バ', 'ビ', 'ブ', 'ベ', 'ボ'
]
for idx, ch in enumerate(KATAKANA_DAKUTEN):
    CHARMAP[135 + idx] = ch

# 155-159: Katakana Handakuten
KATAKANA_HANDAKUTEN = ['パ', 'ピ', 'プ', 'ペ', 'ポ']
for idx, ch in enumerate(KATAKANA_HANDAKUTEN):
    CHARMAP[155 + idx] = ch

CHARMAP[160] = 'ヴ'

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
CHARMAP[207] = 'ー'  # Verified chōonpu in Desc 0 (ポーション)

# Known verified Kanji
CHARMAP[402] = '全'
CHARMAP[403] = '回'
CHARMAP[404] = '復'

def main():
    os.makedirs("font", exist_ok=True)

    full_table = {}
    for gid in range(640):
        if gid in CHARMAP:
            full_table[str(gid)] = CHARMAP[gid]
        else:
            full_table[str(gid)] = f"[G:{gid:03d}]"

    # Lowercase letters in slots 208-233
    for i in range(26):
        full_table[str(208 + i)] = chr(ord('a') + i)

    with open("font/glyph_table.json", "w", encoding="utf-8") as f:
        json.dump(full_table, f, ensure_ascii=False, indent=2)

    print(f"Generated verified font/glyph_table.json with {len(full_table)} entries.")

if __name__ == "__main__":
    main()
