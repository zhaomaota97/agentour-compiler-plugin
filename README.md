# Agentour Compiler Plugin for Claude Code

Full-auto Claude Code Plugin for inventing new Agentour Agents or reconstructing existing Agent projects with high behavioral fidelity.

## Install

```text
/plugin marketplace add agentour-platform https://github.com/Onesyn-ai/agentour-claudecode-plugin
/plugin install agentour-compiler@agentour-platform
```

At startup the Plugin checks the Marketplace version and installs a newer release automatically. Restart Claude Code after an upgrade so the new Plugin code is loaded. Model discovery probes every platform model and filters failed models before Agent generation.

Start a new Claude Code session, then run:

```text
/agentour-compiler
```

## Workflow

The Plugin strictly asks one question or one choice per turn:

1. Choose **测试服** (`https://test.agentour.ai`) or **正式服** (`https://agentour.ai`).
2. Enter a `at_` developer token; it is validated with `GET /v1/dev/me` and never written to files.
3. The Plugin fetches enabled models from `GET /v1/models`.
4. Choose existing-Agent reconstruction or new-Agent invention.
5. Internal brainstorm and grill-me agents conduct a multi-round, one-question interview.
6. The Plugin generates Package(s), validates, repairs, and verifies fidelity.
7. Choose private or public upload, run the remote Build Gate, then publish only after it succeeds.

If a source repository contains multiple Agents, the Plugin inventories them and asks whether to merge all into one Package, convert all separately, or select a subset.

A successful build is not considered proof of equivalence. Critical workflow, tool, approval, attachment, schema, or artefact mismatches block publication.

## Remote Build behavior

`remote-build` prints state changes and structured Gate results. A cached result reuses the
same Package hash without consuming a new E2B quota. HTTP `429` means the developer's active
or daily Build quota is exhausted; wait for the stated window instead of retrying unchanged
content. Deterministic Gate failures must be repaired before retrying. Cancel a no-longer-needed
job with `cancel-build <job-id>`; cancellation and timeout always produce a non-zero result.
Interrupted observation can be continued with `track-build <job-id>` without creating or charging
a replacement Build.
