const fs = require('fs');
const c = fs.readFileSync('insurance-picc.html', 'utf8');
const s = c.match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];

// Track bracket/paren/brace depth per line
let depthP = 0, depthB = 0, depthBr = 0;
const lines = s.split('\n');
for (let li = 0; li < lines.length; li++) {
  const line = lines[li];
  let inStr = null, esc = false;
  for (let ci = 0; ci < line.length; ci++) {
    const ch = line[ci];
    if (esc) { esc = false; continue; }
    if (ch === '\\') { esc = true; continue; }
    if (ch === "'" || ch === '"') {
      if (inStr === ch) inStr = null;
      else if (!inStr) inStr = ch;
      continue;
    }
    if (inStr) continue; // inside string
    if (ch === '(') depthP++;
    else if (ch === ')') depthP--;
    else if (ch === '[') depthB++;
    else if (ch === ']') depthB--;
    else if (ch === '{') depthBr++;
    else if (ch === '}') depthBr--;
  }
  if (depthP < 0 || depthB < 0 || depthBr < 0) {
    console.log('Line ' + (li+1) + ': NEGATIVE DEPTH P=' + depthP + ' B=' + depthB + ' Br=' + depthBr);
    console.log('  => ' + line.trim().substring(0,150));
  }
}
console.log('Final depths: paren=' + depthP + ' bracket=' + depthB + ' brace=' + depthBr);
if (depthP !== 0 || depthB !== 0 || depthBr !== 0) {
  // Show areas where depth changes
  for (let li = 0; li < lines.length; li++) {
    const line = lines[li];
    // Count only non-string brackets
    let lp=0, rp=0, lb=0, rb=0, lbr=0, rbr=0;
    let ins=null, es=false;
    for(let ci=0;ci<line.length;ci++){
      const ch=line[ci];
      if(es){es=false;continue;}
      if(ch==='\\'){es=true;continue;}
      if(ch==="'||ch==='"'){if(ins===ch)ins=null;else if(!ins)ins=ch;continue;}
      if(ins)continue;
      if(ch==='(')lp++;else if(ch===')')rp++;else if(ch==='[')lb++;else if(ch===']')rb++;else if(ch==='{')lbr++;else if(ch==='}')rbr++;
    }
    if(lp+rp+lb+rb+lbr+rbr > 2){
      console.log('L' + (li+1) + ' (ΔP:'+(lp-rp)+' ΔB:'+(lb-rb)+' ΔBr:'+(lbr-rbr)+'): '+line.trim().substring(0,120));
    }
  }
}
