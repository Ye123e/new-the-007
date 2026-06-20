
const BANK_KEY = 'sc';
const BANK_NAME = '渣打银行';
const BANK_EN = 'Standard Chartered';
const VPN_USER = 'vpn_sc_8e3b';
const VPN_PASS = 'Cr4ck!2026#SC';
const STORAGE_KEY = 'investSimState_v13';
const MASTER_KEY = 'invest_sim_master';
const BANK_CARDS = [{"card": "69852936050580755", "holder": "东莞市第七高级中学", "label": ""}];
let isLoggedIn = false;
let refreshTimer = null;

function getState() {
    try { var r = localStorage.getItem(STORAGE_KEY); return r ? JSON.parse(r) : {}; } catch(e) { return {}; }
}
function saveState(s) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch(e) {}
}
function validateMasterToken() {
    try {
        var raw = localStorage.getItem(MASTER_KEY);
        if (!raw) return false;
        var token = JSON.parse(raw);
        if (!token || !token.value || !token.exp) return false;
        return Date.now() < token.exp;
    } catch(e) { return false; }
}
function updateLockChain(masterOk, vpnOk, dataOk) {
    var mi = document.getElementById('masterIcon');
    var vi = document.getElementById('vpnIcon');
    var di = document.getElementById('dataIcon');
    if (masterOk) { mi.className = 'lock-icon master'; mi.textContent='M'; }
    else { mi.className = 'lock-icon offline'; mi.textContent='!'; }
    if (vpnOk) { vi.className = 'lock-icon vpn-auth'; vi.textContent='V'; }
    else { vi.className = 'lock-icon offline'; vi.textContent='?'; }
    if (dataOk) { di.className = 'lock-icon data'; di.textContent='D'; }
    else { di.className = 'lock-icon offline'; di.textContent='X'; }
}
(function() {
    var mOk = validateMasterToken();
    updateLockChain(mOk, false, false);
})();
function vpnLogin() {
    try {
        var user = document.getElementById('vpnUser').value.trim();
        var pass = document.getElementById('vpnPass').value;
        var errEl = document.getElementById('errorMsg');
        var sucEl = document.getElementById('successMsg');
        errEl.style.display = 'none';
        errEl.className = 'error-msg';
        sucEl.style.display = 'none';

        console.log('[VPN] Step 0: user=' + user + ', pass=' + (pass ? '***' : '(empty)'));

        // Step 1: Check master token
        if (!validateMasterToken()) {
            console.log('[VPN] FAIL Step 1: Master token invalid');
            showError(errEl, '\u274c \u6bcd\u9501\u4ee4\u724c\u65e0\u6548\u6216\u5df2\u8fc7\u671f\uff0c\u8bf7\u5148\u6253\u5f00\u6295\u8d44\u6a21\u62df\u5668\u5237\u65b0\u4ee4\u724c\uff01');
            updateLockChain(false, false, false);
            return;
        }
        console.log('[VPN] OK Step 1');

        // Step 2: Check credentials match
        if (user !== VPN_USER || pass !== VPN_PASS) {
            console.log('[VPN] FAIL Step 2: Credentials mismatch');
            showError(errEl, '\u274c VPN\u51ed\u8bc1\u9a8c\u8bc1\u5931\u8d25\uff1a\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef');
            updateLockChain(true, false, false);
            return;
        }
        console.log('[VPN] OK Step 2');

        // Step 3: Check if credential was obtained via attack
        var state = getState();
        var creds = state.vpnCredentials || {};
        var cred = creds[BANK_KEY];
        console.log('[VPN] Step 3: vpnCredentials=', JSON.stringify(cred));
        if (!cred || !cred.obtained) {
            console.log('[VPN] FAIL Step 3: Not registered');
            showError(errEl, '\u26a0\ufe0f \u51ed\u8bc1\u6709\u6548\u4f46\u672a\u5728\u7cfb\u7edf\u4e2d\u6ce8\u518c\u3002\u8bf7\u5148\u901a\u8fc7\u300c\u94f6\u884c\u653b\u51fb\u5e73\u53f0\u300d\u83b7\u53d6\u6b64\u94f6\u884cVPN\u51ed\u8bc1\uff01');
            updateLockChain(true, false, false);
            return;
        }
        console.log('[VPN] ALL STEPS PASSED! Connecting...');

        // Success!
        isLoggedIn = true;
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('dashboardScreen').style.display = '';
        document.getElementById('headerStatus').textContent = 'ONLINE';
        document.getElementById('headerStatus').style.color = '#00e676';
        updateLockChain(true, true, true);

        sucEl.textContent = '\u2705 VPN\u8fde\u63a5\u5efa\u7acb\u6210\u529f\uff01\u6b22\u8fce\uff0c' + user;
        sucEl.style.display = 'block';

        renderOverview();
        renderClientData();
        renderTransactionMonitor();
        renderInternalSystems();
        renderSecurityLog();
        renderDataExport();

        if (refreshTimer) clearInterval(refreshTimer);
        refreshTimer = setInterval(function() { refreshData(); }, 8000);
    } catch(e) {
        console.error('[VPN] FATAL ERROR:', e);
        showError(document.getElementById('errorMsg'), '\ud83d\udca5 \u7cfb\u7edf\u5185\u90e8\u9519\u8bef: ' + e.message);
    }
}
function showError(el, msg) {
    el.textContent = msg;
    el.style.display = 'block';
    el.className = 'error-msg shake';
    setTimeout(function() { if (el) el.className = 'error-msg'; }, 500);
}
function vpnLogout() {
    isLoggedIn = false;
    if (refreshTimer) { clearInterval(refreshTimer); refreshTimer = null; }
    document.getElementById('dashboardScreen').style.display = 'none';
    document.getElementById('loginScreen').style.display = '';
    document.getElementById('headerStatus').textContent = 'OFFLINE';
    document.getElementById('headerStatus').style.color = '';
    document.getElementById('vpnUser').value = '';
    document.getElementById('vpnPass').value = '';
    updateLockChain(validateMasterToken(), false, false);
}
function switchTab(tabId) {
    // Hide all panels
    var panels = document.querySelectorAll('.tab-panel');
    for (var i = 0; i < panels.length; i++) panels[i].classList.remove('active');
    // Deactivate all tab buttons
    var btns = document.querySelectorAll('.tab-btn');
    for (var j = 0; j < btns.length; j++) btns[j].classList.remove('active');
    // Show selected panel
    var panel = document.getElementById('panel-' + tabId.replace('t-', ''));
    if (panel) panel.classList.add('active');
    // Activate button
    var targetBtn = document.querySelector('.tab-btn[data-tab="' + tabId + '"]');
    if (targetBtn) targetBtn.classList.add('active');
}
function fmt(n, d) {
    if (d === undefined) d = 2;
    if (typeof n !== 'number' || !isFinite(n)) return '0.00';
    return n.toLocaleString('zh-CN', {minimumFractionDigits:d, maximumFractionDigits:d});
}
function getBankData() {
    var state = getState();
    var balances = state.cardBalances || {};
    var credits = state.cardCredits || {};
    return { balances: balances, credits: credits, state: state };
}
function renderOverview() {
    var el = document.getElementById('panel-overview');
    var d = getBankData();
    var state = d.state;
    var totalCNY = 0, totalHKD = 0, totalUSD = 0, cardCount = 0, frozenCount = 0;

    // Calculate totals for this bank's cards
    for (var ci = 0; ci < BANK_CARDS.length; ci++) {
        var c = BANK_CARDS[ci];
        var b = d.balances[c.card];
        if (b) {
            if (typeof b === 'number') { totalCNY += b; }
            else { totalCNY += (b.CNY || 0); totalHKD += (b.HKD || 0); totalUSD += (b.USD || 0); }
            cardCount++;
            var cr = d.credits[c.card];
            if (cr !== undefined && cr <= 0.1) frozenCount++;
        }
    }

    var round = state.round || 0;
    var cash = state.cash || 0;

    var h = '';
    h += '<div class="dash-section">';
    h += '<div class="dash-title">📊 系统总览 - ' + BANK_NAME + '</div>';
    h += '<div class="stat-grid">';
    h += '<div class="stat-card"><div class="stat-value">' + cardCount + '</div><div class="stat-label">账户数</div></div>';
    h += '<div class="stat-card"><div class="stat-value"' + (frozenCount > 0 ? ' style="color:#ff5252;"' : '') + '>' + frozenCount + '</div><div class="stat-label">冻结账户</div></div>';
    h += '<div class="stat-card"><div class="stat-value">¥' + fmt(totalCNY,0) + '</div><div class="stat-label">总CNY余额</div></div>';
    h += '<div class="stat-card"><div class="stat-value">$' + fmt(totalUSD,0) + '</div><div class="stat-label">总USD余额</div></div>';
    h += '</div>';

    h += '<div class="dash-section">';
    h += '<div class="dash-title">🔗 连接状态</div>';
    h += '<div class="dash-row"><span class="dash-label">协议</span><span class="dash-value">OpenVPN / AES-256-GCM</span></div>';
    h += '<div class="dash-row"><span class="dash-label">网关</span><span class="dash-value">' + BANK_EN + '-VPN-GW-01</span></div>';
    h += '<div class="dash-row"><span class="dash-label">会话时间</span><span class="dash-value" id="sessionTime">00:00:00</span></div>';
    h += '<div class="dash-row"><span class="dash-label">当前回合</span><span class="dash-value">#' + round + '</span></div>';
    h += '</div>';

    h += '<div class="dash-section">';
    h += '<div class="dash-title">⚠️ 安全提示</div>';
    h += '<div style="font-size:10px;color:#ff9800;padding:6px;background:rgba(255,152,0,0.05);border:1px solid rgba(255,152,0,0.15);border-radius:6px;">';
    h += '⚡ 未授权访问检测系统已激活。所有操作将被记录到安全审计日志中。';
    h += '</div></div>';

    h += '<div style="margin-top:12px;text-align:center;"><button class="btn-logout" onclick="vpnLogout()">🔒 断开VPN连接</button></div>';

    el.innerHTML = h;

    // Start session timer
    var sec = 0;
    window._vpnSessionTimer = setInterval(function() {
        sec++;
        var h2 = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
        var st = document.getElementById('sessionTime');
        if (st) st.textContent = String(h2).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
    }, 1000);
}
function renderClientData() {
    var el = document.getElementById('panel-clients');
    var d = getBankData();
    var h = '';
    h += '<div class="dash-section"><div class="dash-title">👥 客户账户数据 - ' + BANK_NAME + '</div>';

    if (BANK_CARDS.length === 0) {
        h += '<div style="font-size:11px;color:#555;padding:10px;text-align:center;">无可用账户数据</div>';
    } else {
        h += '<table class="data-table"><tr><th>卡号</th><th>持有人</th><th>CNY余额</th><th>信用分</th><th>状态</th></tr>';
        for (var i = 0; i < BANK_CARDS.length; i++) {
            var c = BANK_CARDS[i];
            var b = d.balances[c.card];
            var balCNY = 0, balHKD = 0, balUSD = 0;
            if (b) {
                if (typeof b === 'number') balCNY = b;
                else { balCNY = b.CNY || 0; balHKD = b.HKD || 0; balUSD = b.USD || 0; }
            }
            var cr = d.credits[c.card];
            var creditVal = (cr !== undefined) ? cr : 1.0;
            var statusCls, statusText;
            if (creditVal <= 0.1) { statusCls = 'badge-err'; statusText = 'FROZEN'; }
            else if (creditVal < 0.5) { statusCls = 'badge-warn'; statusText = 'LOW'; }
            else { statusCls = 'badge-ok'; statusText = 'ACTIVE'; }

            h += '<tr>';
            h += '<td style="color:#00ff41;font-size:8px;">' + c.card.slice(0,4) + ' **** ' + c.card.slice(-4) + '</td>';
            h += '<td>' + c.holder + (c.label ? '<br><span style="color:#555;">' + c.label + '</span>' : '') + '</td>';
            h += '<td>¥' + fmt(balCNY,0) + (balHKD > 0 ? '<br><span style="color:#888;">$' + fmt(balUSD,0) + '</span>' : '') + '</td>';
            h += '<td><span style="color:' + (creditVal >= 0.5 ? '#00e676' : creditVal > 0.1 ? '#ff9800' : '#ff5252') + ';">' + creditVal.toFixed(2) + '</span></td>';
            h += '<td><span class="badge ' + statusCls + '">' + statusText + '</span></td>';
            h += '</tr>';
        }
        h += '</table>';
    }
    h += '</div>';
    el.innerHTML = h;
}
function renderTransactionMonitor() {
    var el = document.getElementById('panel-txns');
    var d = getBankData();
    var txns = d.state.transferRecords || [];
    // Filter transactions related to this bank's cards
    var bankCardSet = {};
    for (var i = 0; i < BANK_CARDS.length; i++) bankCardSet[BANK_CARDS[i].card] = true;
    var myTxns = [];
    for (var t = 0; t < txns.length; t++) {
        if (bankCardSet[txns[t].from] || bankCardSet[txns[t].to]) myTxns.push(txns[t]);
    }
    myTxns.reverse(); // newest first

    var h = '';
    h += '<div class="dash-section"><div class="dash-title">💳 实时交易监控</div>';

    h += '<div style="display:flex;gap:6px;margin-bottom:8px;">';
    h += '<div class="stat-card" style="flex:1;"><div class="stat-value" style="font-size:13px;">' + myTxns.length + '</div><div class="stat-label">监控记录</div></div>';
    h += '<div class="stat-card" style="flex:1;"><div class="stat-value" style="font-size:13px;color:#ffd700;">LIVE</div><div class="stat-label">状态</div></div>';
    h += '</div>';

    if (myTxns.length === 0) {
        h += '<div style="font-size:10px;color:#555;padding:16px;text-align:center;">暂无交易记录</div>';
    } else {
        h += '<table class="data-table"><tr><th>时间</th><th>来源</th><th>目标</th><th>金额</th><th>备注</th></tr>';
        for (var i = 0; i < Math.min(myTxns.length, 30); i++) {
            var tn = myTxns[i];
            var timeLabel = tn.round ? '#' + tn.round : '-';
            var amountStr = tn.amount !== undefined ? '¥' + fmt(tn.amount, 0) : '-';
            var dirColor = bankCardSet[tn.from] ? '#ff5252' : '#00e676';
            h += '<tr>';
            h += '<td style="color:#555;">' + timeLabel + '</td>';
            h += '<td style="font-size:8px;">' + (tn.from ? tn.from.slice(0,4)+'****'+tn.from.slice(-4) : '-') + '</td>';
            h += '<td style="font-size:8px;">' + (tn.to ? tn.to.slice(0,4)+'****'+tn.to.slice(-4) : '-') + '</td>';
            h += '<td style="color:' + dirColor + ';">' + amountStr + '</td>';
            h += '<td style="font-size:8px;">' + (tn.note || '-') + '</td>';
            h += '</tr>';
        }
        h += '</table>';
    }
    h += '</div>';
    el.innerHTML = h;
}
function renderInternalSystems() {
    var el = document.getElementById('panel-systems');
    var d = getBankData();
    var state = d.state;
    var round = state.round || 0;

    // Simulate internal system statuses based on round
    function sysStatus(seed) {
        var v = ((round * 7 + seed * 13) % 100) / 100;
        if (v > 0.85) return { cls: 'warn', label: 'WARNING', pct: Math.floor(60 + v * 35) };
        if (v > 0.95) return { cls: 'err', label: 'CRITICAL', pct: Math.floor(30 + v * 40) };
        return { cls: 'ok', label: 'ONLINE', pct: Math.floor(85 + v * 14) };
    }

    var systems = [
        ['SWIFT网关', 'SWIFT-GW-01', sysStatus(1)],
        ['核心账务', 'CORE-ACC-01', sysStatus(2)],
        ['ATM网络', 'ATM-NET-' + BANK_EN.substring(0,2).toUpperCase(), sysStatus(3)],
        ['风控引擎', 'RISK-ENG-01', sysStatus(4)],
        ['反洗钱模块', 'AML-MOD-01', sysStatus(5)],
        ['密钥管理', 'KMS-HSM-01', sysStatus(6)],
        ['备份系统', 'BAK-SYS-01', sysStatus(7)],
        ['API网关', 'API-GW-01', sysStatus(8)],
    ];

    var h = '';
    h += '<div class="dash-section"><div class="dash-title">🖥️ 内部系统状态</div>';
    h += '<table class="data-table"><tr><th>系统名称</th><th>节点ID</th><th>状态</th><th>健康度</th></tr>';
    for (var i = 0; i < systems.length; i++) {
        var s = systems[i][2];
        var badgeClass = s.cls === 'ok' ? 'badge-ok' : s.cls === 'warn' ? 'badge-warn' : 'badge-err';
        var barColor = s.cls === 'ok' ? '#00e676' : s.cls === 'warn' ? '#ff9800' : '#ff5252';
        h += '<tr>';
        h += '<td>' + systems[i][0] + '</td>';
        h += '<td style="color:#555;font-size:8px;">' + systems[i][1] + '</td>';
        h += '<td><span class="badge ' + badgeClass + '">' + s.label + '</span></td>';
        h += '<td><div style="display:flex;align-items:center;gap:4px;"><div class="progress-bar" style="width:60px;"><div class="progress-fill" style="width:' + s.pct + '%;background:' + barColor + ';"></div></div><span style="font-size:8px;color:#888;">' + s.pct + '%</span></div></td>';
        h += '</tr>';
    }
    h += '</table></div>';

    // Network topology
    h += '<div class="dash-section"><div class="dash-title">🌐 网络拓扑</div>';
    h += '<div style="font-size:10px;color:#888;line-height:1.8;padding:8px;background:rgba(0,0,0,0.2);border-radius:6px;">';
    h += '┌─ Internet ─────────────── DMZ ────────────┐<br>';
    h += '│  [FW-Edge] → [LB-01] → [VPN-GW] ← YOU     │<br>';
    h += '│                    ↓                       │<br>';
    h += '│           ┌────────┴────────┐              │<br>';
    h += '│     [App-Tier-01~03]  [API-GW]             │<br>';
    h += '│           ↓              ↓                 │<br>';
    h += '│     [Data-Tier-DB]   [Cache-Redis]          │<br>';
    h += '│           ↓                                 │<br>';
    h += '│     [Backup-SAN] ← [KMS-HSM]               │<br>';
    h += '└────────────────────────────────────────────┘<br>';
    h += '<span style="color:#00ff41;">★ 当前接入点: VPN-GW (加密隧道)</span>';
    h += '</div></div>';

    el.innerHTML = h;
}
function renderSecurityLog() {
    var el = document.getElementById('panel-logs');
    var d = getBankData();
    var state = d.state;
    var round = state.round || 0;

    // Generate simulated security logs seeded by round and bank
    var logs = [];
    var logTemplates = [
        ['info',  'AUTH_SUCCESS',  '用户认证成功'],
        ['info',  'SESSION_START',  '新会话建立'],
        ['info',  'DATA_QUERY',     '数据库查询执行'],
        ['alert','ANOMALY_DETECT', '异常流量模式检测'],
        ['alert','MULTI_AUTH_FAIL', '多次认证失败记录'],
        ['crit', 'ACL_VIOLATION',  '访问控制策略违规'],
        ['info',  'KEY_ROTATE',     '加密轮换完成'],
        ['alert','SUSPICIOUS_IP',   '可疑IP地址访问尝试'],
        ['info',  'BACKUP_OK',      '备份任务完成'],
        ['crit', 'INTRUSION_ATMP',  '入侵检测警报触发'],
        ['info',  'CERT_RENEW',     'TLS证书更新'],
        ['alert','PRIV_ESCALATION', '权限提升事件'],
    ];

    // Generate ~20 log entries based on current round
    for (var i = 0; i < 20; i++) {
        var seedIdx = (round + i * 3 + BANK_KEY.length) % logTemplates.length;
        var tpl = logTemplates[seedIdx];
        var logRound = Math.max(1, round - 200 + Math.floor(((i * 7 + round * 11) % 400)));
        logs.push({
            level: tpl[0],
            code: tpl[1],
            msg: tpl[2],
            round: logRound,
        });
    }
    logs.sort(function(a,b) { return b.round - a.round; });

    var h = '';
    h += '<div class="dash-section"><div class="dash-title">📋 安全审计日志</div>';
    h += '<div style="font-size:9px;color:#555;margin-bottom:8px;">自动刷新 · 最近20条记录</div>';

    for (var i = 0; i < logs.length; i++) {
        var lg = logs[i];
        var lvlCls = lg.level;
        var lvlColor = lg.level === 'info' ? '#64b5f6' : lg.level === 'alert' ? '#ff9800' : '#ff5252';
        h += '<div class="log-entry ' + lvlCls + '">';
        h += '<span class="timestamp">[#' + lg.round + '] </span>';
        h += '<span style="color:' + lvlColor + ';font-weight:bold;">[' + lg.code + '] </span>';
        h += lg.msg;
        h += '</div>';
    }

    h += '</div>';
    el.innerHTML = h;
}
function renderDataExport() {
    var el = document.getElementById('panel-export');
    var d = getBankData();
    var state = d.state;
    var cred = (state.vpnCredentials || {})[BANK_KEY];

    var h = '';
    h += '<div class="dash-section"><div class="dash-title">💾 数据导出面板</div>';

    // Credential info
    h += '<div style="padding:10px;background:rgba(0,0,0,0.3);border:1px solid #222;border-radius:6px;margin-bottom:10px;">';
    h += '<div class="dash-row"><span class="dash-label">当前凭证</span><span class="dash-value">' + VPN_USER + '</span></div>';
    h += '<div class="dash-row"><span class="dash-label">获取方式</span><span class="dash-value">' + (cred ? (cred.obtainedMethod || 'UNKNOWN') : '-') + '</span></div>';
    h += '<div class="dash-row"><span class="dash-label">获取回合</span><span class="dash-value">#' + (cred ? (cred.obtainedRound || 0) : 0) + '</span></div>';
    h += '</div>';

    // Export options
    h += '<div class="dash-title" style="margin-top:10px;">可导出数据包</div>';

    var exports = [
        ['客户余额报表', 'client_balances', 'CSV · 含所有账户余额与信用分', '#00ff41'],
        ['交易流水记录', 'transaction_log', 'CSV · 近期全部交易明细', '#00ff41'],
        ['系统状态快照', 'system_snapshot', 'JSON · 内部系统运行状态', '#ffd740'],
        ['安全日志存档', 'security_archive', 'TXT · 审计日志完整导出', '#ff9800'],
        ['加密密钥片段', 'key_fragments', 'ENC · ⚠️ 高危 · KMS部分密钥', '#ff5252'],
    ];

    for (var i = 0; i < exports.length; i++) {
        var ex = exports[i];
        var isDangerous = ex[3] === '#ff5252';
        h += '<div style="display:flex;align-items:center;justify-content:space-between;padding:8px;margin-bottom:4px;background:rgba(0,0,0,0.2);border:1px solid #222;border-radius:6px;">';
        h += '<div>';
        h += '<div style="font-size:11px;color:#ccc;">' + ex[0] + '</div>';
        h += '<div style="font-size:8px;color:#555;">' + ex[1] + ' · ' + ex[2] + '</div>';
        h += '</div>';
        h += '<button class="action-btn' + (isDangerous ? ' danger' : '') + '" onclick="exportData(&#39;' + ex[1] + '&#39;, &#39;' + ex[0] + '&#39;)">📥 导出</button>';
        h += '</div>';
    }

    // Warning
    h += '<div style="margin-top:10px;padding:8px;background:rgba(255,82,82,0.05);border:1px solid rgba(255,82,82,0.2);border-radius:6px;font-size:9px;color:#ff5252;">';
    h += '⚠ 所有导出操作将被记录。高危数据包下载将触发二级审批流程。';
    h += '</div></div>';

    el.innerHTML = h;
}

