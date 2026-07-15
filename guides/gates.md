# 质检闸门 — 常见失败与修复

上传后按顺序执行，全绿才入库。

| 闸门 | 检查内容 | 常见失败 | 修复方法 |
|---|---|---|---|
| structure | 目录结构、必备文件 | 缺少 agentour.json / instructions.md / README.md | 补全文件 |
| manifest | agentour.json 字段合法性 | id 格式错、缺少 examples、价格为负 | 检查字段格式 |
| secrets | 密钥不进包 | 代码中出现 sk- 前缀或密钥明文 | 删除密钥，改用平台 LLM |
| approval_declared | 审批声明与实现双向一致 | 声明了但工具未配 `approval: always()` | 工具加 `approval: always()` |
| deps_locked | pnpm-lock.yaml 存在 | 未运行 `pnpm install --lockfile-only` | payload 内运行生成锁文件 |
| smoke_spec | smoke.yaml 用例合法 | 声明审批工具但无 expect_approval 用例 | 加一条审批用例 |
| build | payload 可编译起服 | skill 文件名含中文；缺 modelContextWindowTokens | 改名 ASCII；加声明 |
| smoke | 冒烟用例真跑通过 | 指令语气不够强致模型未调工具 | 收紧 instructions |
| ownership | 包 ID 归属核验 | 同一 ID 已被其他开发者占用 | 换 ID |
| registry | 版本不可变核验 | 同版本号重复发布 | 升版本号 |

## 调试技巧

1. 首次发布经常因 `pnpm install` 超时失败——原样重发一次即可（平台自愈）
2. smoke 失败时看日志里的工具调用记录，确认模型是否调了预期的工具
3. `--skip-dynamic` 跳过 build + smoke，调试静态 gate 时更快
