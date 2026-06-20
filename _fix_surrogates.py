#!/usr/bin/env python3
"""Fix single-backslash backslash-u escapes in gen_vpn.py that create surrogates."""

import re

with open('gen_vpn.py', 'r', encoding='utf-8') as f:
    content = f.read()

# In Python ''' strings, \uXXXX is interpreted as Python unicode escape
# For surrogate pairs (emoji), this creates lone surrogates that can't be written to UTF-8
# We need to escape them as \\uXXXX so Python outputs them as literal \uXXXX for JS

# Find all lines with \uXXXX (single backslash) that are NOT preceded by another backslash
# Pattern: backslash-u-4hexdigits, where the backslash is NOT doubled

# We'll do line-by-line replacement
lines = content.split('\n')
fixed_lines = []
count = 0

for i, line in enumerate(lines):
    # Check if this line has \uXXXX patterns
    # Match: \u followed by 4 hex digits, not preceded by another \
    # In regex: r'(?<!\\)\\u([0-9a-fA-F]{4})'
    # But we need to be careful with raw strings
    new_line = re.sub(r'(?<!\\)\\u([0-9a-fA-F]{4})', r'\\u\1', line)
    if new_line != line:
        count += 1
        print(f'Fixed line {i+1}')
    fixed_lines.append(new_line)

content = '\n'.join(fixed_lines)

with open('gen_vpn.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Total: Fixed {count} lines')
