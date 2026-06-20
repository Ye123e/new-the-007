import json
import datetime

brokers = {
    'citics': {
        'name': '中信证券',
        'en': 'CITIC Securities',
        'color': '#ff6d00',
        'emoji': '🏛️',
        'region': 'mainland',
        'commission': 0.0003,
        'accounts': [
            {'holder': '叶珒铭', 'account': 'A88810001'},
            {'holder': '东莞市第二高级中学', 'account': 'A88820001'},
            {'holder': '复旦大学', 'account': 'A88830001'},
            {'holder': '上海交通大学', 'account': 'A88840001'},
        ]
    },
    'goldman': {
        'name': '高盛证券',
        'en': 'Goldman Sachs',
        'color': '#7b1fa2',
        'emoji': '💎',
        'region': 'hongkong',
        'commission': 0.0005,
        'accounts': [
            {'holder': '叶珒铭', 'account': 'G90010001'},
            {'holder': '华东师范大学', 'account': 'G90020001'},
        ]
    }
}

# Stock list (must match invest-sim.html asset keys)
STOCKS = [
    {'key': 'tech', 'name': '科技股(Tech)', 'color': '#2196f3'},
    {'key': 'energy', 'name': '能源股(Energy)', 'color': '#ff9800'},
    {'key': 'medical', 'name': '医疗股(Medical)', 'color': '#4caf50'},
    {'key': 'mining_stock', 'name': '矿业股(Mining)', 'color': '#9c27b0'},
]


