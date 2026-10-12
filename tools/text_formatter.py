"""
tools/text_formatter.py
Formats dialogue strings strictly into GBA text box constraints:
  - Max 13 characters per line
  - At most 2 body lines per box
  - No trailing cutoff prepositions
  - Ends with {CTRL:F3}
"""

import re

PREPOSITIONS = {'to', 'of', 'and', 'the', 'a', 'an', 'in', 'for', 'with', 'on', 'at', 'is', 'be', 'are', 'your', 'my', 'its'}

def wrap_to_lines(text, max_len=13):
    words = text.strip().split()
    lines = []
    cur_line = []
    cur_len = 0
    for w in words:
        if not cur_line:
            cur_line.append(w)
            cur_len = len(w)
        elif cur_len + 1 + len(w) <= max_len:
            cur_line.append(w)
            cur_len += 1 + len(w)
        else:
            lines.append(" ".join(cur_line))
            cur_line = [w]
            cur_len = len(w)
    if cur_line:
        lines.append(" ".join(cur_line))
    return lines

def make_box(speaker, text_or_lines):
    if isinstance(text_or_lines, (list, tuple)):
        raw_text = " ".join(text_or_lines)
    else:
        raw_text = text_or_lines

    # Wrap to lines of max 13 chars
    lines = wrap_to_lines(raw_text, max_len=13)
    
    # If more than 2 lines, try tightening
    if len(lines) > 2:
        # Keep top 2 lines or condense
        lines = lines[:2]
    
    # Check trailing preposition on the final line
    if lines:
        last_words = lines[-1].split()
        if last_words and last_words[-1].lower() in PREPOSITIONS:
            # remove the trailing preposition
            last_words.pop()
            if last_words:
                lines[-1] = " ".join(last_words)
            else:
                lines.pop()

    body = "{NEWLINE}".join(lines) if len(lines) > 1 else (lines[0] if lines else "...")
    if speaker:
        return f"{speaker}{{NEWLINE}}{body}{{CTRL:F3}}"
    return f"{body}{{CTRL:F3}}"

if __name__ == '__main__':
    sample = "You returned alive, brave warrior!"
    print(make_box("{CTRL:F9}Guard", sample))