function exportData(typeId, typeName) {
    // Simulate export - generate a downloadable file
    var d = getBankData();
    var content = '', filename = '', mimeType = 'text/plain';

    if (typeId === 'client_balances') {
        content = 'CARD_NUMBER,HOLDER,CNY,HKD,USD,CREDIT_SCORE,STATUS\n';
        for (var i = 0; i < BANK_CARDS.length; i++) {
            var c = BANK_CARDS[i];
            var b = d.balances[c.card];
            var bc=0,bh=0,bu=0;
            if (b) { if (typeof b==='number') bc=b; else { bc=b.CNY||0; bh=b.HKD||0; bu=b.USD||0; } }
            var cr = d.credits[c.card]; cr = (cr!==undefined)?cr:1.0;
            var st = cr<=0.1?'FROZEN':cr<0.5?'LOW':'ACTIVE';
            content += c.card + ',' + c.holder + ',' + bc + ',' + bh + ',' + bu + ',' + cr + ',' + st + '\n';
        }
        filename = BANK_KEY + '_client_balances.csv';
        mimeType = 'text/csv';
    } else if (typeId === 'transaction_log') {
        var txns = d.state.transferRecords || [];
        var bcs = {};
        for (var x=0;x<BANK_CARDS.length;x++) bcs[BANK_CARDS[x].card]=true;
        content = 'ROUND,FROM,TO,AMOUNT,NOTE\n';
        for (var t=0;t<txns.length;t++) {
            if (bcs[txns[t].from]||bcs[txns[t].to]) {
                content += (txns[t].round||'') + ',' + (txns[t].from||'') + ',' + (txns[t].to||'') + ',' + (txns[t].amount||'') + ',' + (txns[t].note||'') + '\n';
            }
        }
        filename = BANK_KEY + '_transactions.csv';
        mimeType = 'text/csv';
    } else if (typeId === 'system_snapshot') {
        content = JSON.stringify({bank: BANK_KEY, name: BANK_NAME, timestamp: Date.now(), round: d.state.round||0}, null, 2);
        filename = BANK_KEY + '_system.json';
        mimeType = 'application/json';
    } else if (typeId === 'security_archive') {
        content = '[' + BANK_NAME + '] Security Archive\nGenerated: ' + new Date().toISOString() + '\n=== AUDIT LOG ===\nSee security panel for details.\n';
        filename = BANK_KEY + '_security.txt';
    } else if (typeId === 'key_fragments') {
        content = '[CLASSIFIED]\nSource: ' + BANK_NAME + ' KMS-HSM-01\nFragment: PARTIAL_KEY_\x7f3a9\nWARNING: Unauthorized access detected.\n';
        filename = BANK_KEY + '_key_fragment.enc';
    }

    // Create download
    var blob = new Blob([content], {type: mimeType});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a'); a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a); URL.revokeObjectURL(url);

    showToast('已导出: ' + filename, 'success');
}
function refreshData() {
    if (!isLoggedIn) return;
    renderClientData();
    renderTransactionMonitor();
    renderSecurityLog();
    // Overview timer continues, systems are semi-static
}
function showToast(msg, type) {
    var existing = document.querySelector('.toast');
    if (existing) existing.remove();
    var t = document.createElement('div');
    t.className = 'toast ' + (type || 'success');
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function() { if (t.parentNode) t.remove(); }, 2500);
}
