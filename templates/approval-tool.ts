// Berth Platform — approval tool template (side-effect actions)
// Use this for tools that send reports, create tickets, dispatch orders, etc.
import { defineTool } from "eve/tools";
import { always } from "eve/tools/approval";
import { z } from "zod";

export default defineTool({
  description: "TOOL_DESCRIPTION",
  inputSchema: z.object({
    summary: z.string().describe("Summary shown on the approval card"),
    detail: z.string().optional().describe("Additional context"),
  }),
  // always() means this tool ALWAYS requires human approval before executing.
  // The platform shows an approval card; user clicks Approve/Deny.
  approval: always(),
  async execute({ summary, detail }) {
    // In production: call external API, send email, create ticket, etc.
    // For the package: return a mock result — the smoke test auto-denies.
    return { sent: true, summary };
  },
});
