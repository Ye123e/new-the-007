# -*- coding: utf-8 -*-
"""
gen_insurance.py - 保险公司页面生成器
生成3个保险公司: 人保(PICC)、平安(PingAn)、友邦(AIA)
每个平台独立HTML文件，通过 investSimState_v13 与主模拟器同步
"""

import json

# Insurance company definitions
companies = {
    'picc': {
        'name': '中国人民保险',
        'en': 'PICC',
        'short_name': '人保',
        'color': '#d32f2f',
        'emoji': '🛡️',
        'region': 'mainland',
        'description': '中央管理的国有保险巨头，覆盖财险、寿险、健康险全品类',
        'products': [
            {'id': 'health_basic', 'name': '基础医疗险', 'type': 'health', 'premium_range': [500, 2000], 'coverage_range': [50000, 200000], 'term': 12, 'desc': '住院/手术费用报销'},
            {'id': 'property_home', 'name': '家庭财产险', 'type': 'property', 'premium_range': [300, 1500], 'coverage_range': [100000, 800000], 'term': 12, 'desc': '房屋/家具/电器保障'},
            {'id': 'accident_yearly', 'name': '综合意外险', 'type': 'accident', 'premium_range': [100, 500], 'coverage_range': [200000, 1000000], 'term': 12, 'desc': '意外身故/伤残/医疗'},
        ]
    },
    'pingan': {
        'name': '中国平安保险',
        'en': 'Ping An',
        'short_name': '平安',
        'color': '#ff9800',
        'emoji': '🔶',
        'region': 'mainland',
        'description': '综合金融服务集团，保险+科技双驱动，产品线丰富',
        'products': [
            {'id': 'life_term', 'name': '定期寿险', 'type': 'life', 'premium_range': [800, 3000], 'coverage_range': [500000, 3000000], 'term': 24, 'desc': '身故/全残赔付保额'},
            {'id': 'health_cancer', 'name': '重疾险', 'type': 'health', 'premium_range': [1000, 5000], 'coverage_range': [100000, 600000], 'term': 36, 'desc': '120种重大疾病一次性赔付'},
            {'id': 'car_insurance', 'name': '车辆综合险', 'type': 'vehicle', 'premium_range': [2000, 8000], 'coverage_range': [50000, 300000], 'term': 12, 'desc': '车损/三者/盗抢险全包'},
        ]
    },
    'aia': {
        'name': '友邦保险',
        'en': 'AIA',
        'short_name': '友邦',
        'color': '#1976d2',
        'emoji': '💙',
        'region': 'hongkong',
        'description': '亚太区领先人寿保险公司，高端医疗保障专家',
        'products': [
            {'id': 'health_premium', 'name': '全球医疗险', 'type': 'health', 'premium_range': [3000, 12000], 'coverage_range': [200000, 2000000], 'term': 12, 'desc': '全球范围内住院/门诊/牙科'},
            {'id': 'life_whole', 'name': '终身寿险', 'type': 'life', 'premium_range': [5000, 20000], 'coverage_range': [1000000, 5000000], 'term': 999, 'desc': '终身保障+现金价值积累'},
            {'id': 'investment_link', 'name': '投资连结险', 'type': 'investment', 'premium_range': [10000, 100000], 'coverage_range': [0, 0], 'term': 60, 'desc': '保险+投资双重功能，账户价值浮动'},
        ]
    }
}

# Claim event templates for random generation
CLAIM_EVENTS = [
    {'name': '感冒发烧就医', 'type': 'health', 'cost_range': [200, 1500], 'prob_base': 0.15},
    {'name': '急性肠胃炎', 'type': 'health', 'cost_range': [500, 3000], 'prob_base': 0.05},
    {'name': '意外摔伤', 'type': 'accident', 'cost_range': [1000, 8000], 'prob_base': 0.03},
    {'name': '交通事故', 'type': 'accident', 'cost_range': [5000, 50000], 'prob_base': 0.01},
    {'name': '家中水管爆裂', 'type': 'property', 'cost_range': [2000, 15000], 'prob_base': 0.04},
    {'name': '家电损坏', 'type': 'property', 'cost_range': [500, 5000], 'prob_base': 0.06},
    {'name': '车辆碰撞维修', 'type': 'vehicle', 'cost_range': [2000, 20000], 'prob_base': 0.08},
    {'name': '车辆被盗', 'type': 'vehicle', 'cost_range': [30000, 150000], 'prob_base': 0.005},
    {'name': '重大疾病确诊', 'type': 'health', 'cost_range': [30000, 150000], 'prob_base': 0.02},
    {'name': '自然灾害损失', 'type': 'property', 'cost_range': [10000, 100000], 'prob_base': 0.01},
]


