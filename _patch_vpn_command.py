#!/usr/bin/env python3
"""Patch gen_vpn.py to add Command tab (wipe/freeze) and darknet link."""
import sys

filepath = 'gen_vpn.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# === 1. Add new tab to both tab lists ===
old_tabs = """    tabs = [
        ('t-overview', '\U0001f4ca \u603b\u89c8'),
        ('t-clients', '\U0001f465 \u5ba2\u6237'),
        ('t-txns', '\U0001f4b3 \u4ea4\u4e8c'),
        ('t-systems', '\U0001f5a5\ufe0f \u7cfb\u7edf'),
        ('t-logs', '\U0001f4cb \u65e5\u5fd7'),
        ('t-export', '\U0001f4be \u5bfc\u51fa'),
    ]"""

new_tabs = """    tabs = [
        ('t-overview', '\U0001f4ca \u603b\u89c8'),
        ('t-clients', '\U0001f465 \u5ba2\u6237'),
        ('t-txns', '\U0001f4b3 \u4ea4\u4e8c'),
        ('t-systems', '\U0001f5a5\ufe0f \u7cfb\u7edf'),
        ('t-logs', '\U0001f4cb \u65e5\u5fd7'),
        ('t-export', '\U0001f4be \u5bfc\u51fa'),
        ('t-command', '\u26a1 \u6307\u4ee4'),
    ]"""

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    changes += 1
    print('[1] Added command tab to tab lists')
else:
    print('[1] SKIP - tab list not found (emoji encoding mismatch)')

# === 2. Add new panel div after both panel-export lines ===
old_panel = "    html += '    <div id=\"panel-export\" class=\"tab-panel\"></div>\\n'"
new_panel = "    html += '    <div id=\"panel-export\" class=\"tab-panel\"></div>\\n'\n    html += '    <div id=\"panel-command\" class=\"tab-panel\"></div>\\n'"

count = content.count(old_panel)
if count >= 2:
    content = content.replace(old_panel, new_panel)
    changes += 1
    print(f'[2] Added panel-command div ({count} locations)')
else:
    print(f'[2] SKIP - panel-export found {count} times')

# === 3. Add CSS for wipe buttons ===
old_css = "    html += '.action-btn.danger { border-color: #ff1744; color: #ff1744; }\\n'"
new_css = old_css + """
    html += '.wipe-btn { background:rgba(255,0,0,0.15); border:2px solid #ff1744; color:#ff1744; font-size:12px; padding:10px 20px; cursor:pointer; border-radius:4px; text-transform:uppercase; letter-spacing:2px; font-weight:bold; transition:all 0.3s; }\\n'
    html += '.wipe-btn:hover { background:rgba(255,0,0,0.3); box-shadow:0 0 15px rgba(255,0,0,0.4); }\\n'
    html += '.wipe-btn:disabled { opacity:0.3; cursor:not-allowed; }\\n'
    html += '.confirm-overlay { position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.85); z-index:9998; display:flex; align-items:center; justify-content:center; }\\n'
    html += '.confirm-box { background:#111; border:2px solid #ff1744; padding:20px; border-radius:8px; max-width:400px; text-align:center; }\\n'
    html += '.confirm-box h3 { color:#ff1744; margin-bottom:12px; }\\n'
    html += '.confirm-box .btn-row { display:flex; gap:10px; justify-content:center; margin-top:15px; }\\n'"""

count = content.count(old_css)
if count >= 2:
    content = content.replace(old_css, new_css)
    changes += 1
    print(f'[3] Added wipe CSS ({count} locations)')
else:
    print(f'[3] SKIP - action-btn.danger found {count} times')

# === 4. Add renderCommandTab() call in vpnLogin success ===
old_render = "        renderDataExport();"
new_render = "        renderDataExport();\n        renderCommandTab();"

count = content.count(old_render)
# Only replace the 2 vpnLogin success sections (not inside renderDataExport function def)
# There should be exactly 2 occurrences in vpnLogin
if count >= 2:
    content = content.replace(old_render, new_render)
    changes += 1
    print(f'[4] Added renderCommandTab() call ({count} vpnLogin sections)')
else:
    print(f'[4] SKIP - renderDataExport call found {count} times')

