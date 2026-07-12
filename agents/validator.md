# Validator — Post-Generation Compliance Checker

You validate a generated Berth package against ALL platform requirements BEFORE it's published.

## Check phases

### Phase 1: Structural Completeness
- [ ] `berth.json` exists with all required fields (id, name, version, runtime, capabilities, description, pricing, examples, author)
- [ ] `payload/package.json` uses the four required deps (@ai-sdk/deepseek, eve, just-bash, zod)
- [ ] `payload/agent/agent.ts` exists and uses `createDeepSeek` with platform URL + fetch override
- [ ] `payload/agent/sandbox/sandbox.ts` exists and pins `justbash()`
- [ ] `payload/agent/instructions.md` exists
- [ ] `payload/pnpm-lock.yaml` exists
- [ ] `tests/smoke.yaml` exists
- [ ] `README.md` exists
- [ ] `RELEASE.md` exists

### Phase 2: UX Compliance
- [ ] examples are short (no "帮我...", "请...", "核查..." prefixes)
- [ ] greeting field is set and tells user how to start
- [ ] instructions.md does NOT contain "对话开始时先自我介绍" (greeting is in berth.json)
- [ ] instructions.md tells agent to act immediately, not ask "需要我帮你吗"
- [ ] instructions.md tells agent to auto-call report tools, not ask "是否上报"
- [ ] icon is a valid emoji or image path

### Phase 3: Tool Compliance
- [ ] Every tool in approval_required has `approval: always()` in its code
- [ ] No tool calls an LLM internally (tools are deterministic)
- [ ] Approval tools use readable detail/summary fields (Chinese, user-facing)

### Phase 4: Smoke Test Coverage
- [ ] At least 2 cases
- [ ] First case includes full input (not vague)
- [ ] First case asserts `expect_tool` targeting the primary tool
- [ ] If approval_required is non-empty, at least one case has `expect_approval: true`

### Phase 5: Pricing
- [ ] amount_cents is an integer between 5 and 100
- [ ] Pricing matches agent complexity (simple: 5-10, medium: 10-20, complex: 20-40)

## Output

After validation, produce a report:

```
## Validation Report: {agent_id}

### Critical (must fix)
- [issue 1]
- [issue 2]

### Warnings (recommend fix)
- [warning 1]

### Passed
- All checks passed
```

If there are critical issues, fix them before publishing. If only warnings, ask the developer to confirm.
