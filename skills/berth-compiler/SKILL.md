---
user-invocable: true
name: berth-compiler
description: Fully automatic Berth Agent compiler. Selects local or competition platform, validates the developer token, discovers models, then invents a new Agent or reconstructs existing Agent projects through strict one-question-per-turn brainstorm and grill-me interviews, fidelity verification, validation, and private/public upload.
---

# Berth Compiler

Run the entire process. The user must never coordinate phases, agents, validators, commands, or retries.

## Iron rule: one decision per turn

Each conversational turn may ask exactly one question or offer exactly one choice.

- Never bundle questions in bullets, numbered fields, or paragraphs.
- Never ask for three examples in one turn; collect them across turns.
- A multi-option choice must resolve one decision only.
- After every answer, update the spec/state and ask the single next highest-value question.
- Continue all unblocked inspection, generation, testing, and repair between questions.

## Fixed platform targets

| Choice | Platform | URL |
|---|---|---|
| A | 本地服 | `http://127.0.0.1:8600` |
| B | 比赛服 | `http://61.29.254.146` |

Never ask the user to type or configure a URL.

## Mandatory sequence

Persist non-secret progress in `.berth/compiler-state.json`. Never persist the token.

### 1. Choose platform

The first unresolved message must ask only:

> 请选择发布平台：A. 本地服；B. 比赛服。

### 2. Validate developer token

The next message asks only for that platform's `bt_` token and states that it will not be saved.

```bash
BERTH_TOKEN="<token>" python3 "${CLAUDE_PLUGIN_ROOT}/scripts/berth_api.py" \
  --platform <local|competition> verify-token
```

Use `GET /v1/dev/me`. If invalid, ask only for a corrected token after the user checks the selected platform's console. Never print, save, commit, or report the token.

### 3. Discover models

After successful token validation, automatically call:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/berth_api.py" \
  --platform <local|competition> models
```

Choose an enabled model based on complexity, risk, context, and cost. Ask a model choice only when the tradeoff is material, and ask nothing else that turn.

### 4. Choose source

Ask only:

> 这次是：A. 重构已有 Agent；B. 从零发明一个 Agent？

## Existing Agent path

Inspect the repository before asking discoverable facts. Inventory every Agent, entrypoint, prompt, Skill, Tool, MCP server, sub-agent, workflow, router, test, example, dependency, environment variable, external service, file/attachment behavior, approval, artefact, retry, and failure path.

If multiple Agents exist, ask only:

> 检测到多个 Agent。你希望：A. 合成一个 Agent；B. 分别转换并上传全部 Agent；C. 只转换其中一部分？

- If C, the next turn asks only which Agents to include; multi-select is allowed as one scope choice.
- If A, preserve all source roles, routing, orchestration, tools, and boundaries in one Package.
- If B, create one Package and fidelity report per Agent.

Create `.berth/conversion-inventory.json`, `.berth/conversion-map.json`, and `.berth/fidelity-report.json`. Record every capability as preserved, adapted, reimplemented, degraded, unsupported, or explicitly authorized removed.

Use the `brainstorm` and `grill-me` agents internally to challenge uncertain business behavior. Do not require the user to invoke them.

## New Agent path

Create `AGENT_SPEC.md` immediately, then dispatch `brainstorm` and `grill-me` internally. Collect exactly one unresolved fact per user turn across domain, job, user, error impact, inputs, outputs, workflow, missing data, ambiguity, tools, model judgment, integrations, secrets, approvals, SOPs, edge cases, forbidden actions, runtime labels, pricing, identity, and examples.

Do not generate until the intended workflow is precise. When the original request already authorizes creation, do not ask a separate “start coding” question.

## Generate Package(s)

Use `templates/` and the relevant guides. Each Package must contain `berth.json`, consumer README, release notes, Smoke Tests, lockfile, Eve runtime entrypoint, instructions, pinned sandbox, deterministic tools, and domain knowledge.

Preserve source flow, tool contracts, approvals, attachments, schemas, artefacts, failure/retry behavior, and user-visible interactions. Every loaded capability needs business-readable `runtime_ui` text. Never expose `load skill`; `waiting_approval` is waiting, not running.

## Validate and repair automatically

Dispatch `validator`, generate the lockfile, build, run Smoke Tests, source tests, and relevant project tests. Fix failures narrowly and repeat until green or genuinely blocked. Never weaken valid tests or hand the validator report to the user as homework.

## Fidelity requirement

For reconstruction, create same-case comparisons from tests, examples, sanitized real cases, prompts, and workflows. Compare workflow/routing, tools/arguments, approvals, files/attachments, schemas, artefacts, normal/boundary/failure/retry/multi-turn behavior, semantic result, latency, and resources.

Bind the fidelity report to the final Package SHA-256. Any critical workflow, tool, approval, attachment, schema, or artefact mismatch blocks upload regardless of score. Repair and rerun until fidelity is as high as technically possible; disclose remaining degradation.

## Choose visibility

After validation and fidelity pass, ask only:

> 请选择上传方式：A. 私有；B. 公开（需要平台审核）。

For multiple Packages, first ask whether one setting applies to all or should be selected one by one. If one by one, ask one Package per turn.

## Upload

Revalidate the token immediately before upload. Present one compact summary of platform, IDs, versions, models, visibility, validation, fidelity, and limitations. If upload was requested, proceed; otherwise ask one final upload confirmation.

```bash
BERTH_TOKEN="<token>" python3 "${CLAUDE_PLUGIN_ROOT}/scripts/berth_api.py" \
  --platform <local|competition> publish-async packages/<agent-id> \
  --visibility <private|public>
```

Follow every job. On Gate failure, fix, bump the version when needed, rebuild fidelity evidence, and retry. Finish with final platform status and Package identifiers.

## Resources

- `agents/brainstorm.md` — one-question domain exploration
- `agents/grill-me.md` — one-question ambiguity elimination
- `agents/validator.md` — automatic Package and fidelity validation
- `guides/migration.md` — migration patterns
- `guides/gates.md` — Gate repair
- `guides/ux-checklist.md` — user experience requirements
- `guides/tool-patterns.md` — deterministic and approval tools
- `templates/` — Package templates