def generate_broker_page(key, broker):
    accounts_json = json.dumps(broker['accounts'], ensure_ascii=False)
    n = broker['name']
    en = broker['en']
    color = broker['color']
    emoji = broker['emoji']
    comm = broker['commission']

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html += '<title>' + n + ' - 证券交易系统</title>\n'
    html += '<style>\n'
    html += '* { margin:0; padding:0; box-sizing:border-box; }\n'
    html += 'body { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; background: linear-gradient(135deg,#0a0e27 0%,#1a1f3a 50%,#0d1126 100%); min-height:100vh; display:flex; flex-direction:column; align-items:center; color:#e0e0e0; }\n'

    # Header
    html += '.header { width:100%; padding:30px 20px 16px; text-align:center; background: linear-gradient(180deg,rgba(0,0,0,0.3) 0%,transparent 100%); }\n'
    html += '.bank-logo { font-size:48px; margin-bottom:8px; }\n'
    html += '.bank-name { font-size:26px; font-weight:700; color:' + color + '; letter-spacing:2px; }\n'
    html += '.bank-en { font-size:12px; color:#888; margin-top:4px; letter-spacing:1px; }\n'
    html += '.container { width:100%; max-width:420px; padding:0 20px; margin-top:20px; }\n'
    html += '.card { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:28px; backdrop-filter:blur(10px); margin-bottom:16px; }\n'
    html += '.card-title { font-size:16px; font-weight:600; text-align:center; margin-bottom:20px; color:#fff; }\n'

    # Lock chain CSS
    html += '.lock-chain { display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:20px; padding:12px 16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; flex-wrap:wrap; }\n'
    html += '.lock-node { display:flex; flex-direction:column; align-items:center; gap:4px; min-width:70px; }\n'
    html += '.lock-node .lock-icon { width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:16px; border:2px solid; }\n'
    html += '.lock-node .lock-icon.master { background:rgba(0,230,118,0.1); border-color:rgba(0,230,118,0.4); color:#00e676; }\n'
    html += '.lock-node .lock-icon.sub { background:' + color + '15; border-color:' + color + '66; color:' + color + '; }\n'
    html += '.lock-node .lock-icon.data { background:rgba(255,193,7,0.1); border-color:rgba(255,193,7,0.4); color:#ffc107; }\n'
    html += '.lock-node .lock-icon.offline { background:rgba(255,82,82,0.1); border-color:rgba(255,82,82,0.4); color:#ff5252; animation:pulse-red 1.5s infinite; }\n'
    html += '@keyframes pulse-red { 0%,100%{opacity:1} 50%{opacity:0.5} }\n'
    html += '.lock-node .lock-label { font-size:10px; color:#888; font-weight:500; text-align:center; }\n'
    html += '.lock-arrow { font-size:14px; color:#555; }\n'
    html += '.lock-chain-status { text-align:center; font-size:10px; margin-top:6px; }\n'
    html += '.lock-chain-status.ok { color:#00e676; }\n'
    html += '.lock-chain-status.err { color:#ff5252; }\n'

    # Form CSS
    html += '.form-group { margin-bottom:16px; }\n'
    html += '.form-group label { display:block; font-size:12px; color:#9e9e9e; margin-bottom:6px; }\n'
    html += '.form-group select, .form-group input { width:100%; padding:11px 13px; border-radius:10px; border:1px solid rgba(255,255,255,0.1); background:rgba(0,0,0,0.2); color:#e0e0e0; font-size:14px; outline:none; transition:border-color 0.2s; }\n'
    html += '.form-group select:focus, .form-group input:focus { border-color:' + color + '; }\n'
    html += '.form-group select option { background:#1a1f3a; color:#e0e0e0; }\n'
    html += '.btn { width:100%; padding:12px; border-radius:10px; border:none; background:linear-gradient(135deg,' + color + ',' + color + 'dd); color:#fff; font-size:14px; font-weight:600; cursor:pointer; transition:transform 0.15s,box-shadow 0.15s; margin-top:4px; }\n'
    html += '.btn:hover { transform:translateY(-1px); box-shadow:0 4px 20px ' + color + '44; }\n'
    html += '.btn:disabled { opacity:0.4; cursor:not-allowed; transform:none; box-shadow:none; }\n'
    html += '.btn-outline { background:transparent; border:1px solid rgba(255,255,255,0.1); color:#9e9e9e; margin-top:8px; }\n'
    html += '.btn-outline:hover { border-color:' + color + '; color:' + color + '; box-shadow:none; }\n'
    html += '.hint { font-size:11px; color:#555; text-align:center; margin-top:12px; }\n'
    html += '.error-msg { font-size:12px; color:#ff5252; text-align:center; margin-top:-8px; margin-bottom:8px; display:none; }\n'
    html += '.success-msg { font-size:12px; color:#00e676; text-align:center; margin-top:-8px; margin-bottom:8px; display:none; }\n'

    # Tabs
    html += '.tabs { display:flex; gap:0; margin-bottom:16px; background:rgba(255,255,255,0.04); border-radius:12px; border:1px solid rgba(255,255,255,0.08); overflow:hidden; flex-wrap:wrap; }\n'
    html += '.tab-btn { flex:1; padding:10px 6px; border:none; background:transparent; color:#888; font-size:12px; font-weight:500; cursor:pointer; transition:all 0.2s; white-space:nowrap; }\n'
    html += '.tab-btn.active { background:' + color + '22; color:' + color + '; }\n'

    # Dashboard rows
    html += '.acc-header { display:flex; align-items:center; gap:12px; margin-bottom:16px; padding-bottom:14px; border-bottom:1px solid rgba(255,255,255,0.06); }\n'
    html += '.acc-avatar { width:42px; height:42px; border-radius:50%; background:' + color + '22; border:1px solid ' + color + '44; display:flex; align-items:center; justify-content:center; font-size:18px; }\n'
    html += '.bal-row { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.04); }\n'
    html += '.bal-row:last-child { border-bottom:none; }\n'
    html += '.bal-label { font-size:12px; color:#9e9e9e; }\n'
    html += '.bal-value { font-size:17px; font-weight:700; color:' + color + '; }\n'

    # Stock trading
    html += '.stock-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px; }\n'
    html += '.stock-item { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:12px; text-align:center; cursor:pointer; transition:all 0.15s; }\n'
    html += '.stock-item:hover { border-color:' + color + '66; background:' + color + '10; }\n'
    html += '.stock-item.selected { border-color:' + color + '; background:' + color + '18; }\n'
    html += '.stock-name { font-size:13px; font-weight:600; margin-bottom:4px; }\n'
    html += '.stock-price { font-size:18px; font-weight:700; color:' + color + '; }\n'
    html += '.stock-change { font-size:11px; margin-top:2px; }\n'
    html += '.stock-change.up { color:#ff5252; }  # Chinese market: red=up\n'
    html += '.stock-change.down { color:#00e676; }  # green=down\n'
    html += '.trade-form { margin-top:14px; padding:14px; background:rgba(255,255,255,0.02); border-radius:10px; }\n'
    html += '.trade-info { font-size:11px; color:#aaa; margin-bottom:10px; line-height:1.7; }\n'
    html += '.trade-calc { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed rgba(255,255,255,0.08); font-size:13px; }\n'
    html += '.trade-calc span:last-child { font-weight:700; color:' + color + '; }\n'
    html += '.trade-buttons { display:flex; gap:10px; margin-top:12px; }\n'
    html += '.trade-buttons button { flex:1; padding:10px; border:none; border-radius:10px; font-size:14px; font-weight:600; cursor:pointer; transition:all 0.15s; }\n'
    html += '.trade-buttons .buy-btn { background:linear-gradient(135deg,#ff5252,#ff1744); color:#fff; }\n'
    html += '.trade-buttons .sell-btn { background:linear-gradient(135deg,#00e676,#00c853); color:#fff; }\n'
    html += '.trade-buttons button:hover { transform:translateY(-1px); box-shadow:0 4px 15px rgba(0,0,0,0.3); }\n'
    html += '.trade-buttons button:disabled { opacity:0.35; cursor:not-allowed; transform:none; box-shadow:none; }\n'

    # Position table
    html += '.pos-table { width:100%; border-collapse:collapse; }\n'
    html += '.pos-table th { text-align:left; font-size:11px; color:#888; padding:8px 6px; border-bottom:1px solid rgba(255,255,255,0.08); font-weight:500; }\n'
    html += '.pos-table td { padding:10px 6px; border-bottom:1px solid rgba(255,255,255,0.04); font-size:13px; vertical-align:top; }\n'
    html += '.pos-profit { font-weight:700; }\n'
    html += '.pos-profit.positive { color:#ff5252; }\n'   # red = profit in China
    html += '.pos-profit.negative { color:#00e676; }\n'  # green = loss

    # Order records
    html += '.order-item { padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.04); }\n'
    html += '.order-item:last-child { border-bottom:none; }\n'
    html += '.order-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }\n'
    html += '.order-type { font-size:12px; padding:2px 8px; border-radius:4px; font-weight:600; }\n'
    html += '.order-type.buy { background:rgba(255,82,82,0.15); color:#ff5252; }\n'
    html += '.order-type.sell { background:rgba(0,230,118,0.15); color:#00e676; }\n'
    html += '.order-amount { font-weight:700; font-size:14px; }\n'
    html += '.order-detail { font-size:11px; color:#888; margin-top:2px; }\n'
    html += '.order-empty { text-align:center; color:#555; font-size:12px; padding:20px 0; }\n'
    html += '.order-list { max-height:360px; overflow-y:auto; }\n'

    # Credit badge
    html += '.credit-badge { display:inline-block; font-size:11px; padding:2px 8px; border-radius:6px; font-weight:600; }\n'
    html += '.credit-badge.high { background:rgba(0,230,118,0.15); color:#00e676; }\n'
    html += '.credit-badge.mid { background:rgba(255,193,7,0.15); color:#ffc107; }\n'
    html += '.credit-badge.low { background:rgba(255,82,82,0.15); color:#ff5252; }\n'
    html += '.credit-badge.frozen { background:rgba(255,23,68,0.25); color:#ff1744; }\n'

    # Footer
    html += '.footer { margin-top:auto; padding:20px; font-size:11px; color:#444; text-align:center; }\n'
    html += '</style>\n</head>\n<body>\n'

    # Header
    html += '<div class="header"><div class="bank-logo">' + emoji + '</div><div class="bank-name">' + n + '</div><div class="bank-en">' + en + ' - Securities Trading Platform</div></div>\n'
    html += '<div class="container">\n'

    # Lock chain on login page
    html += '<div class="lock-chain" id="lockChain">\n'
    html += '  <div class="lock-node"><div class="lock-icon offline" id="masterLockIcon">🔒</div><div class="lock-label">母锁<br><span id="masterLockLabel" style="font-size:9px;color:#ff5252;">验证中</span></div></div>\n'
    html += '  <div class="lock-arrow">→</div>\n'
    html += '  <div class="lock-node"><div class="lock-icon sub" id="subLockIcon">🔐</div><div class="lock-label">子锁<br><span style="font-size:9px;">' + n + '</span></div></div>\n'
    html += '  <div class="lock-arrow">→</div>\n'
    html += '  <div class="lock-node"><div class="lock-icon data" id="dataLockIcon">📋</div><div class="lock-label">数据<br><span style="font-size:9px;">交易/持仓</span></div></div>\n'
    html += '</div>\n'
    html += '<div class="lock-chain-status err" id="lockChainStatus">正在验证母锁授权...</div>\n'

    # Login card
    html += '<div class="card" id="loginCard">\n'
    html += '<div class="card-title">证券账户登录</div>\n'
    html += '<div class="form-group"><label>选择证券账户</label><select id="accountSelect"><option value="">请选择账户</option></select></div>\n'
    html += '<div class="form-group"><label>交易密码</label><input type="password" id="pwdInput" placeholder="请输入账号后6位"></div>\n'
    html += '<div class="error-msg" id="loginError"></div>\n'
    html += '<button class="btn" id="loginBtn">登录交易</button>\n'
    html += '<div class="hint">密码为您的证券账号后6位数字（如 A88810001 → 输入 810001）</div>\n'
    html += '</div>\n'

    # Dashboard
    html += '<div id="dashboard" style="display:none;">\n'
    html += '<div class="lock-chain" style="margin-bottom:12px;">\n'
    html += '  <div class="lock-node"><div class="lock-icon master" id="masterLockIcon2">🔓</div><div class="lock-label">母锁<br><span style="font-size:9px;color:#00e676;">已授权</span></div></div>\n'
    html += '  <div class="lock-arrow">→</div>\n'
    html += '  <div class="lock-node"><div class="lock-icon sub">🔐</div><div class="lock-label">子锁<br><span style="font-size:9px;">' + n + '</span></div></div>\n'
    html += '  <div class="lock-arrow">→</div>\n'
    html += '  <div class="lock-node"><div class="lock-icon data">📋</div><div class="lock-label">数据<br><span style="font-size:9px;">交易已就绪</span></div></div>\n'
    html += '</div>\n'

    # Tab buttons: 4 tabs
    html += '<div class="tabs">'
    html += '<button class="tab-btn active" data-tab="overview">账户概览</button>'
    html += '<button class="tab-btn" data-tab="trade">股票交易</button>'
    html += '<button class="tab-btn" data-tab="positions">持仓查询</button>'
    html += '<button class="tab-btn" data-tab="orders">委托记录</button>'
    html += '</div>\n'

    # === Overview Tab ===
    html += '<div class="card" id="tabOverview">\n'
    html += '<div class="card-title">账户信息</div>\n'
    html += '<div class="acc-header"><div class="acc-avatar">📊</div><div class="acc-info"><h3 id="accHolder" style="font-size:15px;margin-bottom:2px;">--</h3><p id="accAccount" style="font-size:12px;color:#888;">--</p></div></div>\n'
    html += '<div class="bal-row"><span class="bal-label">可用资金</span><span class="bal-value" id="accBalance">¥0.00</span></div>\n'
    html += '<div class="bal-row"><span class="bal-label">总资产市值</span><span class="bal-value" id="totalValue" style="font-size:15px;color:#ffc107;">¥0.00</span></div>\n'
    html += '<div class="bal-row"><span class="bal-label">今日盈亏</span><span class="bal-value" id="todayPnL" style="font-size:15px;">¥0.00</span></div>\n'
    html += '<div class="bal-row"><span class="bal-label">佣金费率</span><span style="font-size:14px;color:#aaa;">' + str(comm * 100).rstrip('0').rstrip('.') + '%（最低 ¥5）</span></div>\n'
    html += '<div class="bal-row"><span class="bal-label">母锁状态</span><span id="masterStatusDash" style="font-size:13px;">--</span></div>\n'
    html += '<div class="bal-row"><span class="bal-label">券商地区</span><span style="font-size:13px;color:#aaa;">' + ('内地' if broker.get('region') == 'mainland' else '香港') + '</span></div>\n'
    html += '</div>\n'

    # === Trade Tab ===
    html += '<div class="card" id="tabTrade" style="display:none;">\n'
    html += '<div class="card-title">股票交易</div>\n'
    html += '<div class="trade-info">选择股票 → 输入数量 → 确认买入/卖出 · 佣金 ' + str(comm * 100).rstrip('0').rstrip('.') + '%（最低 ¥5）</div>\n'
    # Stock selection grid
    html += '<div class="stock-grid" id="stockGrid">\n'
    for s in STOCKS:
        html += '  <div class="stock-item" data-stock="' + s['key'] + '" onclick="selectStock(\'' + s['key'] + '\')">\n'
        html += '    <div class="stock-name">' + s['name'] + '</div>\n'
        html += '    <div class="stock-price" id="price_' + s['key'] + '">--</div>\n'
        html += '    <div class="stock-change" id="change_' + s['key'] + '">--</div>\n'
        html += '  </div>\n'
    html += '</div>\n'
    # Trade form
    html += '<div class="trade-form">\n'
    html += '  <div class="form-group"><label>当前选中：<span id="selectedStockName" style="color:' + color + ';font-weight:600;">未选择</span> | 价格：<span id="selectedPrice" style="color:' + color + ';">--</span></label></div>\n'
    html += '  <div class="form-group"><label>交易数量</label><input type="number" id="tradeAmount" placeholder="输入股数" min="1" step="1" value="100"></div>\n'
    html += '  <div class="trade-calc"><span>预估金额</span><span id="calcAmount">¥0.00</span></div>\n'
    html += '  <div class="trade-calc"><span>佣金</span><span id="calcCommission">¥0.00</span></div>\n'
    html += '  <div class="trade-calc" style="border-bottom:none;"><span>合计</span><span id="calcTotal" style="color:#ffc107;font-size:15px;">¥0.00</span></div>\n'
    html += '  <div class="error-msg" id="tradeError"></div>\n'
    html += '  <div class="success-msg" id="tradeSuccess"></div>\n'
    html += '  <div class="trade-buttons">\n'
    html += '    <button class="buy-btn" id="buyBtn" onclick="executeTrade(\'buy\')">📈 买入</button>\n'
    html += '    <    <button class="sell-btn" id="sellBtn" onclick="executeTrade(\'sell\')">📉 卖出</button>\n'
    html += '  </div>\n'
    html += '</div>\n'
    html += '</div>\n'

    # === Positions Tab ===
    html += '<div class="card" id="tabPositions" style="display:none;">\n'
    html += '<div class="card-title">当前持仓</div>\n'
    html += '<table class="pos-table" id="posTable">\n'
    html += '<thead><tr><th>股票</th><th>持有量</th><th>成本价</th><th>现价</th><th>市值</th><th>盈亏</th><th>收益率</th></tr></thead>\n'
    html += '<tbody id="posBody"><tr><td colspan="7" style="text-align:center;color:#555;padding:20px;">暂无持仓</td></tr></tbody>\n'
    html += '</table>\n'
    html += '</div>\n'

    # === Orders Tab ===
    html += '<div class="card" id="tabOrders" style="display:none;">\n'
    html += '<div class="card-title">委托记录</div>\n'
    html += '<div class="order-list" id="orderList"><div class="order-empty">暂无委托记录</div></div>\n'
    html += '</div>\n'

    html += '<button class="btn btn-outline" id="backBtn">↩ 退出登录</button>\n'
    html += '</div>\n</div>\n'
    html += '<div class="footer">&copy; ' + n + ' ' + en + ' | 证券交易系统 v1.0 | 子母锁安全保护</div>\n'

    # ========== JavaScript ==========
    html += '<script>\n'
    html += 'var BROKER_KEY = "' + key + '";\n'
    html += 'var BROKER_NAME = "' + n + '";\n'
    html += 'var BROKER_COMM = ' + str(comm) + ';\n'
    html += 'var BROKER_COLOR = "' + color + '";\n'
    html += 'var ACCOUNTS = ' + accounts_json + ';\n'
    html += 'var currentAccount = null;\n'
    html += 'var selectedStock = null;\n'
    html += 'var masterTokenValid = false;\n'
    html += 'var MIN_COMMISSION = 5;\n'

    # Stock definitions for JS
    stocks_js = json.dumps(STOCKS, ensure_ascii=False)
    html += 'var STOCKS = ' + stocks_js + ';\n'

    # ---- Data access ----
    html += 'function getState(){ try{ var r=localStorage.getItem("investSimState_v13"); if(!r) return {}; return JSON.parse(r); }catch(e){ return {}; } }\n'
    html += 'function saveState(s){ try{ localStorage.setItem("investSimState_v13", JSON.stringify(s)); }catch(e){} }\n'
    html += 'function getBalances(){ return getState().cardBalances || {}; }\n'
    html += 'function getCredits(){ return getState().cardCredits || {}; }\n'
    html += 'function getAssets(){ var s=getState(); if(s.assets) return s.assets; if(s.this && s.this.assets) return s.this.assets; return null; }\n'
    html += 'function getRound(){ var s=getState(); return s.round || s.currentRound || 0; }\n'
    html += 'function getCash(){ var s=getState(); return s.cash || 0; }\n'

    # Broker accounts storage helpers
    html += 'function getBrokerData(){ var s=getState(); if(!s.brokerAccounts) s.brokerAccounts={}; if(!s.brokerAccounts[BROKER_KEY]) s.brokerAccounts[BROKER_KEY]={orders:[], openedAt: Date.now() }; return s.brokerAccounts[BROKER_KEY]; }\n'
    html += 'function saveBrokerData(d){ var s=getState(); if(!s.brokerAccounts) s.brokerAccounts={}; s.brokerAccounts[BROKER_KEY]=d; saveState(s); }\n'
    html += 'function addOrder(order){ var d=getBrokerData(); d.orders.unshift(order); if(d.orders.length>200)d.orders=d.orders.slice(0,200); saveBrokerData(d); }\n'
    html += 'function getOrders(){ return getBrokerData().orders||[]; }\n'

    # Master token validation (same as banks)
    html += 'function validateMasterToken(){\n'
    html += '  try{\n'
    html += '    var raw = localStorage.getItem("invest_sim_master");\n'
    html += '    if(!raw){ return { valid:false, reason:"母锁未激活" }; }\n'
    html += '    var token = JSON.parse(raw);\n'
    html += '    var age = Date.now() - (token.ts || 0);\n'
    html += '    if(age > 3600000){ return { valid:false, reason:"母锁令牌已过期" }; }\n'
    html += '    if(token.status !== "active"){ return { valid:false, reason:"母锁已被停用" }; }\n'
    html += '    return { valid:true, age:age };\n'
    html += '  }catch(e){ return { valid:false, reason:"母锁验证异常" }; }\n'
    html += '}\n'

    # Lock chain update
    html += 'function updateLockChain(){\n'
    html += '  var result = validateMasterToken();\n'
    html += '  var icon = document.getElementById("masterLockIcon");\n'
    html += '  var label = document.getElementById("masterLockLabel");\n'
    html += '  var status = document.getElementById("lockChainStatus");\n'
    html += '  if(result.valid){\n'
    html += '    icon.className = "lock-icon master"; icon.textContent = "🔓";\n'
    html += '    label.textContent = "已授权"; label.style.color="#00e676";\n'
    html += '    status.className = "lock-chain-status ok"; status.textContent = "母锁授权有效 · 交易数据已解锁";\n'
    html += '    masterTokenValid = true;\n'
    html += '  } else {\n'
    html += '    icon.className = "lock-icon offline"; icon.textContent = "🔒";\n'
    html += '    label.textContent = "离线"; label.style.color="#ff5252";\n'
    html += '    status.className = "lock-chain-status err"; status.textContent = result.reason+" — 请先打开投资模拟平台";\n'
    html += '    masterTokenValid = false;\n'
    html += '  }\n'
    html += '}\n'

    # Format functions
    html += 'function fmt(n){ if(!isFinite(n)||n==null)n=0; var f=n.toFixed(2),p=f.split("."),sg=n<0?"-":"",a=p[0].replace("-",""); return sg+"¥"+a.replace(/\\B(?=(\\d{3})+(?!\\d))/g,",")+"."+p[1]; }\n'
    html += 'function pct(v){ if(!isFinite(v))return "0.00%"; return (v>=0?"+":"")+v.toFixed(2)+"%"; }\n'
    html += 'function maskAcc(a){ return a.length > 6 ? a.slice(0,-6)+"******" : a; }\n'

    # Get stock info from state
    html += 'function getStockPrice(key){\n'
    html += '  var assets = getAssets();\n'
    html += '  if(!assets || !assets[key]) return 0;\n'
    html += '  return assets[key].price || 0;\n'
    html += '}\n'
    html += 'function getStockHolding(key){\n'
    html += '  var assets = getAssets();\n'
    html += '  if(!assets || !assets[key]) return { amount:0, avgCost:0 };\n'
    html += '  return { amount: assets[key].amount || 0, avgCost: assets[key].avgCost || 0 };\n'
    html += '}\n'
    html += 'function getPrevPrice(key){\n'
    html += '  var s = getState();\n'
    html += '  var prevPrices = s.prevPrices || {};\n'
    html += '  return prevPrices[key] != null ? prevPrices[key] : getStockPrice(key);\n'
    html += '}\n'

    # Update stock prices in the trade tab
    html += 'function updateStockPrices(){\n'
    html += '  for(var i=0;i<STOCKS.length;i++){\n'
    html += '    var sk = STOCKS[i].key;\n'
    html += '    var price = getStockPrice(sk);\n'
    html += '    var prev = getPrevPrice(sk);\n'
    html += '    var elP = document.getElementById("price_"+sk);\n'
    html += '    var elC = document.getElementById("change_"+sk);\n'
    html += '    if(elP) elP.textContent = fmt(price);\n'
    html += '    if(prev > 0 && price > 0){\n'
    html += '      var chg = ((price - prev) / prev * 100);\n'
    html += '      if(elC){ elC.textContent = pct(chg); elC.className = "stock-change "+(chg>=0?"up":"down"); }\n'
    html += '    } else {\n'
    html += '      if(elC){ elC.textContent = "--"; elC.className = "stock-change"; }\n'
    html += '    }\n'
    html += '  }\n'
    html += '}\n'

    # Select stock
    html += 'function selectStock(sk){\n'
    html += '  selectedStock = sk;\n'
    html += '  var items = document.querySelectorAll(".stock-item");\n'
    html += '  for(var i=0;i<items.length;i++) items[i].classList.toggle("selected", items[i].dataset.stock===sk);\n'
    html += '  var price = getStockPrice(sk);\n'
    html += '  var sinfo = null;\n'
    html += '  for(var i=0;i<STOCKS.length;i++){ if(STOCKS[i].key===sk){ sinfo=STOCKS[i]; break; } }\n'
    html += '  document.getElementById("selectedStockName").textContent = sinfo?sinfo.name:sk;\n'
    html += '  document.getElementById("selectedPrice").textContent = fmt(price);\n'
    html += '  updateCalculation();\n'
    html += '}\n'

    # Calculate trade costs
    html += 'function updateCalculation(){\n'
    html += '  if(!selectedStock){ document.getElementById("calcAmount").textContent="¥0.00"; document.getElementById("calcCommission").textContent="¥0.00"; document.getElementById("calcTotal").textContent="¥0.00"; return; }\n'
    html += '  var qty = parseInt(document.getElementById("tradeAmount").value)||0;\n'
    html += '  var price = getStockPrice(selectedStock);\n'
    html += '  var amt = qty * price;\n'
    html += '  var comm = Math.max(amt * BROKER_COMM, MIN_COMMISSION);\n'
    html += '  var total = amt + comm;\n'
    html += '  document.getElementById("calcAmount").textContent = fmt(amt);\n'
    html += '  document.getElementById("calcCommission").textContent = fmt(comm);\n'
    html += '  document.getElementById("calcTotal").textContent = fmt(total);\n'
    html += '}\n'

    # Execute trade
    html += 'function executeTrade(side){\n'
    html += '  var errEl = document.getElementById("tradeError");\n'
    html += '  var sucEl = document.getElementById("tradeSuccess");\n'
    html += '  errEl.style.display="none"; sucEl.style.display="none";\n'
    # Validate
    html += '  if(!validateMasterToken().valid){ showTradeErr("母锁令牌已失效！"); return; }\n'
    html += '  if(!selectedStock){ showTradeErr("请先选择一只股票"); return; }\n'
    html += '  var qty = parseInt(document.getElementById("tradeAmount").value)||0;\n'
    html += '  if(qty <= 0){ showTradeErr("交易数量必须大于0"); return; }\n'
    html += '  if(qty % 100 !== 0){ showTradeErr("交易数量必须为100的整数倍（手）"); return; }\n'
    html += '  var price = getStockPrice(selectedStock);\n'
    html += '  if(price <= 0){ showTradeErr("股票价格无效，请等待行情更新"); return; }\n'
    html += '  var s = getState();\n'
    html += '  var cash = s.cash || 0;\n'
    html += '  var assets = s.assets;\n'
    html += '  var amt = qty * price;\n'
    html += '  var comm = Math.max(amt * BROKER_COMM, MIN_COMMISSION);\n'

    # Buy logic
    html += '  if(side === "buy"){\n'
    html += '    var totalCost = amt + comm;\n'
    html += '    if(cash < totalCost){ showTradeErr("资金不足！需要 "+fmt(totalCost)+"，可用现金 "+fmt(cash)); return; }\n'
    html += '    cash -= totalCost;\n'
    html += '    s.cash = cash;\n'
    html += '    var asset = assets[selectedStock];\n'
    html += '    if(!asset.amount){ asset.amount = 0; asset.avgCost = 0; }\n'
    html += '    var oldTotal = asset.avgCost * asset.amount;\n'
    html += '    asset.amount += qty;\n'
    html += '    asset.avgCost = oldTotal / asset.amount + price * qty / asset.amount;\n'
    # Record order
    html += '    addOrder({id:Date.now(), side:"buy", stock:selectedStock, name:getStockName(selectedStock), quantity:qty, price:price, commission:comm, round:getRound(), time:Date.now(), account:currentAccount.account});\n'
    html += '    sucEl.textContent = "买入成功！"+qty+" 股 × "+fmt(price)+" = "+fmt(amt)+" （佣金 "+fmt(comm)+"）"; sucEl.style.display="block";\n'
    html += '  }\n'

    # Sell logic
    html += '  else if(side === "sell"){\n'
    html += '    var holding = assets[selectedStock];\n'
    html += '    var holdQty = holding.amount || 0;\n'
    html += '    if(holdQty < qty){ showTradeErr("持仓不足！持有 "+holdQty+" 股，欲卖 "+qty+" 股"); return; }\n'
    html += '    holding.amount -= qty;\n'
    html += '    cash += (amt - comm);\n'
    html += '    s.cash = cash;\n'
    # If sold all, reset avgCost
    html += '    if(holding.amount <= 0){ holding.amount=0; holding.avgCost=0; }\n'
    # Record order
    html += '    addOrder({id:Date.now(), side:"sell", stock:selectedStock, name:getStockName(selectedStock), quantity:qty, price:price, commission:comm, round:getRound(), time:Date.now(), account:currentAccount.account});\n'
    html += '    sucEl.textContent = "卖出成功！"+qty+" 股 × "+fmt(price)+" = "+fmt(amt)+" （佣金 "+fmt(comm)+"，净收入 "+fmt(amt-comm)+"）"; sucEl.style.display="block";\n'
    html += '  }\n'
    html += '  saveState(s);\n'
    html += '  showDashboard();\n'
    html += '  updateStockPrices();\n'
    html += '}\n'

    # Helper: get stock name by key
    html += 'function getStockName(key){ for(var i=0;i<STOCKS.length;i++){if(STOCKS[i].key===key)return STOCKS[i].name;} return key; }\n'

    # Error helper
    html += 'function showTradeErr(msg){ document.getElementById("tradeError").textContent=msg; document.getElementById("tradeError").style.display="block"; document.getElementById("tradeSuccess").style.display="none"; }\n'

    # DOMContentLoaded
    html += 'document.addEventListener("DOMContentLoaded", function(){\n'
    html += '  updateLockChain();\n'
    # Populate account selector
    html += '  var sel = document.getElementById("accountSelect");\n'
    html += '  for(var i=0;i<ACCOUNTS.length;i++){\n'
    html += '    var o = document.createElement("option"); o.value=i;\n'
    html += '    o.textContent = ACCOUNTS[i].holder + " · " + maskAcc(ACCOUNTS[i].account);\n'
    html += '    sel.appendChild(o);\n'
    html += '  }\n'
    # Login handler
    html += '  document.getElementById("loginBtn").addEventListener("click", function(){\n'
    html += '    var idx = parseInt(sel.value);\n'
    html += '    var pwd = document.getElementById("pwdInput").value.trim();\n'
    html += '    var err = document.getElementById("loginError");\n'
    html += '    if(isNaN(idx)){ err.textContent="请选择证券账户"; err.style.display="block"; return; }\n'
    html += '    var acc = ACCOUNTS[idx];\n'
    html += '    if(pwd !== acc.account.slice(-6)){ err.textContent="密码错误"; err.style.display="block"; return; }\n'
    html += '    if(!masterTokenValid){ err.textContent="母锁未授权！请先打开 invest-sim.html"; err.style.display="block"; return; }\n'
    html += '    err.style.display="none";\n'
    html += '    currentAccount = acc;\n'
    # Mark as opened in state
    html += '    var d = getBrokerData(); d.holder=acc.holder; d.account=acc.account; d.openedAt=d.openedAt||Date.now(); saveBrokerData(d);\n'
    html += '    showDashboard();\n'
    html += '  });\n'
    html += '  document.getElementById("pwdInput").addEventListener("keypress", function(e){ if(e.key==="Enter") document.getElementById("loginBtn").click(); });\n'
    # Back button
    html += '  document.getElementById("backBtn").addEventListener("click", function(){\n'
    html += '    document.getElementById("dashboard").style.display="none";\n'
    html += '    document.getElementById("loginCard").style.display="block";\n'
    html += '    document.getElementById("pwdInput").value="";\n'
    html += '    currentAccount=null; selectedStock=null;\n'
    html += '    switchTab("overview");\n'
    html += '    updateLockChain();\n'
    html += '  });\n'
    # Tab buttons
    html += '  document.querySelectorAll(".tab-btn").forEach(function(btn){\n'
    html += '    btn.addEventListener("click", function(){ switchTab(this.dataset.tab); });\n'
    html += '  });\n'
    # Trade amount input -> recalculate
    html += '  document.getElementById("tradeAmount").addEventListener("input", updateCalculation);\n'
    html += '});\n'

    # Switch tab function
    html += 'function switchTab(name){\n'
    html += '  document.querySelectorAll(".tab-btn").forEach(function(b){ b.classList.toggle("active", b.dataset.tab===name); });\n'
    html += '  document.getElementById("tabOverview").style.display = name==="overview"?"block":"none";\n'
    html += '  document.getElementById("tabTrade").style.display = name==="trade"?"block":"none";\n'
    html += '  document.getElementById("tabPositions").style.display = name==="positions"?"block":"none";\n'
    html += '  document.getElementById("tabOrders").style.display = name==="orders"?"block":"none";\n'
    html += '  if(name==="overview"){ showDashboard(); }\n'
    html += '  if(name==="trade"){ updateStockPrices(); updateCalculation(); }\n'
    html += '  if(name==="positions"){ renderPositions(); }\n'
    html += '  if(name==="orders"){ renderOrders(); }\n'
    html += '}\n'

    # Show dashboard
    html += 'function showDashboard(){\n'
    html += '  var s = getState();\n'
    html += '  var cash = s.cash || 0;\n'
    html += '  var assets = s.assets;\n'
    html += '  var totalVal = 0;\n'
    html += '  var todayPL = 0;\n'
    html += '  if(assets){\n'
    html += '    for(var k in assets){\n'
    html += '      if(assets[k].amount && assets[k].price){ totalVal += assets[k].amount * assets[k].price; }\n'
    html += '    }\n'
    html += '  }\n'
    html += '  document.getElementById("accHolder").textContent = currentAccount?currentAccount.holder:"--";\n'
    html += '  document.getElementById("accAccount").textContent = currentAccount?maskAcc(currentAccount.account):"--";\n'
    html += '  document.getElementById("accBalance").textContent = fmt(cash);\n'
    html += '  document.getElementById("totalValue").textContent = fmt(totalVal);\n'
    html += '  document.getElementById("todayPnL").textContent = fmt(todayPL);\n'
    html += '  var mResult = validateMasterToken();\n'
    html += '  var mSt = document.getElementById("masterStatusDash");\n'
    html += '  mSt.innerHTML = mResult.valid?\'<span class="credit-badge high">🔓 已授权</span>\':\'<span class="credit-badge low">🔒 未授权</span>\';\n'
    html += '  document.getElementById("loginCard").style.display="none";\n'
    html += '  document.getElementById("dashboard").style.display="block";\n'
    html += '}\n'

    # Render positions table
    html += 'function renderPositions(){\n'
    html += '  var assets = getAssets();\n'
    html += '  var tbody = document.getElementById("posBody");\n'
    html += '  if(!assets){ tbody.innerHTML="<tr><td colspan=\\"7\\" style=\\"text-align:center;color:#555;padding:20px;\\">无法加载资产数据</td></tr>"; return; }\n'
    html += '  var h = "";\n'
    html += '  var hasPos = false;\n'
    html += '  for(var i=0;i<STOCKS.length;i++){\n'
    html += '    var sk = STOCKS[i].key;\n'
    html += '    var a = assets[sk];\n'
    html += '    if(!a || !a.amount || a.amount <= 0) continue;\n'
    html += '    hasPos = true;\n'
    html += '    var price = a.price || 0;\n'
    html += '    var cost = a.avgCost || 0;\n'
    html += '    var mktVal = a.amount * price;\n'
    html += '    var pnl = a.amount * (price - cost);\n'
    html += '    var retPct = cost > 0 ? ((price - cost)/cost*100) : 0;\n'
    html += '    h += "<tr>";\n'
    html += '    h += "<td>"+getStockName(sk)+"</td>";\n'
    html += '    h += "<td>"+a.amount+"</td>";\n'
    html += '    h += "<td>"+fmt(cost)+"</td>";\n'
    html += '    h += "<td>"+fmt(price)+"</td>";\n'
    html += '    h += "<td>"+fmt(mktVal)+"</td>";\n'
    html += '    h += \'<td class="pos-profit "\'+(pnl>=0?"positive":"negative")+"\\">"+fmt(pnl)+"</td>";\n'
    html += '    h += \'<td class="pos-profit "\'+(retPct>=0?"positive":"negative")+"\\">"+pct(retPct)+"</td>";\n'
    html += '    h += "</tr>";\n'
    html += '  }\n'
    html += '  if(!hasPos){ tbody.innerHTML="<tr><td colspan=\\"7\\" style=\\"text-align:center;color:#555;padding:20px;\\">暂无持仓</td></tr>"; return; }\n'
    html += '  tbody.innerHTML = h;\n'
    html += '}\n'

    # Render orders
    html += 'function renderOrders(){\n'
    html += '  var orders = getOrders();\n'
    html += '  var container = document.getElementById("orderList");\n'
    html += '  if(!orders || orders.length===0){ container.innerHTML=\'<div class="order-empty">暂无委托记录</div>\'; return; }\n'
    html += '  var h = "";\n'
    html += '  for(var i=0;i<Math.min(orders.length,50);i++){\n'
    html += '    var o = orders[i];\n'
    html += '    var isBuy = o.side === "buy";\n'
    html += '    var d = new Date(o.time);\n'
    html += '    var tstr = d.getFullYear()+"/"+("0"+(d.getMonth()+1)).slice(-2)+"/"+("0"+d.getDate()).slice(-2)+" "+("0"+d.getHours()).slice(-2)+":"+("0"+d.getMinutes()).slice(-2);\n'
    html += '    h += \'<div class="order-item">\';\n'
    html += '    h += \'<div class="order-header"><span class="order-type "\'+o.side+\'">\'+(isBuy?"买入":"卖出")+\'</span><span class="order-amount">\'+fmt(o.quantity*o.price)+\'</span></div>\';\n'
    html += '    h += \'<div class="order-detail">\'+o.name+\' · \'+o.quantity+\'股 × \'+fmt(o.price)+\' · 佣金 \'+fmt(o.commission)+\' · 第\'+o.round+\'回合 · \'+tstr+\'</div>\';\n'
    html += '    h += "</div>";\n'
    html += '  }\n'
    html += '  container.innerHTML = h;\n'
    html += '}\n'
    html += '</script>\n'
    html += '</body>\n</html>'
    return html


# Generate all broker pages
for key, broker in brokers.items():
    html = generate_broker_page(key, broker)
    path = 'C:/Users/Ye201/WorkBuddy/2026-05-23-task-2/broker-' + key + '.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Created: broker-' + key + '.html (' + broker['name'] + ')')

print('Done!')
