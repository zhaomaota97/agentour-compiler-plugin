# Agent 迁移指南

## 从任何框架迁移到 Berth

无论你的 agent 是 Claude Code、LangChain、自研框架还是 Python 脚本，迁移流程一致：

### Step 1: 识别内核 vs 外壳

**内核（保留）：**
- 提示词文案（角色、语气、固定话术）
- 业务规则（检查清单、阈值、评分标准）
- 工具逻辑（算法、校验公式、比对流程）
- 领域知识（SOP、行业标准、合规要求）

**外壳（丢弃）：**
- CLI / HTTP 路由 / 传输协议
- 自制的模型循环（eval + 工具路由 + 循环逻辑）
- 离线/降级分支（无密钥时的兜底方案）
- 加密/解密逻辑（密钥管理由平台负责）

### Step 2: 提取到 Berth 结构

| 原项目中的... | 迁移到 |
|---|---|
| 系统提示词（不含工具描述） | `instructions.md` |
| 工具函数 | `tools/<name>.ts` |
| 业务规则清单、SOP | `skills/<name>.md` |
| 对外操作（发送/提交/支付） | `tools/<name>.ts` + `approval: always()` |
| 环境变量/密钥 | `berth.json` 的 `secrets` 数组 |

### Step 3: 适配平台规范

- 模型调用: 用 `@ai-sdk/deepseek` + 平台端点（见 `templates/agent.ts`）
- 工具定义: 用 Zod schema + 确定性逻辑
- 副作用: 加 `approval: always()` + 在 berth.json 声明
- 输入/输出: 短输入（订单号/ID），Markdown 表格输出

### Step 4: 验证与发布

```bash
pnpm install --lockfile-only
core/.venv/bin/python -m berthcore publish packages/<id>
```

按 gate 报告修复，直到全绿。

## 常见迁移失败

- **smoke 失败**: 原提示词太发散 → 收紧 instructions，加"必须调 X 工具"
- **build 失败**: skill 文件名含中文 → 改为 ASCII
- **approval_declared**: 声明了但工具没配 `approval: always()` → 补配
