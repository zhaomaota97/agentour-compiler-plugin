# 版本管理

## 语义化版本

Berth 使用语义化版本号（x.y.z）：

- **主版本 (x)**: Agent 核心流程或输出格式有重大变更时升级
- **次版本 (y)**: 新增工具或功能，或改进现有工具时升级
- **修订号 (z)**: 修正 bug、优化提示词、调整参数时升级

## 版本不可变

一旦发布到 Registry，同一版本号不可覆盖。修改后必须升级版本号再发布。升级只需修改 `berth.json` 中的 `version` 字段。

## RELEASE.md 模板

```markdown
# v0.2.0 — 新增报价对比功能

## 新增
- 新增 `compare_quotes` 工具：支持多份报价横向对比
- 新增 `export_report` 工具：一键导出审查报告

## 改进
- `score_clause` 工具新增 3 种风险模式的检测
- `instructions.md` 优化了 Markdown 表格输出格式

## 修复
- 修复空输入时工具调用超时的问题
```

## 发布流程

1. 修改代码
2. 更新 RELEASE.md
3. 升级 berth.json 的 version
4. 重新生成 pnpm-lock.yaml
5. 发布 `core/.venv/bin/python -m berthcore publish packages/<id>`
