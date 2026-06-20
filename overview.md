# invest-sim.html V5 修复总结

## 问题
页面内容区域完全空白，控制台报错：
```
TypeError: Cannot read properties of undefined (reading '0')
    at renderAssets (invest-sim.html:1540)
```

## 根因
构造函数执行顺序问题：
1. `this.resetAssets()` 正确初始化 `priceHistory`（为每个资产写入初始价格数组）
2. 但紧接着构造函数第 924 行执行 `this.priceHistory = {}`，**把已初始化的数据清空为空对象**
3. `init()` → `renderAssets()` 访问 `this.priceHistory[asset.id][0]` 时崩溃

## 修改
1. **删除构造函数中多余的 `this.priceHistory = {}`** —— `resetAssets()` 已负责初始化
2. **renderAssets 第 1540 行加防御** —— `(this.priceHistory[asset.id] && this.priceHistory[asset.id][0]) || asset.price`
3. **simulateRound 价格历史记录加防御** —— 如果 `priceHistory[asset.id]` 缺失，自动初始化新数组

## 验证
- JS 语法校验通过（node -c）
- 修复后刷新页面即可正常渲染资产卡片、雷达图和交易日志
