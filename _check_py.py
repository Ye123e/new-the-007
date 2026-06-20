import re

with open('insurance-picc.html', 'r', encoding='utf-8') as f:
    c = f.read()
s = re.search(r'<script[^>]*>(.*?)</script>', c, re.DOTALL).group(1)
lines = s.split('\n')
depthP = depthB = depthBr = 0
for li, line in enumerate(lines):
    i = 0
    inStr = None
    while i < len(line):
        ch = line[i]
        if inStr:
            if ch == '\\' and i + 1 < len(line):
                i += 2
                continue
            if ch == inStr:
                inStr = None
            i += 1
            continue
        if ch in ("'", '"'):
            inStr = ch
            i += 1
            continue
        if ch == '\\' and i + 1 < len(line):
            i += 2
            continue
        if   ch == '(': depthP += 1
        elif ch == ')': depthP -= 1
        elif ch == '[': depthB += 1
        elif ch == ']': depthB -= 1
        elif ch == '{': depthBr += 1
        elif ch == '}': depthBr -= 1
        i += 1
    if depthP < 0 or depthB < 0 or depthBr < 0:
        print(f'Line {li+1}: NEG P={depthP} B={depthB} Br={depthBr}')
        print(f'  => {line.strip()[:150]}')
print(f'Final: paren={depthP} bracket={depthB} brace={depthBr}')

# Also show lines where bracket depth changes a lot (potential issue spots)
if depthP != 0 or depthB != 0 or depthBr != 0:
    print('\n--- Lines with bracket activity ---')
    depthP = depthB = depthBr = 0
    for li, line in enumerate(lines):
        lp = rp = lb = rb = lbr = rbr = 0
        ins = None
        i = 0
        while i < len(line):
            ch = line[i]
            if ins:
                if ch == '\\' and i+1 < len(line): i+=2; continue
                if ch == ins: ins = None
                i+=1; continue
            if ch in ("'",'"'): ins = ch; i+=1; continue
            if ch == '\\\\' and i+1 < len(line): i+=2; continue
            if   ch == '(': lp+=1
            elif ch == ')': rp+=1
            elif ch == '[': lb+=1
            elif ch == ']': rb+=1
            elif ch == '{': lbr+=1
            elif ch == '}': rbr+=1
            i+=1
        delta = (lp-rp)+(lb-rb)+(lbr-rbr)
        if abs(delta) >= 3 or (lp+rp+lb+rb+lbr+rbr) >= 6:
            print(f'L{li+1} (dP:{lp-rp} dB:{lb-rb} dBr:{lbr-rbr}): {line.strip()[:120]}')
