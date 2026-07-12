# 本地测试与调试

## 快速验证

```bash
# 只跑静态 gate（结构/清单/密钥/审批声明/依赖/冒烟），跳过 build + smoke
core/.venv/bin/python -m berthcore publish packages/<agent-id> --skip-dynamic
```

## 全量发布

```bash
core/.venv/bin/python -m berthcore publish packages/<agent-id>
```

## 常见失败与调试

### deps_locked 失败
```bash
cd packages/<agent-id>/payload
pnpm install --lockfile-only
```

### build 失败
```bash
cd packages/<agent-id>/payload
pnpm exec eve build
# 检查输出，常见原因：
# - skill 文件名含中文
# - agent.ts 缺少 modelContextWindowTokens
```

### smoke 失败
- 检查 `tests/smoke.yaml` 的 expect_tool 是否匹配实际工具名
- 检查 instructions.md 语气是否足够强（"必须调" 而不是 "可以调"）
- 审批工具必须有 expect_approval 用例

### secrets 失败
- 代码中不能出现任何 `sk-` 或 `AKIA` 前缀的字符串
- LLM 密钥由平台提供，不在 berth.json 的 secrets 里声明

## 调试技巧

1. **看 gate 报告**: 每个失败门都给出 file:line 级原因
2. **看 build log**: `payload/.berth-build.log`
3. **看 server log**: `~/.berth/eve/<agent-id>/.berth-server.log`
4. **重发即可**: pnpm install 超时/中断后直接重发（平台按时间戳判断是否需重装）

## 冒烟测试用例写法

```yaml
cases:
  - send: "具体的用户输入"              # 信息要完整
    expect_tool: tool_name               # 预期被调的工具
    expect_contains: "必定出现的词"       # 可选，选确定性词汇
  - send: "请直接调用 report_xxx 上报…"  # 审批用例
    expect_approval: true
```

- 第一条用例信息必须给全
- expect_tool 比 expect_contains 更可靠
- expect_contains 选工具输出中必定回显的词