# === 5. Add command tab functions after exportData ===
# Build the JS function block
command_js = r"""
    # --- Panel 7: Command Tab (wipe/freeze) ---
    html += '''function renderCommandTab() {
    var el = document.getElementById('panel-command');
    var d = getBankData();
    var state = d.state;
    var hasPurged = state._vpnDataPurged && state._vpnDataPurged[BANK_KEY];
    var h = '';
    h += '<div class="dash-section">';
    h += '<div class="dash-title">\u26a1 \u8fdc\u7a0b\u6307\u4ee4\u63a7\u5236\u53f0</div>';
    h += '<div style="padding:8px;background:rgba(0,0,0,0.3);border:1px solid #222;border-radius:6px;margin-bottom:10px;">';
    if (hasPurged) {
        h += '<div style="color:#ff1744;font-size:12px;">\ud83d\udd34 \u6570\u636e\u6e05\u6d01\u6307\u4ee4\u5df2\u6267\u884c \u2014 ' + BANK_NAME + ' \u6570\u636e\u5e93\u5df2\u88ab\u64e6\u5012</div>';
        h += '<div style="font-size:9px;color:#555;margin-top:4px;">\u6267\u884c\u56de\u5408: #' + (state._vpnDataPurged[BANK_KEY].round || '?') + '</div>';
    } else {
        h += '<div style="color:#00ff41;font-size:12px;">\ud83d\udfe1 \u7cfb\u7edf\u6b63\u5e38 \u2014 \u6570\u636e\u5b8c\u6574</div>';
    }
    h += '</div>';
    h += '<div class="dash-title">\u53ef\u7528\u6307\u4ee4</div>';
    if (!hasPurged) {
        h += '<div style="display:flex;align-items:center;justify-content:space-between;padding:10px;margin-bottom:6px;background:rgba(255,0,0,0.05);border:1px solid rgba(255,0,0,0.2);border-radius:6px;">';
        h += '<div>';
        h += '<div style="font-size:11px;color:#ff1744;">\ud83d\udc80 PURGE-DATA-ALL</div>';
        h += '<div style="font-size:8px;color:#555;">\u6e05\u9664\u6240\u6709\u94f6\u884c\u5ba2\u6237\u6570\u636e \u00b7 \u4f59\u989d\u6e05\u970d \u00b7 \u4fe1\u7528\u5206\u91cd\u7f6e \u00b7 \u4ea4\u4e8c\u8bb0\u5f55\u5220\u9664</div>';
        h += '<div style="font-size:8px;color:#ff9800;">\u26a0 \u4e0d\u53ef\u9006\u64cd\u4f5c \u00b7 \u6e05\u9664\u540e\u53ef\u5728\u6697\u7f51\u51fa\u5512\u6570\u636e\u5e93\u832a\u9e97</div>';
        h += '</div>';
        h += '<button class="wipe-btn" onclick="confirmWipe()">\ud83d\udc80 \u6267\u884c</button>';
        h += '</div>';
        h += '<div style="display:flex;align-items:center;justify-content:space-between;padding:10px;margin-bottom:6px;background:rgba(255,152,0,0.05);border:1px solid rgba(255,152,0,0.2);border-radius:6px;">';
        h += '<div>';
        h += '<div style="font-size:11px;color:#ff9800;">\ud83d\udd12 FREEZE-ALL-ACCTS</div>';
        h += '<div style="font-size:8px;color:#555;">\u51bb\u7f9e\u6240\u6709\u5ba2\u6237\u8d26\u6237 \u00b7 \u4fe1\u7528\u5206\u964d\u81f30.1 \u00b7 \u7981\u6b62\u6240\u6709\u8f6c\u8d26</div>';
        h += '</div>';
        h += '<button class="wipe-btn" style="border-color:#ff9800;color:#ff9800;" onclick="confirmFreeze()">\ud83d\udd12 \u6267\u884c</button>';
        h += '</div>';
    }
    h += '<div style="margin-top:10px;padding:8px;background:rgba(255,82,82,0.05);border:1px solid rgba(255,82,82,0.2);border-radius:6px;font-size:9px;color:#ff5252;">';
    h += '\u26a0 \u6307\u4ee4\u6267\u884c\u5c06\u89e6\u53d1\u6700\u9ad8\u7ea7\u522b\u5b89\u5168\u8c03\u94db\u3002\u64cd\u4f5c\u4e0d\u53ef\u9006\u3002';
    h += '</div></div>';
    el.innerHTML = h;
}

function confirmWipe() {
    var overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.id = 'wipeOverlay';
    overlay.innerHTML = '<div class="confirm-box">' +
        '<h3>\ud83d\udc80 \u786e\u8ba4\u6e05\u9664\u6240\u6709\u6570\u636e\uff1f</h3>' +
        '<div style="font-size:11px;color:#aaa;margin-bottom:8px;">\u6b64\u64cd\u4f5c\u5c06\uff1a</div>' +
        '<div style="font-size:10px;color:#ff1744;line-height:1.6;">' +
        '\u2022 \u6240\u6709\u94f6\u884c\u5361\u4f59\u989d \u2192 \u00a50<br>' +
        '\u2022 \u6240\u6709\u4fe1\u7528\u5206 \u2192 1.0<br>' +
        '\u2022 \u6240\u6709\u8f6c\u8d26\u8bb0\u5f55 \u2192 \u5220\u9664<br>' +
        '\u2022 \u6240\u6709\u652f\u7807 \u2192 \u5220\u9664<br>' +
        '\u2022 \u6240\u6709\u8d37\u6b3e \u2192 \u5220\u9664<br>' +
        '\u2022 \u6807\u8bb3\u6570\u636e\u5e93\u5df2\u6e05\u9664\uff08\u53ef\u5728\u6697\u7f51\u51fa\u5512\uff09<br>' +
        '</div>' +
        '<div style="font-size:9px;color:#ff9800;margin-top:6px;">\u26a0 \u4e0d\u53ef\u9006\uff01\u786e\u8ba4\u8bf7\u8f93\u8f93\u8f93\u5165: ' + BANK_KEY + '</div>' +
        '<div style="margin-top:10px;"><input id="wipeConfirmInput" style="background:#000;border:1px solid #ff1744;color:#ff1744;padding:6px;width:200px;font-size:12px;text-align:center;" placeholder="\u8f93\u5165\u786e\u8ba4\u7801"></div>' +
        '<div class="btn-row">' +
        '<button class="wipe-btn" onclick="executeWipe()">\ud83d\udc80 \u786e\u8ba4\u6e05\u9664</button>' +
        '<button class="action-btn" onclick="closeOverlay()">\u53d6\u6d88</button>' +
        '</div></div>';
    document.body.appendChild(overlay);
}

function executeWipe() {
    var input = document.getElementById('wipeConfirmInput').value.trim().toLowerCase();
    if (input !== BANK_KEY.toLowerCase()) {
        showToast('\u786e\u8ba4\u7801\u9519\u8bef\uff01\u6307\u4ee4\u7ec8\u6b62', 'error');
        closeOverlay();
        return;
    }
    var state = getState();
    var balances = state.cardBalances || {};
    var credits = state.cardCredits || {};
    for (var i = 0; i < BANK_CARDS.length; i++) {
        var card = BANK_CARDS[i].card;
        if (balances[card]) {
            if (typeof balances[card] === 'number') balances[card] = 0;
            else { balances[card].CNY = 0; balances[card].HKD = 0; balances[card].USD = 0; }
        }
        credits[card] = 1.0;
    }
    state.cheques = [];
    state.transferRecords = [];
    state.loans = [];
    state._vpnDataPurged = state._vpnDataPurged || {};
    state._vpnDataPurged[BANK_KEY] = { round: state.round || 0, bankName: BANK_NAME, timestamp: Date.now() };
    saveState(state);
    closeOverlay();
    renderCommandTab();
    renderOverview();
    renderClientData();
    showToast('\ud83d\udc80 \u6570\u636e\u6e05\u9664\u6307\u4ee4\u5df2\u6267\u884c\uff01' + BANK_NAME + ' \u6240\u6709\u6570\u636e\u5df2\u64e6\u5012', 'error');
}

function confirmFreeze() {
    var overlay = document.createElement('div');
    overlay.className = 'confirm-overlay';
    overlay.id = 'freezeOverlay';
    overlay.innerHTML = '<div class="confirm-box">' +
        '<h3>\ud83d\udd12 \u786e\u8ba4\u51bb\u7f9e\u6240\u6709\u8d26\u6237\uff1f</h3>' +
        '<div style="font-size:10px;color:#ff9800;line-height:1.6;">' +
        '\u2022 \u6240\u6709\u4fe1\u7528\u5206 \u2192 0.1\uff08\u51bb\u7f9e\uff09<br>' +
        '\u2022 \u6240\u6709\u8f6c\u8d26\u529f\u80fd \u2192 \u7981\u6b62<br>' +
        '</div>' +
        '<div class="btn-row">' +
        '<button class="wipe-btn" style="border-color:#ff9800;color:#ff9800;" onclick="executeFreeze()">\ud83d\udd12 \u786e\u8ba4\u51bb\u7f9e</button>' +
        '<button class="action-btn" onclick="closeOverlay()">\u53d6\u6d88</button>' +
        '</div></div>';
    document.body.appendChild(overlay);
}

function executeFreeze() {
    var state = getState();
    var credits = state.cardCredits || {};
    for (var i = 0; i < BANK_CARDS.length; i++) {
        credits[BANK_CARDS[i].card] = 0.1;
    }
    saveState(state);
    closeOverlay();
    renderCommandTab();
    renderOverview();
    renderClientData();
    showToast('\ud83d\udd12 \u6240\u6709\u8d26\u6237\u5df2\u51bb\u7f9e\uff01', 'error');
}

function closeOverlay() {
    var o = document.getElementById('wipeOverlay');
    if (o) o.remove();
    var f = document.getElementById('freezeOverlay');
    if (f) f.remove();
}
'''

    # --- Refresh data (re-render active panels) ---"""

# Find the marker: exportData end + refreshData section start
marker = "    showToast('\u5df2\u5bfc\u51fa: ' + filename, 'success');\n}\n'''\n\n    # --- Refresh data (re-render active panels) ---"

if marker in content:
    # Replace just the first occurrence (the second JS block)
    # Actually there are 2 occurrences - but the first one is the old/duplicate JS block
    # We want to replace both
    content = content.replace(marker, command_js)
    changes += 1
    print('[5] Added renderCommandTab + command functions (both JS blocks)')
else:
    print('[5] SKIP - exportData end marker not found')
    # Debug
    idx = content.find("showToast('\u5df2\u5bfc\u51fa")
    if idx >= 0:
        print(f'  Found at pos {idx}, context: {repr(content[idx:idx+80])}')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')
print('Done! Run gen_vpn.py to regenerate pages.')
