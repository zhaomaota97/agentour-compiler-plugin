# Tool 设计模式

## 模式 1: 数据查询（Query & Return）

```ts
// 输入一个标识符，查询数据并返回结果
export default defineTool({
  description: "根据订单号查询订单详情",
  inputSchema: z.object({ order_id: z.string() }),
  async execute({ order_id }) {
    const order = lookupOrder(order_id);
    return { found: !!order, order };
  },
});
```

## 模式 2: 逐项比对（Compare & Flag）

```ts
// 对比两份数据，标记差异项
export default defineTool({
  description: "比对订单与托盘实物",
  inputSchema: z.object({
    order_items: z.array(z.object({ sku: z.string(), qty: z.number() })),
    actual_items: z.array(z.object({ sku: z.string(), qty: z.number() })),
  }),
  async execute({ order_items, actual_items }) {
    const issues = [];
    for (const oi of order_items) {
      const actual = actual_items.find(a => a.sku === oi.sku);
      if (!actual || actual.qty !== oi.qty)
        issues.push({ sku: oi.sku, expected: oi.qty, actual: actual?.qty || 0 });
    }
    return { passed: issues.length === 0, issues };
  },
});
```

## 模式 3: 上报/审批（Report + Approve）

```ts
// 副作用操作，需要人工确认
import { always } from "eve/tools/approval";

export default defineTool({
  description: "将违规项上报给值班经理",
  inputSchema: z.object({
    order_id: z.string(),
    violations: z.array(z.object({ type: z.string(), detail: z.string() })),
  }),
  approval: always(),
  async execute({ order_id, violations }) {
    return { reported: true, order_id, count: violations.length };
  },
});
```

## 模式 4: 批处理（Batch + Summary）

```ts
// 对一批数据逐条处理，返回汇总
export default defineTool({
  description: "对多条合同条款逐条打分，返回汇总",
  inputSchema: z.object({
    clauses: z.array(z.object({ id: z.string(), text: z.string() })),
  }),
  async execute({ clauses }) {
    const results = clauses.map(c => ({
      id: c.id,
      score: scoreClause(c.text), // deterministic scoring
      risks: findRisks(c.text),
    }));
    return { total: clauses.length, results, avg_score: avg(results.map(r => r.score)) };
  },
});
```

## 模式 5: 清单核验（Checklist + Record）

```ts
// 按预定义清单逐项检查
const CHECKLIST = ["灭火器", "消火栓", "烟感报警", "应急照明", "安全出口"];

export default defineTool({
  description: "开始消防巡检，加载检查清单",
  inputSchema: z.object({ area: z.string() }),
  async execute({ area }) {
    return { area, checklist: CHECKLIST, items_total: CHECKLIST.length };
  },
});
```

## 原则

- 工具是确定性代码，不调 LLM
- 每个工具做一件事
- 输入/输出用 Zod 类型化
- 审批工具用 `approval: always()` 并在 berth.json 声明
