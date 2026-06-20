#!/usr/bin/env python3
"""Double all single backslash-u escapes in gen_vpn.py to prevent surrogate issues."""

# Read as raw bytes
with open('gen_vpn.py', 'rb') as f:
    raw = f.read()

# Replace all b'\\u' (single backslash-u) with b'\\\\u' (double backslash-u)
# But we need to be careful: only replace when it's NOT already doubled

# Strategy: iterate through and check each backslash
result = bytearray()
i = 0
count = 0
while i < len(raw):
    # Check for backslash followed by 'u'
    if raw[i:i+2] == b'\\u':
        # Check if it's already doubled (preceded by another backslash)
        if i > 0 and raw[i-1] == ord('\\'):
            # Already doubled, keep as-is
            result.extend(b'\\u')
        else:
            # Single backslash-u, need to double it
            result.extend(b'\\\\u')
            count += 1
        i += 2
    else:
        result.append(raw[i])
        i += 1

with open('gen_vpn.py', 'wb') as f:
    f.write(result)

print(f'Doubled {count} single backslash-u escapes')
