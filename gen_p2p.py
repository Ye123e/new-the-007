# -*- coding: utf-8 -*-
"""
gen_p2p.py - P2P借贷平台页面生成器
生成3个P2P平台: 陆金所(lufax)、拍拍贷(ppdai)、人人贷(renrendai)
每个平台独立HTML文件，通过 investSimState_v13 与主模拟器同步
"""

import json

# P2P platform definitions
platforms = {
    'lufax': {
        'name': '陆金所',
        'en': 'Lufax',
        'color': '#e53935',
        'emoji': '🏦',
        'region': 'mainland',
        'min_invest': 1000,
        'max_return': 0.12,
        'risk_levels': ['低风险', '中低风险', '中风险'],
        'description': '平安集团旗下，稳健型P2P平台，专注优质资产',
        'fee_rate': 0.02,  # 2% 管理费
        'default_prob': 0.03  # 3% 违约率
    },
    'ppdai': {
        'name': '拍拍贷',
        'en': 'Ppdai',
        'color': '#1e88e5',
        'emoji': '📊',
        'region': 'mainland',
        'min_invest': 100,
        'max_return': 0.18,
        'risk_levels': ['中风险', '中高风险', '高风险'],
        'description': '中国首家P2P平台，高收益伴随较高风险',
        'fee_rate': 0.03,
        'default_prob': 0.08
    },
    'renrendai': {
        'name': '人人贷',
        'en': 'Renrendai',
        'color': '#43a047',
        'emoji': '🤝',
        'region': 'mainland',
        'min_invest': 500,
        'max_return': 0.15,
        'risk_levels': ['低风险', '中低风险', '中风险', '中高风险'],
        'description': '人人友信旗下，风控严格，中等收益选择',
        'fee_rate': 0.025,
        'default_prob': 0.05
    }
}

# Predefined lending projects (will be randomly selected each session)
PROJECT_TEMPLATES = [
    {'title': '个人消费贷款', 'borrower': '张*明', 'purpose': '装修', 'amount_range': [10000, 80000], 'term_range': [3, 12], 'rate_range': [6, 10]},
    {'title': '小微企业周转', 'borrower': '李*公司', 'purpose': '采购原材料', 'amount_range': [30000, 150000], 'term_range': [6, 24], 'rate_range': [8, 13]},
    {'title': '车辆抵押贷款', 'borrower': '王*华', 'purpose': '购车', 'amount_range': [20000, 120000], 'term_range': [6, 36], 'rate_range': [5, 9]},
    {'title': '教育进修贷款', 'borrower': '陈*静', 'purpose': 'MBA学费', 'amount_range': [15000, 60000], 'term_range': [12, 36], 'rate_range': [7, 11]},
    {'title': '医疗支出贷款', 'borrower': '刘*强', 'purpose': '手术费用', 'amount_range': [5000, 40000], 'term_range': [3, 12], 'rate_range': [8, 14]},
    {'title': '房产装修贷款', 'borrower': '赵*芳', 'purpose': '房屋翻新', 'amount_range': [20000, 100000], 'term_range': [6, 18], 'rate_range': [6, 10]},
    {'title': '创业启动资金', 'borrower': '孙*伟', 'purpose': '开餐厅', 'amount_range': [50000, 200000], 'term_range': [12, 24], 'rate_range': [10, 16]},
    {'title': '供应链金融', 'borrower': '周*贸易', 'purpose': '货款垫付', 'amount_range': [80000, 300000], 'term_range': [3, 6], 'rate_range': [7, 11]},
    {'title': '农业种植贷款', 'borrower': '吴*农', 'purpose': '购买种子化肥', 'amount_range': [10000, 50000], 'term_range': [6, 12], 'rate_range': [9, 15]},
    {'title': '信用卡代偿', 'borrower': '郑*磊', 'purpose': '信用卡还款', 'amount_range': [5000, 30000], 'term_range': [3, 6], 'rate_range': [12, 20]},
]


