# UX 约束检查清单

发布前逐项确认：

## instructions.md
- [ ] 第一句说明 Agent 角色，不给模型反问空间
- [ ] 工作方式：收到输入 → 调工具 → 输出结果，一气呵成
- [ ] 对上报工具用强制语气："发现问题后立即调 X，不要问'是否上报'"
- [ ] 输出结构用 Markdown 模板固定（表格列、清单）
- [ ] 信息不全时必须向用户提问补齐，不得猜测或编造数据。追问需明确列出缺少哪些信息
- [ ] 不包含"对话开始时先自我介绍"（greeting 在 berth.json 里）

## berth.json
- [ ] examples ≥ 2 条，第一条信息给全，可独立运行
- [ ] examples 是短输入（订单号/ID），不含"帮我..."冗余前缀
- [ ] greeting 字段有值，用一句话告诉用户怎么开始
- [ ] icon 使用合适的行业 emoji
- [ ] pricing 在建议范围内（5-40 积分）
- [ ] approval_required 列出的每个工具都配了 `approval: always()`

## tools
- [ ] 每个工具有清晰的 description（控制在模型理解范围内）
- [ ] 确定性逻辑，不调 LLM
- [ ] 审批工具使用 `approval: always()` 并 `import { always } from "eve/tools/approval"`
- [ ] 上报工具的 detail 字段是用户可读的中文描述

## smoke.yaml
- [ ] 第一条用例信息给全，断言 expect_tool
- [ ] 有审批工具的必须有 expect_approval 用例