def generate_insurance_page(key, comp):
    color = comp['color']
    name = comp['name']
    en = comp['en']
    short_name = comp['short_name']
    emoji = comp['emoji']
    desc = comp['description']
    products_json = json.dumps(comp['products'], ensure_ascii=False)
    claims_json = json.dumps(CLAIM_EVENTS, ensure_ascii=False)

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
    html += '<title>' + name + ' - 保险服务</title>\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'

    # CSS
    html += '<style>\n'
    html += '* { margin:0; padding:0; box-sizing:border-box; }\n'
    html += 'body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#0a0e17; color:#e0e0e0; min-height:100vh; }\n'
    html += '.header { background:linear-gradient(135deg,' + color + ',' + color + '99); padding:20px 24px; display:flex;align-items:center;gap:14px; }\n'
    html += '.header-icon { width:48px;height:48px;background:rgba(255,255,255,0.2);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px; }\n'
    html += '.header-info h1 { font-size:22px;color:#fff; }\n'
    html += '.header-info p { font-size:12px;color:rgba(255,255,255,0.75);margin-top:2px; }\n'
    html += '.container { max-width:900px;margin:0 auto;padding:16px; }\n'

    # Login box (with master-slave lock)
    html += '.login-box { background:#131823;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:28px;margin-top:20px;text-align:center; }\n'
    html += '.login-box h2 { font-size:18px;margin-bottom:12px;color:' + color + '; }\n'
    html += '.login-box p { font-size:13px;color:#888;margin-bottom:18px;line-height:1.6; }\n'
    html += '.login-btn { display:inline-block;padding:12px 40px;background:' + color + ';color:#fff;border:none;border-radius:8px;font-size:15px;cursor:pointer;font-weight:600;transition:transform 0.2s; }\n'
    html += '.login-btn:hover { transform:scale(1.04); }\n'
    html += '.lock-chain { display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:16px;font-size:11px;color:#666; }\n'
    html += '.lock-dot { width:8px;height:8px;border-radius:50%;background:#444; }\n'
    html += '.lock-dot.active { background:#4caf50;box-shadow:0 0 6px #4caf50; }\n'
    html += '.lock-line { width:30px;height:2px;background:#333; }\n'
    html += '.lock-line.active { background:#4caf50; }\n'

    # Main app (hidden by default)
    html += '.main-app { display:none; }\n'

    # Nav tabs
    html += '.nav-tabs { display:flex;gap:4px;margin-bottom:16px;flex-wrap:wrap; }\n'
    html += '.nav-tab { padding:8px 16px;border-radius:8px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#888;transition:all 0.2s;flex:0 0 auto; }\n'
    html += '.nav-tab.active { background:' + color + '22;color:' + color + ';border-color:' + color + '44;font-weight:600; }\n'
    html += '.tab-panel { display:none; }\n'
    html += '.tab-panel.active { display:block; }\n'

    # Stats row
    html += '.stat-row { display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px; }\n'
    html += '.stat-card { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;text-align:center; }\n'
    html += '.stat-value { font-size:20px;font-weight:700;color:' + color + '; }\n'
    html += '.stat-label { font-size:11px;color:#777;margin-top:2px; }\n'

    # Product cards
    html += '.prod-list { display:flex;flex-direction:column;gap:12px; }\n'
    html += '.prod-card { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:18px;transition:border-color 0.2s; }\n'
    html += '.prod-card:hover { border-color:' + color + '33; }\n'
    html += '.prod-header { display:flex;justify-content:space-between;align-items:start;margin-bottom:10px; }\n'
    html += '.prod-name { font-size:16px;font-weight:600; }\n'
    html += '.prod-type-badge { font-size:10px;padding:3px 10px;border-radius:20px;font-weight:600;background:' + color + '18;color:' + color + '; }\n'
    html += '.prod-desc { font-size:12px;color:#999;margin-bottom:12px;line-height:1.5; }\n'
    html += '.prod-specs { display:flex;gap:16px;flex-wrap:wrap;margin-bottom:14px; }\n'
    html += '.prod-spec { display:flex;flex-direction:column;gap:2px; }\n'
    html += '.spec-label { font-size:10px;color:#666; }\n'
    html += '.spec-value { font-size:13px;font-weight:600;color:#ddd; }\n'
    # Buy form inside product card
    html += '.buy-bar { display:flex;align-items:center;gap:8px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.05); }\n'
    html += '.premium-input { width:130px;padding:8px 10px;background:#1a1f2e;border:1px solid rgba(255,255,255,0.1);border-radius:6px;color:#fff;font-size:14px;outline:none; }\n'
    html += '.premium-input:focus { border-color:' + color + '; }\n'
    html += '.btn-buy { padding:8px 22px;background:' + color + ';color:#fff;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-weight:600; }\n'
    html += '.btn-buy:hover { opacity:0.85; }\n'
    html += '.btn-buy:disabled { opacity:0.4;cursor:not-allowed; }\n'

    # My policies table
    html += '.policy-table { width:100%;border-collapse:collapse; }\n'
    html += '.policy-table th { text-align:left;font-size:11px;color:#777;padding:8px 6px;border-bottom:1px solid rgba(255,255,255,0.06);font-weight:500; }\n'
    html += '.policy-table td { padding:11px 6px;border-bottom:1px solid rgba(255,255,255,0.03);font-size:12px;vertical-align:middle; }\n'
    html += '.status-active { color:#4caf50;font-weight:600;font-size:11px; }\n'
    html += '.status-expired { color:#888;font-size:11px; }\n'
    html += '.status-claimed { color:#ff9800;font-size:11px; }\n'

    # Claims panel
    html += '.claim-item { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;margin-bottom:10px; }\n'
    html += '.claim-header { display:flex;justify-content:space-between;align-items:center;margin-bottom:6px; }\n'
    html += '.claim-event { font-weight:600;font-size:14px; }\n'
    html += '.claim-amount { font-size:16px;font-weight:700;color:#ff5252; }  # red\n'
    html += '.claim-detail { font-size:11px;color:#888; }\n'
    html += '.btn-claim { padding:6px 16px;background:#4caf50;color:#fff;border:none;border-radius:5px;font-size:12px;cursor:pointer;margin-top:8px;font-weight:600; }\n'
    html += '.btn-claim:disabled { opacity:0.4;cursor:not-allowed; }\n'
    html += '.btn-claim:hover {notdisabled} { background:#43a047; }\n'

    # Account summary
    html += '.acct-summary { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:18px;margin-bottom:14px; }\n'
    html += '.acct-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px; }\n'
    html += '.acct-row:last-child { border-bottom:none; }\n'
    html += '.acct-label { color:#888; }\n'
    html += '.acct-value { font-weight:600; }\n'

    # Notice
    html += '.notice { padding:10px 14px;background:rgba(33,150,243,0.06);border:1px solid rgba(33,150,243,0.15);border-radius:8px;font-size:11px;color:#ccc;line-height:1.6;margin-top:12px; }\n'
    html += '</style>\n</head>\n<body>\n'

    # Header
    html += '<div class="header">\n'
    html += '  <div class="header-icon">' + emoji + '</div>\n'
    html += '  <div class="header-info"><h1>' + name + '</h1><p>' + en + ' · ' + desc + '</p></div>\n'
    html += '</div>\n'

    html += '<div class="container">\n'

    # Login screen
    html += '<div id="loginScreen" class="login-box">\n'
    html += '  <div class="lock-chain" id="lockChain"></div>\n'
    html += '  <h2>🛡️ 登录 ' + short_name + '</h2>\n'
    html += '  <p>安全登录以访问您的保险账户<br>需要母锁令牌验证</p>\n'
    html += '  <button class="login-btn" onclick="doLogin()">🔑 验证并登录</button>\n'
    html += '  <p id="loginError" style="color:#f44336;margin-top:10px;display:none;"></p>\n'
    html += '</div>\n'

    # Main app
    html += '<div id="mainApp" class="main-app">\n'
    html += '  <div class="nav-tabs">\n'
    html += '    <div class="nav-tab active" data-iTab="overview">📊 概览</div>\n'
    html += '    <div class="nav-tab" data-iTab="products">📦 投保</div>\n'
    html += '    <div class="nav-tab" data-iTab="policies">📋 我的保单</div>\n'
    html += '    <div class="nav-tab" data-iTab="claims">🏥 理赔</div>\n'
    html += '  </div>\n'

    # Overview panel
    html += '  <div id="iTab-overview" class="tab-panel active">\n'
    html += '    <div id="acctSummary" class="acct-summary"></div>\n'
    html += '    <div class="notice">ℹ️ 保险是一种风险管理工具。保费支出会从模拟器现金中扣除，理赔金会加回现金。不同产品的赔付条件和比例不同。</div>\n'
    html += '  </div>\n'

    # Products panel
    html += '  <div id="iTab-products" class="tab-panel">\n'
    html += '    <div id="productList" class="prod-list"></div>\n'
    html += '  </div>\n'

    # Policies panel
    html += '  <div id="iTab-policies" class="tab-panel">\n'
    html += '    <div style="overflow-x:auto;"><table class="policy-table"><thead><tr><th>产品名称</th><th>类型</th><th>保额</th><th>年保费</th><th>剩余期数</th><th>状态</th></tr></thead><tbody id="policyBody"></tbody></table></div>\n'
    html += '  </div>\n'

    # Claims panel
    html += '  <div id="iTab-claims" class="tab-panel">\n'
    html += '    <div id="claimsList"></div>\n'
    html += '  </div>\n'

    html += '</div>\n'  # end mainApp
    html += '</div>\n'  # end container

    # JavaScript
    html += '<script>\n'
    html += "const INS_KEY = '" + key + "';\n"
    html += "const INS_NAME = '" + name + "';\n"
    html += "const INS_SHORT = '" + short_name + "';\n"
    html += "const INS_COLOR = '" + color + "';\n"
    html += 'var STORAGE_KEY = "investSimState_v13";\n'
    html += 'var isLoggedIn = false;\n'
    html += 'var PRODUCTS = ' + products_json + ';\n'
    html += 'var CLAIM_EVENTS = ' + claims_json + ';\n'

    # Utility functions
    html += 'function fmt(n) {\n'
    html += '  if (n == null || isNaN(n) || !isFinite(n)) return "0.00";\n'
    html += '  return n.toLocaleString("zh-CN", {minimumFractionDigits:2, maximumFractionDigits:2});\n'
    html += '}\n'
    html += 'function safeFixed(n, d) {\n'
    html += '  if (n == null || isNaN(n) || !isFinite(n)) return "0." + "0".repeat(d||2);\n'
    html += '  return Number(n).toFixed(d || 2);\n'
    html += '}\n\n'

    # Master-slave lock check
    html += 'function checkMasterLock() {\n'
    html += '  try {\n'
    html += '    var raw = localStorage.getItem("invest_sim_master");\n'
    html += '    if (!raw) return { ok:false, msg:"未找到母锁令牌，请先打开投资模拟器" };\n'
    html += '    var token = JSON.parse(raw);\n'
    html += '    if (Date.now() - token.time > 3600000) return { ok:false, msg:"母锁令牌已过期(>1小时)，请重新打开模拟器" };\n'
    html += '    return { ok:true, token:token };\n'
    html += '  } catch(e) { return { ok:false, msg:"令牌解析失败" }; }\n'
    html += '}\n\n'

    # Render lock chain
    html += 'function renderLockChain() {\n'
    html += '  var c = document.getElementById("lockChain");\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  c.innerHTML = \'<span class="lock-dot \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-line \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-dot \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-line \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span style="font-size:10px;color:\'+(lock.ok?"#4caf50":"#666")+\'">\'+(lock.ok?"母锁→数据 已连接":"母锁→数据 断开")+\'</span>\';\n'
    html += '}\n\n'

    # Load/Save state
    html += 'function loadState() {\n'
    html += '  try { var r = localStorage.getItem(STORAGE_KEY); return r ? JSON.parse(r) : null; } catch(e) { return null; }\n'
    html += '}\n'
    html += 'function saveState(s) {\n'
    html += '  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch(e) {}\n'
    html += '}\n\n'

    # Get insurance data
    html += 'function getInsData(state) {\n'
    html += '  if (!state.insurancePolicies) state.insurancePolicies = {};\n'
    html += '  if (!state.insurancePolicies[INS_KEY]) {\n'
    html += '    state.insurancePolicies[INS_KEY] = {\n'
    html += '      totalPremium: 0,\n'
    html += '      totalClaimed: 0,\n'
    html += '      policies: [],\n'
    html += '      claims: []\n'
    html += '    };\n'
    html += '  }\n'
    html += '  return state.insurancePolicies[INS_KEY];\n'
    html += '}\n\n'

    # Login function
    html += 'function doLogin() {\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) {\n'
    html += '    document.getElementById("loginError").textContent = lock.msg;\n'
    html += '    document.getElementById("loginError").style.display = "block";\n'
    html += '    renderLockChain(); return;\n'
    html += '  }\n'
    html += '  isLoggedIn = true;\n'
    html += '  document.getElementById("loginScreen").style.display = "none";\n'
    html += '  document.getElementById("mainApp").style.display = "block";\n'
    html += '  renderOverview();\n'
    html += '  renderProducts();\n'
    html += '  renderPolicies();\n'
    html += '  renderClaims();\n'
    html += '}\n\n'

    # Tab switching
    html += 'document.addEventListener("DOMContentLoaded", function() {\n'
    html += '  renderLockChain();\n'
    html += '  document.querySelectorAll(".nav-tab").forEach(function(tab) {\n'
    html += '    tab.addEventListener("click", function() {\n'
    html += '      document.querySelectorAll(".nav-tab").forEach(function(t){t.classList.remove("active")});\n'
    html += '      this.classList.add("active");\n'
    html += '      document.querySelectorAll(".tab-panel").forEach(function(p){p.classList.remove("active")});\n'
    html += '      var target = "iTab-" + this.getAttribute("data-iTab");\n'
    html += '      var panel = document.getElementById(target);\n'
    html += '      if (panel) panel.classList.add("active");\n'
    html += '      if (target === "iTab-overview") renderOverview();\n'
    html += '      if (target === "iTab-products") renderProducts();\n'
    html += '      if (target === "iTab-policies") renderPolicies();\n'
    html += '      if (target === "iTab-claims") renderClaims();\n'
    html += '    });\n'
    html += '  });\n'
    html += '});\n\n'

    # Render overview
    html += 'function renderOverview() {\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  var d = getInsData(s);\n'
    html += '  var cash = s.cash || 0;\n'
    html += '  var activePol = (d.policies||[]).filter(function(p){return p.status === "active";}).length;\n'
    html += '  var c = document.getElementById("acctSummary");\n'
    html += '  c.innerHTML = \'<div class="acct-row"><span class="acct-label">🏢 公司</span><span class="acct-value">\' + INS_NAME + \'</span></div>\'+\n'
    html += '    \'<div class="acct-row"><span class="acct-label">💰 现金余额</span><span class="acct-value">¥\' + fmt(cash) + \'</span></div>\'+\n'
    html += '    \'<div class="acct-row"><span class="acct-label">📋 有效保单</span><span class="acct-value">\' + activePol + \' 份</span></div>\'+\n'
    html += '    \'<div class="acct-row"><span class="acct-label">💸 累计保费</span><span class="acct-value" style="color:#f44336;">-¥\' + fmt(d.totalPremium) + \'</span></div>\'+\n'
    html += '    \'<div class="acct-row"><span class="acct-label">✅ 累计理赔</span><span class="acct-value" style="color:#4caf50;">+¥\' + fmt(d.totalClaimed) + \'</span></div>\'+\n'
    html += '    \'<div class="acct-row"><span class="acct-label">📊 净收支</span><span class="acct-value" style="color:\' + ((d.totalClaimed - d.totalPremium) >= 0 ? "#ff5252" : "#00e676") + \';">\' + ((d.totalClaimed - d.totalPremium) >= 0 ? "+" : "") + \'¥\' + fmt(d.totalClaimed - d.totalPremium) + \'</span></div>\';\n'
    html += '}\n\n'

    # Render products list
    html += 'function renderProducts() {\n'
    html += '  var c = document.getElementById("productList"); if (!c) return;\n'
    html += '  var s = loadState(); var cash = s ? (s.cash || 0) : 0;\n'
    html += '  var h = \'\';\n'
    html += '  PRODUCTS.forEach(function(prod, i) {\n'
    html += '    var minPrem = prod.premium_range[0];\n'
    html += '    var maxCov = prod.coverage_range[1];\n'
    html += '    var typeNames = {"health":"医疗","property":"财产","accident":"意外","life":"寿险","vehicle":"车险","investment":"投资"};\n'
    html += '    var tName = typeNames[prod.type] || prod.type;\n'
    html += '    h += \'<div class="prod-card">\';\n'
    html += '    h += \'<div class="prod-header"><div><div class="prod-name">\' + prod.name + \'</div>\';\n'
    html += '    h += \'<span class="prod-type-badge">\' + tName + \'险</span></div></div>\';\n'
    html += '    h += \'<div class="prod-desc">\' + prod.desc + \'</div>\';\n'
    html += '    h += \'<div class="prod-specs">\';\n'
    html += '    h += \'<div class="prod-spec"><span class="spec-label">保障期限</span><span class="spec-value">\' + prod.term + \'个月</span></div>\';\n'
    html += '    h += \'<div class="prod-spec"><span class="spec-label">保额范围</span><span class="spec-value">¥\' + fmt(prod.coverage_range[0]) + \' - ¥\' + fmt(maxCov) + \'</span></div>\';\n'
    html += '    h += \'<div class="prod-spec"><span class="spec-label">年保费范围</span><span class="spec-value">¥\' + minPrem + \' 起</span></div>\';\n'
    html += '    h += \'</div>\';\n'
    html += '    h += \'<div class="buy-bar">\';\n'
    html += '    h += \'<input type="number" class="premium-input" id="prem_\' + i + \'" placeholder="输入保额" min="\' + prod.coverage_range[0] + \'" max="\' + maxCov + \'" step="1000">\';\n'
    html += '    h += \'<button class="btn-buy" onclick="doBuyPolicy(\' + i + \')" \' + (cash < minPrem ? "disabled" : "") + \'>立即投保</button>\';\n'
    html += '    h += \'</div></div>\';\n'
    html += '  });\n'
    html += '  c.innerHTML = h;\n'
    html += '}\n\n'

    # Buy policy function
    html += 'function doBuyPolicy(idx) {\n'
    html += '  // Lock check\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) { alert("母锁验证失败: " + lock.msg); isLoggedIn = false; location.reload(); return; }\n\n'
    html += '  var prod = PRODUCTS[idx]; if (!prod) return;\n'
    html += '  var input = document.getElementById("prem_" + idx); if (!input) return;\n'
    html += '  var coverage = parseFloat(input.value);\n'
    html += '  if (!coverage || coverage < prod.coverage_range[0]) { alert("最低保额 ¥" + fmt(prod.coverage_range[0])); return; }\n'
    html += '  if (coverage > prod.coverage_range[1]) { alert("最高保额 ¥" + fmt(prod.coverage_range[1])); return; }\n\n'
    html += '  // Calculate premium (linear interpolation)\n'
    html += '  var ratio = (coverage - prod.coverage_range[0]) / (prod.coverage_range[1] - prod.coverage_range[0]);\n'
    html += '  var premium = prod.premium_range[0] + ratio * (prod.premium_range[1] - prod.premium_range[0]);\n'
    html += '  premium = Math.round(premium * 100) / 100;\n\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  if ((s.cash || 0) < premium) { alert("现金不足！需 ¥" + fmt(premium)); return; }\n\n'
    html += '  s.cash -= premium;\n'
    html += '  var d = getInsData(s);\n'
    html += '  d.totalPremium = (d.totalPremium || 0) + premium;\n\n'
    html += '  var policy = {\n'
    html += '    id: "pol_" + Date.now(),\n'
    html += '    productId: prod.id,\n'
    html += '    name: prod.name,\n'
    html += '    type: prod.type,\n'
    html += '    coverage: coverage,\n'
    html += '    annualPremium: premium,\n'
    html += '    termMonths: prod.term,\n'
    html += '    remainingMonths: prod.term,\n'
    html += '    purchasedAt: Date.now(),\n'
    html += '    round: s.round || 0,\n'
    html += '    status: "active"\n'
    html += '  };\n'
    html += '  d.policies.push(policy);\n'
    html += '  saveState(s);\n'
    html += '  alert("✅ 投保成功！\\n产品: " + prod.name + "\\n保额: ¥" + fmt(coverage) + "\\n年保费: ¥" + fmt(premium) + "\\n期限: " + prod.term + "个月");\n'
    html += '  renderOverview();\n'
    html += '  renderProducts();\n'
    html += '  renderPolicies();\n'
    html += '}\n\n'

    # Render my policies table
    html += 'function renderPolicies() {\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  var d = getInsData(s);\n'
    html += '  var tbody = document.getElementById("policyBody"); if (!tbody) return;\n'
    html += '  if (!d.policies || d.policies.length === 0) {\n'
    html += '    tbody.innerHTML = \'<tr><td colspan="6" style="text-align:center;color:#555;padding:20px;">暂无保单</td></tr>\'; return;\n'
    html += '  }\n'
    html += '  var typeNames = {"health":"医疗","property":"财产","accident":"意外","life":"寿险","vehicle":"车险","investment":"投资"};\n'
    html += '  var h = \'\';\n'
    html += '  d.policies.forEach(function(p) {\n'
    html += '    var stClass = p.status === "active" ? "status-active" : (p.status === "expired" ? "status-expired" : "status-claimed");\n'
    html += '    var stText = p.status === "active" ? "生效中" : (p.status === "expired" ? "已过期" : "已理赔");\n'
    html += '    h += \'<tr><td>\' + p.name + \'</td><td>\' + (typeNames[p.type]||p.type) + \'</td><td>¥\' + fmt(p.coverage) + \'</td><td>¥\' + fmt(p.annualPremium) + \'</td><td>\' + (p.remainingMonths||0) + \'月</td><td class="\'+stClass+\'">\' + stText + \'</td></tr>\';\n'
    html += '  });\n'
    html += '  tbody.innerHTML = h;\n'
    html += '}\n\n'

    # Render claims (random events that can be claimed)
    html += 'function renderClaims() {\n'
    html += '  var c = document.getElementById("claimsList"); if (!c) return;\n'
    html += '  var s = loadState(); if (!s) { c.innerHTML = "<div style=\\"text-align:center;color:#555;padding:30px;\\">无数据</div>"; return; }\n'
    html += '  var d = getInsData(s);\n'
    html += '  // Generate 1-3 potential claim events based on active policies\n'
    html += '  var activePol = (d.policies||[]).filter(function(p){return p.status === "active";});\n'
    html += '  if (activePol.length === 0) {\n'
    html += '    c.innerHTML = \'<div class="notice">没有有效的保单。先去投保吧！</div>\'; return;\n'
    html += '  }\n'
    html += '  // Show existing claims first\n'
    html += '  var existingClaims = (d.claims||[]).filter(function(cl){return cl.status !== "paid";});\n'
    html += '  var h = \'\';\n'
    html += '  if (existingClaims.length > 0) {\n'
    html += '    h += \'<div style="margin-bottom:14px;"><b style="font-size:13px;">待处理理赔</b></div>\';\n'
    html += '    existingClaims.forEach(function(cl) {\n'
    html += '      h += \'<div class="claim-item">\';\n'
    html += '      h += \'<div class="claim-header"><span class="claim-event">\' + cl.eventName + \'</span><span class="claim-amount">¥\' + fmt(cl.claimAmount) + \'</span></div>\';\n'
    html += '      h += \'<div class="claim-detail">保单: \' + cl.policyName + \' | 发生回合: \' + (cl.round||"?") + \' | 状态: \' + (cl.status==="pending"?"待申请":cl.status) + \'</div>\';\n'
    html += '      if (cl.status === "pending") {\n'
    html += '        h += \'<button class="btn-claim" onclick="submitClaim(\\\'\'+cl.id+\'\\\')">申请理赔</button>\';\n'
    html += '      } else if (cl.status === "approved") {\n'
    html += '        h += \'<button class="btn-claim" onclick="receiveClaim(\\\'\'+cl.id+\'\\\')">领取赔款</button>\';\n'
    html += '      }\n'
    html += '      h += \'</div>\';\n'
    html += '    });\n'
    html += '  }\n'
    html += '  // Generate new potential events\n'
    html += '  h += \'<div style="margin-top:16px;"><b style="font-size:13px;">可能发生的风险事件（随机生成）</b></div>\';\n'
    html += '  var numEvents = Math.min(3, activePol.length);\n'
    html += '  var usedTypes = {};\n'
    html += '  for (var ei = 0; ei < numEvents * 3 && Object.keys(usedTypes).length < numEvents; ei++) {\n'
    html += '    var evIdx = Math.floor(Math.random() * CLAIM_EVENTS.length);\n'
    html += '    var ev = CLAIM_EVENTS[evIdx];\n'
    html += '    // Match event type to a policy type\n'
    html += '    var matchingPol = activePol.find(function(p) {\n'
    html += '      if (ev.type === "health" && (p.type === "health")) return true;\n'
    html += '      if (ev.type === "accident" && (p.type === "accident" || p.type === "health")) return true;\n'
    html += '      if (ev.type === "property" && (p.type === "property")) return true;\n'
    html += '      if (ev.type === "vehicle" && (p.type === "vehicle")) return true;\n'
    html += '      return false;\n'
    html += '    });\n'
    html += '    if (!matchingPol || usedTypes[ev.name]) continue;\n'
    html += '    usedTypes[ev.name] = true;\n'
    html += '    var cost = ev.cost_range[0] + Math.random() * (ev.cost_range[1] - ev.cost_range[0]);\n'
    html += '    var payoutRatio = 0.5 + Math.random() * 0.5;  // 50-100% coverage ratio\n'
    html += '    var claimAmt = cost * payoutRatio;\n'
    html += '    h += \'<div class="claim-item">\';\n'
    html += '    h += \'<div class="claim-header"><span class="claim-event">⚠️ \' + ev.name + \'</span><span class="claim-amount">可赔 ¥\' + fmt(claimAmt) + \'</span></div>\';\n'
    html += '    h += \'<div class="claim-detail">涉及保单: \' + matchingPol.name + \' | 预估损失: ¥\' + fmt(cost) + \' | 赔付比例: \' + safeFixed(payoutRatio*100,0) + \'%</div>\';\n'
    html += '    var btnId = "claimbtn_" + ei;\n'
    html += '    h += \'<button class="btn-claim" id="\' + btnId + \'">发起理赔</button>\';\n'
    html += '    h += \'</div>\';\n'
    html += '    (function(bid,en,et,c,ca,pid){\n'
    html += '      document.getElementById(bid).onclick = function(){ createAndSubmitClaim(en,et,c,ca,pid); };\n'
    html += '    })(btnId,ev.name,ev.type,safeFixed(cost,0),safeFixed(claimAmt,0),matchingPol.id);\n'
    html += '  }\n'
    html += '  if (Object.keys(usedTypes).length === 0) {\n'
    html += '    h += \'<div style="text-align:center;color:#555;padding:20px;">暂无可理赔事件</div>\';\n'
    html += '  }\n'
    html += '  c.innerHTML = h;\n'
    html += '}\n\n'

    # Fix the # comment in JS string context
    html = html.replace('# 50-100% coverage ratio', '// 50-100% coverage ratio')

    # Create and submit claim
    html += 'function createAndSubmitClaim(eventName, eventType, lossCost, claimAmt, policyId) {\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) { alert("母锁验证失败: " + lock.msg); return; }\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  var d = getInsData(s);\n'
    html += '  var pol = (d.policies||[]).find(function(p){return p.id === policyId;});\n'
    html += '  if (!pol) { alert("保单不存在"); return; }\n'
    html += '  var claim = {\n'
    html += '    id: "claim_" + Date.now(),\n'
    html += '    policyId: policyId,\n'
    html += '    policyName: pol.name,\n'
    html += '    eventName: eventName,\n'
    html += '    eventType: eventType,\n'
    html += '    lossCost: lossCost,\n'
    html += '    claimAmount: claimAmt,\n'
    html += '    round: s.round || 0,\n'
    html += '    status: "approved"\n'
    html += '  };\n'
    html += '  d.claims.push(claim);\n'
    html += '  saveState(s);\n'
    html += '  alert("✅ 理赔已受理！\\n事件: " + eventName + "\\n赔款金额: ¥" + fmt(claimAmt) + "\\n点击\\"领取赔款\\"到账");'
    html += '  renderOverview();\n'
    html += '  renderClaims();\n'
    html += '}\n\n'

    # Receive claim payment
    html += 'function receiveClaim(claimId) {\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) { alert("母锁验证失败: " + lock.msg); return; }\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  var d = getInsData(s);\n'
    html += '  var claim = (d.claims||[]).find(function(c){return c.id === claimId;});\n'
    html += '  if (!claim || claim.status !== "approved") { alert("该理赔不可领取"); return; }\n'
    html += '  s.cash = (s.cash || 0) + claim.claimAmount;\n'
    html += '  claim.status = "paid";\n'
    html += '  d.totalClaimed = (d.totalClaimed || 0) + claim.claimAmount;\n'
    html += '  saveState(s);\n'
    html += '  alert("✅ 赔款已到账！¥" + fmt(claim.claimAmount));\n'
    html += '  renderOverview();\n'
    html += '  renderClaims();\n'
    html += '}\n\n'

    # Process insurance renewals (called each cycle from invest-sim or internally)
    html += 'function processInsuranceRenewals(roundNum) {\n'
    html += '  var s = loadState(); if (!s) return;\n'
    html += '  var d = getInsData(s);\n'
    html += '  if (!d.policies) return;\n'
    html += '  var renewedCount = 0;\n'
    html += '  d.policies.forEach(function(p) {\n'
    html += '    if (p.status !== "active") return;\n'
    html += '    p.remainingMonths = (p.remainingMonths || p.termMonths) - 1;\n'
    html += '    if (p.remainingMonths <= 0) {\n'
    html += '      p.status = "expired";\n'
    html += '      renewedCount++;\n'
    html += '    } else {\n'
    html += '      // Deduct monthly premium (annual / 12)\n'
    html += '      var monthlyPrem = p.annualPremium / 12;\n'
    html += '      if ((s.cash || 0) >= monthlyPrem) {\n'
    html += '        s.cash -= monthlyPrem;\n'
    html += '        d.totalPremium = (d.totalPremium || 0) + monthlyPrem;\n'
    html += '      } else {\n'
    html += '        // Insufficient funds - policy lapses\n'
    html += '        p.status = "expired";\n'
    html += '        renewedCount++;\n'
    html += '      }\n'
    html += '    }\n'
    html += '  });\n'
    html += '  if (renewedCount > 0) saveState(s);\n'
    html += '  return renewedCount;\n'
    html += '}\n\n'

    html += '</script>\n</body>\n</html>'
    return html


# Generate all insurance pages
for key, comp in companies.items():
    html = generate_insurance_page(key, comp)
    path = 'C:/Users/Ye201/WorkBuddy/2026-05-23-task-2/insurance-' + key + '.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Created: {path} ({comp["name"]})')
print('Done!')
