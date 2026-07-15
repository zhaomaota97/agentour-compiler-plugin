# 完整示例：从零创建「麦当劳出餐核查员」

## Step 1: 描述想法

用户对 Compiler 说：
> 我想做一个麦当劳出餐核查 agent。输入订单号，自动查订单详情、拍托盘照片、逐项比对、发现漏放错放就上报。

## Step 2: Brainstorm 探索

输出领域简报：
- 核心工作流：收到订单号 → 拉订单 → 拍托盘 → 比对 → 有差异则上报
- 边缘情况：备注执行（去冰/无洋葱）、配件齐全（吸管/纸巾/蘸酱）
- 决策点：上报需要值班经理确认
- 外部系统：摄像头（mock）、POS 订单系统（mock）

## Step 3: Compiler 生成

基于模板自动生成：

```
packages/mcd-meal-checker/
├── agentour.json
│   └── id: mcd-meal-checker, name: 麦当劳出餐核查员, pricing: 10 积分
├── tests/smoke.yaml
└── payload/agent/
    ├── agent.ts         → templates/agent.ts（不改）
    ├── sandbox.ts       → templates/sandbox.ts（不改）
    ├── instructions.md  → UX 约束模板 + 出餐核查角色
    ├── tools/
    │   ├── scan_order.ts        → 模式 1: 查订单
    │   ├── capture_tray.ts      → 模式 1: 拍托盘（mock）
    │   ├── check_completeness.ts → 模式 2: 比对
    │   ├── report_violation.ts  → 模式 3: 上报（审批）
    │   └── report_pass.ts       → 模式 1: 记录通过
    └── skills/
        └── mcd-checklist.md → 配件对照表（ASCII 文件名）
```

## Step 4: 生成锁文件

```bash
cd packages/mcd-meal-checker/payload
pnpm install --lockfile-only
```

## Step 5: 本地验证

```bash
# 快速验证静态 gate
core/.venv/bin/python -m agentourcore publish packages/mcd-meal-checker --skip-dynamic
# ✅ structure, manifest, secrets, approval_declared, deps_locked, smoke_spec

# 全量（含 build + 冒烟）
core/.venv/bin/python -m agentourcore publish packages/mcd-meal-checker
# ✅ 全部 10 道 gate 通过
```

## Step 6: 上架

编译完成后在控制台「发现」页可以看到并试用。
