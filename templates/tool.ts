// Agentour Platform — tool template (data query / computation)
// Replace TOOL_NAME, TOOL_DESCRIPTION, and the Zod schema + execute logic.
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "TOOL_DESCRIPTION",
  inputSchema: z.object({
    // Define your input fields here, e.g.:
    // query: z.string().min(1).describe("The search query"),
  }),
  async execute(input) {
    // Implement deterministic logic here.
    // Do NOT call any LLM inside a tool — tools are pure code.
    return { result: "mock", input };
  },
});
