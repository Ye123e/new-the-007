# Explore-3 代码审查报告

审查范围: 券商/P2P/保险 HTML 页面 + Python 生成器 + invest-sim.html 集成

---

## 🔴 严重 Bug（4个）

### Bug #1: CSS 语法错误 — 理赔按钮 hover 样式完全失效
| 项目 | 详情 |
|------|------|
| **来源** | gen_insurance.py 第159行 |
| **影响** | insurance-aia.html, insurance-pingan.html, insurance-picc.html |
| **问题代码** | `.btn-claim:hover {notdisabled} { background:#43a047; }` |
| **分析** | `{notdisabled}` 是非法 CSS 选择器语法，浏览器忽略整条规则 |
| **修复建议** | 改为 `.btn-claim:hover:not(:disabled) { background:#43a047; }` |

---

### Bug #2: P2P 页面 renderMyInvestments() 缺少字符串拼接 — 投资列表第一列为空
| 项目 | 详情 |
|------|------|
| **来源** | gen_p2p.py 第503行（仅此1行缺失，504-510行正常） |
| **影响** | p2p-lufax.html, p2p-ppdai.html, p2p-renrendai.html |
| **问题代码** | `'<td>' + inv.title + '</td>';` （缺少 `h += ` 前缀） |
| **分析** | 字符串被计算后立即丢弃，不追加到变量 h。其他列有 h+= 正常显示，导致表格错位 |
| **修复建议** | 改为 `h += '<td>' + inv.title + '</td>';` |

---

### Bug #3 [最关键]: 母锁 token 字段名跨文件不匹配 — P2P/保险页面无法打开

#### invest-sim.html 写入的两套不同 token 结构：

**结构 A — refreshMasterToken() (第2567-2571行)**，在 saveState() 时调用：
```javascript
const token = {
    ts: Date.now(),
    seal: Math.random().toString(36).slice(2) + Date.now().toString(36),
    status: 'active'
};
```

**结构 B — processInsurance() (第8203-8206行)**，保险处理时覆盖写入：
```javascript
const token = {
    value: 'ins_' + Date.now() + '_' + Math.random().toString(36).substr(2,12),
    issuedAt: Date.now(),
    expiresAt: Date.now() + 3600000
};
```

#### 各子页面生成器的 token 读取：

| 生成器文件 | 行号 | 读取字段 | 匹配状态 |
|-----------|------|---------|---------|
| gen_brokers.py | 300 | `token.ts` | 匹配结构 A ✓ |
| gen_p2p.py | 244 | `token.time` | **不匹配 ✗ → NaN → 永远过期** |
| gen_insurance.py | 249 | `token.time` | **不匹配 ✗ → NaN → 永远过期** |

#### 影响分析：
- **券商页面** (broker-citics/goldman)：正常工作
- **P2P 页面** (lufax/ppdai/renrendai)：完全无法打开（令牌验证永远失败）
- **保险页面** (aia/pingan/picc)：完全无法打开（同上）

#### 修复方案：
统一为一种 token 结构，建议全部使用结构 A `{ts, seal, status}`：
- gen_p2p.py 第244行：`token.time` → `token.ts`
- gen_insurance.py 第249行：`token.time` → `token.ts`
- invest-sim.html processInsurance()：删除自行构造 token 的代码，改为调用 refreshMasterToken()

---

### Bug #4: invest-sim.html 内部 token 结构自相矛盾
| 项目 | 详情 |
|------|------|
| **来源** | invest-sim.html 第2567行 vs 第8203行 |
| **问题** | refreshMasterToken() 和 processInsurance() 写入的 token 格式完全不同 |
| **影响** | 两套结构互相覆盖 localStorage 中的 `invest_sim_master`，子页面无法同时适配 |
| **修复建议** | processInsurance() 应调用已有的 refreshMasterToken() 方法，而非自行构造新 token |

---

## 🟡 中等 Bug（3个）

### Bug #5: 券商 sell 按钮 HTML 结构错误
| 项目 | 详情 |
|------|------|
| **来源** | gen_brokers.py 第239行 |
| **影响** | broker-citics.html, broker-goldman.html |
| **问题代码** | `html += '    <    <button class="sell-btn" id="sellBtn" onclick="executeTrade(\'sell\')">📉 卖出</button>\n'` |
| **分析** | 按钮标签前有多余的 `<    ` 前缀字符，浏览器可能将其解析为标签开始 |
| **修复建议** | 删除多余的 `<    `，改为 `'    <button class="sell-btn"...` |