def generate_p2p_page(key, plat):
    color = plat['color']
    name = plat['name']
    en = plat['en']
    emoji = plat['emoji']
    min_inv = plat['min_invest']
    max_ret = plat['max_return']
    risk_levels = json.dumps(plat['risk_levels'], ensure_ascii=False)
    desc = plat['description']
    fee_rate = plat['fee_rate']
    default_prob = plat['default_prob']

    html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
    html += '<title>' + name + ' - P2P借贷平台</title>\n'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'

    # CSS styles
    html += '<style>\n'
    html += '* { margin:0; padding:0; box-sizing:border-box; }\n'
    html += 'body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#0a0e17; color:#e0e0e0; min-height:100vh; }\n'
    html += '.header { background:linear-gradient(135deg,' + color + ',' + color + '99); padding:20px 24px; display:flex;align-items:center;gap:14px; }\n'
    html += '.header-icon { width:48px;height:48px;background:rgba(255,255,255,0.2);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:26px; }\n'
    html += '.header-info h1 { font-size:22px;color:#fff; }\n'
    html += '.header-info p { font-size:12px;color:rgba(255,255,255,0.75);margin-top:2px; }\n'
    html += '.container { max-width:900px;margin:0 auto;padding:16px; }\n'
    html += '.login-box { background:#131823;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:28px;margin-top:20px;text-align:center; }\n'
    html += '.login-box h2 { font-size:18px;margin-bottom:12px;color:' + color + '; }\n'
    html += '.login-box p { font-size:13px;color:#888;margin-bottom:18px;line-height:1.6; }\n'
    html += '.login-btn { display:inline-block;padding:12px 40px;background:' + color + ';color:#fff;border:none;border-radius:8px;font-size:15px;cursor:pointer;font-weight:600;transition:transform 0.2s; }\n'
    html += '.login-btn:hover { transform:scale(1.04); }\n'
    html += '.lock-chain { display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:16px;font-size:11px;color:#666; }\n'
    html += '.lock-dot { width:8px;height:8px;border-radius:50%;background:#444; }\n'
    html += '.lock-dot.active { background:#4caf50;box-shadow:0 0 6px #4caf50; }\n'
    html += '.lock-line { width:30px;height:2px;background:#333;position:relative; }\n'
    html += '.lock-line.active { background:#4caf50; }\n'
    html += '.main-app { display:none; }\n'
    html += '.nav-tabs { display:flex;gap:4px;margin-bottom:16px;flex-wrap:wrap; }\n'
    html += '.nav-tab { padding:8px 16px;border-radius:8px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#888;transition:all 0.2s;flex:0 0 auto; }\n'
    html += '.nav-tab.active { background:' + color + '22;color:' + color + ';border-color:' + color + '44;font-weight:600; }\n'
    html += '.tab-panel { display:none; }\n'
    html += '.tab-panel.active { display:block; }\n'
    html += '.stat-row { display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px; }\n'
    html += '.stat-card { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;text-align:center; }\n'
    html += '.stat-value { font-size:20px;font-weight:700;color:' + color + '; }\n'
    html += '.stat-label { font-size:11px;color:#777;margin-top:2px; }\n'
    # Project card styles
    html += '.project-list { display:flex;flex-direction:column;gap:10px; }\n'
    html += '.project-card { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:16px;transition:border-color 0.2s; }\n'
    html += '.project-card:hover { border-color:' + color + '33; }\n'
    html += '.proj-header { display:flex;justify-content:space-between;align-items:start;margin-bottom:10px; }\n'
    html += '.proj-title { font-size:15px;font-weight:600; }\n'
    html += '.proj-rate { text-align:right; }\n'
    html += '.proj-rate-val { font-size:22px;font-weight:700;color:#ff5252; }  # red=profit in China\n'
    html += '.proj-rate-label { font-size:11px;color:#777; }\n'
    html += '.proj-meta { display:flex;gap:16px;font-size:11px;color:#999;flex-wrap:wrap;margin-bottom:10px; }\n'
    html += '.proj-progress { margin-bottom:12px; }\n'
    html += '.prog-bar { height:6px;background:#222;border-radius:3px;overflow:hidden; }\n'
    html += '.prog-fill { height:100%;background:linear-gradient(90deg,' + color + ',' + color + '88);border-radius:3px;transition:width 0.3s; }\n'
    html += '.proj-footer { display:flex;justify-content:space-between;align-items:center; }\n'
    html += '.risk-badge { display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600; }\n'
    html += '.risk-low { background:rgba(76,175,80,0.15);color:#4caf50; }\n'
    html += '.risk-mid { background:rgba(255,193,7,0.15);color:#ffc107; }\n'
    html += '.risk-high { background:rgba(244,67,54,0.15);color:#f44336; }\n'
    # Investment form
    html += '.invest-form { display:flex;align-items:center;gap:8px;margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,0.05); }\n'
    html += '.invest-input { width:120px;padding:8px 10px;background:#1a1f2e;border:1px solid rgba(255,255,255,0.1);border-radius:6px;color:#fff;font-size:14px;outline:none; }\n'
    html += '.invest-input:focus { border-color:' + color + '; }\n'
    html += '.btn-invest { padding:8px 20px;background:' + color + ';color:#fff;border:none;border-radius:6px;font-size:13px;cursor:pointer;font-weight:600; }\n'
    html += '.btn-invest:hover { opacity:0.85; }\n'
    html += '.btn-invest:disabled { opacity:0.4;cursor:not-allowed; }\n'
    # My investments panel
    html += '.inv-table { width:100%;border-collapse:collapse; }\n'
    html += '.inv-table th { text-align:left;font-size:11px;color:#777;padding:8px 6px;border-bottom:1px solid rgba(255,255,255,0.06);font-weight:500; }\n'
    html += '.inv-table td { padding:10px 6px;border-bottom:1px solid rgba(255,255,255,0.03);font-size:12px;vertical-align:middle; }\n'
    html += '.inv-status { padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600; }\n'
    html += '.status-progressing { background:rgba(33,150,243,0.15);color:#2196f3; }\n'
    html += '.status-repaid { background:rgba(76,175,80,0.15);color:#4caf50; }\n'
    html += '.status-defaulted { background:rgba(244,67,54,0.15);color:#f44336; }\n'
    html += '.profit-pos { color:#ff5252;font-weight:600; }  # red=profit\n'
    html += '.profit-neg { color:#00e676;font-weight:600; }  # green=loss\n'
    # Account overview
    html += '.acct-summary { background:#131823;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:18px;margin-bottom:14px; }\n'
    html += '.acct-row { display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px; }\n'
    html += '.acct-row:last-child { border-bottom:none; }\n'
    html += '.acct-label { color:#888; }\n'
    html += '.acct-value { font-weight:600; }\n'
    # Repayment schedule
    html += '.repay-item { display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.04); }\n'
    html += '.repay-date { font-size:11px;color:#888;width:90px; }\n'
    html += '.repay-amount { font-weight:600;font-size:13px; }\n'
    html += '.repay-status { font-size:10px;padding:2px 6px;border-radius:4px; }\n'
    # Notice box
    html += '.notice { padding:10px 14px;background:rgba(255,152,0,0.06);border:1px solid rgba(255,152,0,0.15);border-radius:8px;font-size:11px;color:#ccc;line-height:1.6; }\n'
    html += '</style>\n</head>\n<body>\n'

    # Header
    html += '<div class="header">\n'
    html += '  <div class="header-icon">' + emoji + '</div>\n'
    html += '  <div class="header-info"><h1>' + name + '</h1><p>' + en + ' · ' + desc + '</p></div>\n'
    html += '</div>\n'

    html += '<div class="container">\n'

    # Login screen (with master-slave lock verification)
    html += '<div id="loginScreen" class="login-box">\n'
    html += '  <div class="lock-chain" id="lockChain"></div>\n'
    html += '  <h2>🔐 登录 ' + name + '</h2>\n'
    html += '  <p>安全登录以访问您的P2P投资账户<br>需要母锁令牌验证</p>\n'
    html += '  <button class="login-btn" onclick="doLogin()">🔑 验证并登录</button>\n'
    html += '  <p id="loginError" style="color:#f44336;margin-top:10px;display:none;"></p>\n'
    html += '</div>\n'

    # Main application (hidden until login)
    html += '<div id="mainApp" class="main-app">\n'

    # Navigation tabs
    html += '  <div class="nav-tabs">\n'
    html += '    <div class="nav-tab active" data-pTab="overview">📊 概览</div>\n'
    html += '    <div class="nav-tab" data-pTab="invest">💰 投标</div>\n'
    html += '    <div class="nav-tab" data-pTab="myinv">📋 我的投资</div>\n'
    html += '    <div class="nav-tab" data-pTab="repay">📅 回款计划</div>\n'
    html += '  </div>\n'

    # Overview panel
    html += '  <div id="pTab-overview" class="tab-panel active">\n'
    html += '    <div id="acctSummary" class="acct-summary"></div>\n'
    html += '    <div class="notice">⚠️ P2P投资有风险，本金可能因借款人违约而受损。' + name + '历史违约率约' + str(int(default_prob * 100)) + '%，请根据自身风险承受能力合理配置。</div>\n'
    html += '  </div>\n'

    # Invest panel (project list)
    html += '  <div id="pTab-invest" class="tab-panel">\n'
    html += '    <div id="projectList" class="project-list"></div>\n'
    html += '  </div>\n'

    # My investments panel
    html += '  <div id="pTab-myinv" class="tab-panel">\n'
    html += '    <div id="myInvestments" style="overflow-x:auto;"><table class="inv-table"><thead><tr><th>项目</th><th>投资额</th><th>年化</th><th>期限</th><th>已收</th><th>状态</th><th>收益</th></tr></thead><tbody id="invBody"></tbody></table></div>\n'
    html += '  </div>\n'

    # Repayment schedule panel
    html += '  <div id="pTab-repay" class="tab-panel">\n'
    html += '    <div id="repaySchedule"></div>\n'
    html += '  </div>\n'

    html += '</div>\n'  # end mainApp
    html += '</div>\n'  # end container

    # JavaScript
    html += '<script>\n'
    html += "const PLATFORM_KEY = '" + key + "';\n"
    html += "const PLATFORM_NAME = '" + name + "';\n"
    html += "const PLATFORM_COLOR = '" + color + "';\n"
    html += 'const MIN_INVEST = ' + str(min_inv) + ';\n'
    html += 'const FEE_RATE = ' + str(fee_rate) + ';\n'
    html += 'const DEFAULT_PROB = ' + str(default_prob) + ';\n'
    html += 'var STORAGE_KEY = "investSimState_v13";\n'
    html += 'var isLoggedIn = false;\n'
    html += "var RISK_LEVELS = " + risk_levels + ";\n"

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
    html += '    var now = Date.now();\n'
    html += '    if (now - token.time > 3600000) return { ok:false, msg:"母锁令牌已过期(>1小时)，请重新打开模拟器" };\n'
    html += '    return { ok:true, token:token };\n'
    html += '  } catch(e) { return { ok:false, msg:"令牌解析失败" }; }\n'
    html += '}\n\n'

    # Render lock chain UI
    html += 'function renderLockChain() {\n'
    html += '  var c = document.getElementById("lockChain");\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  c.innerHTML = \'<span class="lock-dot \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-line \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-dot \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span class="lock-line \'+(lock.ok?"active":"")+\'"></span>\'+\n'
    html += '    \'<span style="font-size:10px;color:\'+(lock.ok?"#4caf50":"#666")+\'">\'+(lock.ok?"母锁→数据 已连接":"母锁→数据 断开")+\'</span>\';\n'
    html += '}\n\n'

    # Load shared state
    html += 'function loadState() {\n'
    html += '  try {\n'
    html += '    var raw = localStorage.getItem(STORAGE_KEY);\n'
    html += '    if (!raw) return null;\n'
    html += '    return JSON.parse(raw);\n'
    html += '  } catch(e) { return null; }\n'
    html += '}\n\n'
    html += 'function saveState(s) {\n'
    html += '  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch(e) {}\n'
    html += '}\n\n'

    # Get/create p2p data for this platform
    html += 'function getP2PData(state) {\n'
    html += '  if (!state.p2pInvestments) state.p2pInvestments = {};\n'
    html += '  if (!state.p2pInvestments[PLATFORM_KEY]) {\n'
    html += '    state.p2pInvestments[PLATFORM_KEY] = {\n'
    html += '      totalInvested: 0,\n'
    html += '      totalReceived: 0,\n'
    html += '      totalProfit: 0,\n'
    html += '      activeCount: 0,\n'
    html += '      completedCount: 0,\n'
    html += '      defaultedCount: 0,\n'
    html += '      investments: [],\n'
    html += '      repaySchedule: []\n'
    html += '    };\n'
    html += '  }\n'
    html += '  return state.p2pInvestments[PLATFORM_KEY];\n'
    html += '}\n\n'

    # Get cash from simulator
    html += 'function getCash() {\n'
    html += '  var s = loadState();\n'
    html += '  return s ? s.cash : 0;\n'
    html += '}\n\n'

    # Generate random projects based on templates
    html += 'function generateProjects() {\n'
    html += '  var templates = ' + json.dumps(PROJECT_TEMPLATES, ensure_ascii=False) + ';\n'
    html += '  var projects = [];\n'
    html += '  var used = {};\n'
    html += '  // Pick 6 random projects\n'
    html += '  while (projects.length < 6 && Object.keys(used).length < templates.length) {\n'
    html += '    var idx = Math.floor(Math.random() * templates.length);\n'
    html += '    if (used[idx]) continue;\n'
    html += '    used[idx] = true;\n'
    html += '    var t = templates[idx];\n'
    html += '    var amt = t.amount_range[0] + Math.floor(Math.random() * (t.amount_range[1] - t.amount_range[0]));\n'
    html += '    var term = t.term_range[0] + Math.floor(Math.random() * (t.term_range[1] - t.term_range[0]));\n'
    html += '    var rate = t.rate_range[0] + Math.random() * (t.rate_range[1] - t.rate_range[0]);\n'
    html += '    var funded = Math.floor(Math.random() * amt * 0.7);  // 0-70% funded\n'
    html += '    var rIdx = Math.min(Math.floor((rate - 5) / 4), RISK_LEVELS.length - 1);\n'
    html += '    rIdx = Math.max(0, rIdx);\n'
    html += '    projects.push({\n'
    html += '      id: "proj_" + Date.now() + "_" + idx,\n'
    html += '      title: t.title,\n'
    html += '      borrower: t.borrower,\n'
    html += '      purpose: t.purpose,\n'
    html += '      amount: amt,\n'
    html += '      term: term,\n'
    html += '      rate: rate / 100,\n'
    html += '      funded: funded,\n'
    html += '      riskLevel: RISK_LEVELS[rIdx] || RISK_LEVELS[0]\n'
    html += '    });\n'
    html += '  }\n'
    html += '  return projects;\n'
    html += '}\n\n'
    html += 'var currentProjects = [];\n\n'

    # Login function
    html += 'function doLogin() {\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) {\n'
    html += '    var el = document.getElementById("loginError");\n'
    html += '    el.textContent = lock.msg;\n'
    html += '    el.style.display = "block";\n'
    html += '    renderLockChain();\n'
    html += '    return;\n'
    html += '  }\n'
    html += '  isLoggedIn = true;\n'
    html += '  document.getElementById("loginScreen").style.display = "none";\n'
    html += '  document.getElementById("mainApp").style.display = "block";\n'
    html += '  currentProjects = generateProjects();\n'
    html += '  renderOverview();\n'
    html += '  renderProjects();\n'
    html += '  renderMyInvestments();\n'
    html += '  renderRepaySchedule();\n'
    html += '}\n\n'

    # Tab switching
    html += 'document.addEventListener("DOMContentLoaded", function() {\n'
    html += '  renderLockChain();\n'
    html += '  document.querySelectorAll(".nav-tab").forEach(function(tab) {\n'
    html += '    tab.addEventListener("click", function() {\n'
    html += '      document.querySelectorAll(".nav-tab").forEach(function(t){t.classList.remove("active")});\n'
    html += '      this.classList.add("active");\n'
    html += '      document.querySelectorAll(".tab-panel").forEach(function(p){p.classList.remove("active")});\n'
    html += '      var target = "pTab-" + this.getAttribute("data-pTab");\n'
    html += '      var panel = document.getElementById(target);\n'
    html += '      if (panel) panel.classList.add("active");\n'
    html += '      if (target === "pTab-overview") renderOverview();\n'
    html += '      if (target === "pTab-invest") renderProjects();\n'
    html += '      if (target === "pTab-myinv") renderMyInvestments();\n'
    html += '      if (target === "pTab-repay") renderRepaySchedule();\n'
    html += '    });\n'
    html += '  });\n'
    html += '});\n\n'

    # Render overview
    html += 'function renderOverview() {\n'
    html += '  var s = loadState();\n'
    html += '  if (!s) return;\n'
    html += '  var d = getP2PData(s);\n'
    html += '  var cash = s.cash || 0;\n'
    html += '  var container = document.getElementById("acctSummary");\n'
    html += '  var h = \'\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">📱 平台</span><span class="acct-value">\' + PLATFORM_NAME + \'</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">💰 模拟器现金</span><span class="acct-value">¥\' + fmt(cash) + \'</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">📊 累计投资</span><span class="acct-value">¥\' + fmt(d.totalInvested) + \'</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">✅ 已收回</span><span class="acct-value" style="color:#4caf50;">¥\' + fmt(d.totalReceived) + \'</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">📈 累计收益</span><span class="acct-value" style="color:\' + (d.totalProfit >= 0 ? "#ff5252" : "#00e676") + \';">\' + (d.totalProfit >= 0 ? "+" : "") + \'¥\' + fmt(d.totalProfit) + \'</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">🔄 进行中</span><span class="acct-value">\' + d.activeCount + \' 笔</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">✔️ 已完成</span><span class="acct-value">\' + d.completedCount + \' 笔</span></div>\';\n'
    html += '  h += \'<div class="acct-row"><span class="acct-label">⚠️ 已违约</span><span class="acct-value" style="color:#f44336;">\' + d.defaultedCount + \' 笔</span></div>\';\n'
    html += '  container.innerHTML = h;\n'
    html += '}\n\n'

    # Render project list
    html += 'function renderProjects() {\n'
    html += '  var container = document.getElementById("projectList");\n'
    html += '  if (!container || currentProjects.length === 0) return;\n'
    html += '  var cash = getCash();\n'
    html += '  var h = \'\';\n'
    html += '  currentProjects.forEach(function(p, i) {\n'
    html += '    var pct = Math.round(p.funded / p.amount * 100);\n'
    html += '    var remaining = p.amount - p.funded;\n'
    html += '    var riskClass = p.riskLevel.includes("高") ? "risk-high" : (p.riskLevel.includes("低") ? "risk-low" : "risk-mid");\n'
    html += '    h += \'<div class="project-card">\';\n'
    html += '    h += \'<div class="proj-header">\';\n'
    html += '    h += \'<div><div class="proj-title">\' + p.title + \'</div>\';\n'
    html += '    h += \'<div class="proj-meta"><span>👤 \' + p.borrower + \'</span><span>🎯 \' + p.purpose + \'</span><span>⏱ \' + p.term + \'个月</span></div></div>\';\n'
    html += '    h += \'<div class="proj-rate"><div class="proj-rate-val">\' + safeFixed(p.rate * 100, 1) + \'%</div><div class="proj-rate-label">预期年化</div></div>\';\n'
    html += '    h += \'</div>\';\n'
    html += '    h += \'<div class="proj-progress"><div class="prog-bar"><div class="prog-fill" style="width:\' + pct + \'%;"></div></div></div>\';\n'
    html += '    h += \'<div class="proj-footer">\';\n'
    html += '    h += \'<span><span class="risk-badge \' + riskClass + \'">\' + p.riskLevel + \'</span> 剩余 ¥\' + fmt(remaining) + \' / 总额 ¥\' + fmt(p.amount) + \'</span>\';\n'
    html += '    h += \'</div>\';\n'
    html += '    h += \'<div class="invest-form">\';\n'
    html += '    h += \'<input type="number" class="invest-input" id="invAmt_\' + i + \'" placeholder="最低 ¥\' + MIN_INVEST + \'" min="\' + MIN_INVEST + \'" step="100">\';\n'
    html += '    h += \'<button class="btn-invest" onclick="doInvest(\' + i + \')" \' + (cash < MIN_INVEST ? "disabled" : "") + \'>立即投标</button>\';\n'
    html += '    h += \'</div>\';\n'
    html += '    h += \'</div>\';\n'
    html += '  });\n'
    html += '  container.innerHTML = h;\n'
    html += '}\n\n'

    # Execute investment
    html += 'function doInstall(idx) {\n'
    html += '  // Lock check first\n'
    html += '  var lock = checkMasterLock();\n'
    html += '  if (!lock.ok) { alert("母锁验证失败: " + lock.msg); isLoggedIn = false; location.reload(); return; }\n\n'
    html += '  var p = currentProjects[idx];\n'
    html += '  if (!p) return;\n'
    html += '  var input = document.getElementById("invAmt_" + idx);\n'
    html += '  if (!input) return;\n'
    html += '  var amount = parseFloat(input.value);\n'
    html += '  if (!amount || amount < MIN_INVEST || isNaN(amount)) { alert("最低投资金额 ¥" + MIN_INVEST); return; }\n'
    html += '  if (amount > (p.amount - p.funded)) { alert("不能超过剩余可投金额"); return; }\n\n'
    html += '  var s = loadState();\n'
    html += '  if (!s) return;\n'
    html += '  if ((s.cash || 0) < amount) { alert("模拟器现金不足！当前: ¥" + fmt(s.cash)); return; }\n\n'
    html += '  // Deduct cash\n'
    html += '  s.cash -= amount;\n\n'
    html += '  // Create investment record\n'
    html += '  var d = getP2PData(s);\n'
    html += '  var inv = {\n'
    html += '    id: "inv_" + Date.now(),\n'
    html += '    projectId: p.id,\n'
    html += '    title: p.title,\n'
    html += '    borrower: p.borrower,\n'
    html += '    amount: amount,\n'
    html += '    rate: p.rate,\n'
    html += '    term: p.term,\n'
    html += '    investedAt: Date.now(),\n'
    html += '    round: s.round || 0,\n'
    html += '    status: "progressing",\n'
    html += '    received: 0,\n'
    html += '    expectedReturn: amount * (1 + p.rate * p.term / 12),\n'
    html += '    profit: 0,\n'
    html += '    riskLevel: p.riskLevel,\n'
    html += '    nextRepaymentRound: (s.round || 0) + Math.ceil(p.term / (p.term > 6 ? p.term / 6 : 1)),\n'
    html += '    totalRepayments: p.term <= 6 ? p.term : Math.ceil(p.term / (p.term > 6 ? p.term / 6 : 1)),\n'
    html += '    repaidCount: 0\n'
    html += '  };\n'
    html += '  d.investments.push(inv);\n'
    html += '  d.totalInvested += amount;\n'
    html += '  d.activeCount += 1;\n\n'
    html += '  // Add to repayment schedule\n'
    html += '  var perPayment = inv.expectedReturn / inv.totalRepayments;\n'
    html += '  var startRound = s.round || 0;\n'
    html += '  for (var r = 0; r < inv.totalRepayments; r++) {\n'
    html += '    d.repaySchedule.push({\n'
    html += '      invId: inv.id,\n'
    html += '      title: p.title,\n'
    html += '      amount: perPayment,\n'
    html += '      principal: amount / inv.totalRepayments,\n'
    html += '      interest: perPayment - amount / inv.totalRepayments,\n'
    html += '      dueRound: startRound + (r + 1) * Math.max(1, Math.floor(p.term / inv.totalRepayments)),\n'
    html += '      status: "pending"\n'
    html += '    });\n'
    html += '  }\n\n'
    html += '  // Update project funding\n'
    html += '  p.funded += amount;\n\n'
    html += '  saveState(s);\n'
    html += '  alert("✅ 投资成功！\\n项目: " + p.title + "\\n金额: ¥" + fmt(amount) + "\\n预期收益: ¥" + fmt(inv.expectedReturn - amount));\n'
    html += '  renderOverview();\n'
    html += '  renderProjects();\n'
    html += '  renderMyInvestments();\n'
    html += '  renderRepaySchedule();\n'
    html += '}\n\n'
    # NOTE: There's a typo above - doInstall should be doInvest. Let me fix it in the output.
    # The function name reference in onclick is doInvest, so I need to rename.

    # Fix: replace the function name
    html = html.replace('function doInstall(idx)', 'function doInvest(idx)')

    # Render my investments table
    html += 'function renderMyInvestments() {\n'
    html += '  var s = loadState();\n'
    html += '  if (!s) return;\n'
    html += '  var d = getP2PData(s);\n'
    html += '  var tbody = document.getElementById("invBody");\n'
    html += '  if (!tbody) return;\n'
    html += '  if (!d.investments || d.investments.length === 0) {\n'
    html += '    tbody.innerHTML = \'<tr><td colspan="7" style="text-align:center;color:#555;padding:20px;">暂无投资记录</td></tr>\';\n'
    html += '    return;\n'
    html += '  }\n'
    html += '  var h = \'\';\n'
    html += '  d.investments.forEach(function(inv) {\n'
    html += '    var statusClass = inv.status === "repaid" ? "status-repaid" : (inv.status === "defaulted" ? "status-defaulted" : "status-progressing");\n'
    html += '    var statusText = inv.status === "repaid" ? "已结清" : (inv.status === "defaulted" ? "已违约" : "回款中");\n'
    html += '    var profitClass = inv.profit >= 0 ? "profit-pos" : "profit-neg";\n'
    html += '    h += \'<tr>\';\n'
    html += '    \'<td>\' + inv.title + \'</td>\';\n'
    html += '    h += \'<td>¥\' + fmt(inv.amount) + \'</td>\';\n'
    html += '    h += \'<td>\' + safeFixed(inv.rate * 100, 1) + \'%</td>\';\n'
    html += '    h += \'<td>\' + inv.term + \'月</td>\';\n'
    html += '    h += \'<td>¥\' + fmt(inv.received) + \'</td>\';\n'
    html += '    h += \'<td><span class="\' + statusClass + \'">\' + statusText + \'</span></td>\';\n'
    html += '    h += \'<td class="\' + profitClass + \'">\' + (inv.profit >= 0 ? "+" : "") + \'¥\' + fmt(inv.profit) + \'</td>\';\n'
    html += '    h += \'</tr>\';\n'
    html += '  });\n'
    html += '  tbody.innerHTML = h;\n'
    html += '}\n\n'

    # Render repayment schedule
    html += 'function renderRepaySchedule() {\n'
    html += '  var s = loadState();\n'
    html += '  if (!s) return;\n'
    html += '  var d = getP2PData(s);\n'
    html += '  var container = document.getElementById("repaySchedule");\n'
    html += '  if (!container) return;\n'
    html += '  if (!d.repaySchedule || d.repaySchedule.length === 0) {\n'
    html += '    container.innerHTML = \'<div style="text-align:center;color:#555;padding:30px;">暂无回款计划</div>\';\n'
    html += '    return;\n'
    html += '  }\n'
    html += '  // Sort by dueRound ascending\n'
    html += '  var sorted = d.repaySchedule.slice().sort(function(a,b){ return a.dueRound - b.dueRound; });\n'
    html += '  var currentRound = s.round || 0;\n'
    html += '  var h = \'<div style="margin-bottom:10px;font-size:12px;color:#888;">当前回合: \' + currentRound + \' | 共 \' + sorted.length + \' 条待收</div>\';\n'
    html += '  sorted.forEach(function(r) {\n'
    html += '    var overdue = currentRound > r.dueRound && r.status === "pending";\n'
    html += '    var done = r.status === "paid";\n'
    html += '    var stClass = done ? "status-repaid" : (overdue ? "status-defaulted" : "status-progressing");\n'
    html += '    var stText = done ? "已到账" : (overdue ? "逾期" : "待收");\n'
    html += '    h += \'<div class="repay-item">\';\n'
    html += '    h += \'<span><b>\' + r.title + \'</b></span>\';\n'
    html += '    h += \'<span class="repay-date">第\' + r.dueRound + \'回合</span>\';\n'
    html += '    h += \'<span class="repay-amount">¥\' + fmt(r.amount) + \'</span>\';\n'
    html += '    h += \'<span class="repay-status \' + stClass + \'">\' + stText + \'</span>\';\n'
    html += '    h += \'</div>\';\n'
    html += '  });\n'
    html += '  container.innerHTML = h;\n'
    html += '}\n\n'

    # Process repayments (called from invest-sim.html or manually)
    html += 'function processP2PRepayments(roundNum) {\n'
    html += '  var s = loadState();\n'
    html += '  if (!s) return;\n'
    html += '  var d = getP2PData(s);\n'
    html += '  if (!d.repaySchedule) return;\n'
    html += '  var processed = 0;\n'
    html += '  d.repaySchedule.forEach(function(r) {\n'
    html += '    if (r.status !== "pending" || r.dueRound > roundNum) return;\n'
    html += '    // Check for default (probability-based)\n'
    html += '    var willDefault = Math.random() < DEFAULT_PROB;\n'
    html += '    if (willDefault) {\n'
    html += '      r.status = "defaulted";\n'
    html += '      // Mark investment as defaulted\n'
    html += '      var inv = d.investments.find(function(i){ return i.id === r.invId; });\n'
    html += '      if (inv && inv.status !== "defaulted") {\n'
    html += '        inv.status = "defaulted";\n'
    html += '        d.defaultedCount += 1;\n'
    html += '        d.activeCount = Math.max(0, d.activeCount - 1);\n'
    html += '      }\n'
    html += '    } else {\n'
    html += '      r.status = "paid";\n'
    html += '      // Add cash back with fee deduction\n'
    html += '      var netAmount = r.amount * (1 - FEE_RATE);\n'
    html += '      s.cash = (s.cash || 0) + netAmount;\n'
    html += '      d.totalReceived += netAmount;\n'
    html += '      // Update investment record\n'
    html += '      var inv = d.investments.find(function(i){ return i.id === r.invId; });\n'
    html += '      if (inv) {\n'
    html += '        inv.received = (inv.received || 0) + netAmount;\n'
    html += '        inv.profit = inv.received - inv.amount;\n'
    html += '        inv.repaidCount = (inv.repaidCount || 0) + 1;\n'
    html += '        // Check if fully repaid\n'
    html += '        if (inv.repaidCount >= inv.totalRepayments) {\n'
    html += '          inv.status = "repaid";\n'
    html += '          d.completedCount += 1;\n'
    html += '          d.activeCount = Math.max(0, d.activeCount - 1);\n'
    html += '          d.totalProfit += inv.profit;\n'
    html += '        }\n'
    html += '      }\n'
    html += '    }\n'
    html += '    processed++;\n'
    html += '  });\n'
    html += '  if (processed > 0) saveState(s);\n'
    html += '  return processed;\n'
    html += '}\n\n'

    html += '</script>\n</body>\n</html>'
    return html


# Generate all P2P pages
for key, plat in platforms.items():
    html = generate_p2p_page(key, plat)
    path = 'C:/Users/Ye201/WorkBuddy/2026-05-23-task-2/p2p-' + key + '.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Created: {path} ({plat["name"]})')
print('Done!')