---

### Bug #6: renderPositions() class 属性引号错位
| 项目 | 详情 |
|------|------|
| **来源** | gen_brokers.py 第555-556行 |
| **影响** | 所有券商页面的持仓列表盈亏列 |
| **问题代码** | `h += '<td class="pos-profit "\'+(pnl>=0?"positive":"negative")+"\\">'` |
| **分析** | class 属性值中多了空格和提前闭合的引号，实际渲染可能为 `class="pos-profit positive""` |
| **修复建议** | 改为 `h += '<td class="pos-profit '+(pnl>=0?'positive':'negative')+'">'` |

---

### Bug #7: renderOrders() class 属性同样错位
| 项目 | 详情 |
|------|------|
| **来源** | gen_brokers.py 第575行 |
| **影响** | 所有券商页面的委托列表 |
| **问题代码** | `h += '<div class="order-header"><span class="order-type "\'+o.side+\'">'` |
| **分析** | 与 Bug #6 相同的引号/空格错误模式 |
| **修复建议** | 同上，修正引号嵌套 |

---

## 🟠 信息性发现（3个）

### 发现 #8: insurance-picc.html 缺失原因已确认
- gen_insurance.py 的 companies 字典中**确实定义了 picc**（中国人民保险）
- 循环生成逻辑（第566-571行）会为所有 key 生成对应的 HTML 文件
- 文件缺失原因：生成脚本未执行或执行后被手动删除
- 建议：重新运行 `python gen_insurance.py` 生成缺失文件

### 发现 #9: gen_p2p.py 函数名 typo 有事后修复
- 第417行先写了错误的函数名 `function doInstall(idx)`
- 第484行通过 `html.replace('function doInstall(idx)', 'function doInvest(idx)')` 修正
- 修复本身有效，但代码维护性差，建议直接写正确名称

### 发现 #10: STORAGE_KEY 一致性确认 ✓
| 文件 | STORAGE_KEY | 状态 |
|------|------------|------|
| invest-sim.html 第2561行 | `investSimState_v13` | ✓ |
| gen_brokers.py | `investSimState_v13` | ✓ |
| gen_p2p.py 第223行 | `investSimState_v13` | ✓ |
| gen_insurance.py 第228行 | `investSimState_v13` | ✓ |
| 全部7个HTML子页面 | `investSimState_v13` | ✓ |

---

## ✅ 确认正常项

### 数据结构一致性 ✓
invest-sim.html loadState()（第2761-2764行）正确恢复：
- `brokerAccounts` ←→ 子页面 getBrokerData()/saveBrokerData()
- `p2pInvestments` ←← 子页面 getP2PData()/saveP2PData()  
- `insurancePolicies` ←→ 子页面 getInsData()/saveInsData()

字段名在读写两端完全匹配。

### 函数签名一致性 ✓
- `processP2P()` (invest-sim.html 第8123行): 处理回款计划，违约概率与子平台配置一致
- `processInsurance()` (invest-sim.html 第8200行): 处理续期扣费和理赔
- P2P 违约概率配置: lufax=0.03, ppdai=0.08, renrendai=0.05（与各平台 HTML 定义一致）

### avgCost 计算公式 ✓
gen_brokers.py 第421行非数组分支的公式数学上等价于加权平均成本：
```
asset.avgCost = oldTotal / asset.amount + price * qty / asset.amount;
```
等价于 `(oldTotal + price * qty) / (asset.amount + qty)` 在 amount 更新后的形式。虽然写法不够直观，但逻辑正确。

---

## 总结统计

| 严重程度 | 数量 | 影响范围 |
|---------|------|---------|
| 🔴 严重 | 4 | 功能失效/页面无法打开 |
| 🟡 中等 | 3 | 显示异常 |
| 🟠 信息性 | 3 | 维护建议 |
| ✅ 正常 | - | STORAGE_KEY、数据结构、函数签名均一致 |

**优先修复顺序**: Bug #3 > Bug #1 > Bug #2 > Bug #4 > Bug #5 > Bug #6/#7

---

*报告生成时间: 2026-06-06*
*审查人: Explore-3*
