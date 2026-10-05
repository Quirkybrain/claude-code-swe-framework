// OpenCode V2 adapter for the framework's existing Claude Code guard scripts.
// The scripts remain the authority for handoff and frozen-input checks.

const specialists = new Set([
  "asset-analyst", "requirements-analyst", "system-modeler",
  "solution-architect", "experience-designer", "delivery-planner",
  "implementation-engineer", "test-engineer", "quality-reviewer",
  "integration-engineer", "debug-specialist", "system-verifier",
  "technical-writer", "release-engineer", "repository-manager",
])

async function check(root, script, payload) {
  const proc = Bun.spawn(["python3", `${root}/.claude/hooks/${script}`], {
    cwd: root,
    stdin: new Blob([JSON.stringify(payload)]),
    stdout: "pipe",
    stderr: "pipe",
  })
  const [code, stderr] = await Promise.all([proc.exited, new Response(proc.stderr).text()])
  if (code !== 0) throw new Error(stderr.trim() || `${script} blocked the tool call`)
}

function patchPaths(patch) {
  return [...patch.matchAll(/^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$/gm)].map((match) => match[1])
}

export default {
  id: "swe-guards",
  async setup(ctx) {
    const root = ctx.location.project.canonical
    await ctx.tool.hook("execute.before", async (event) => {
      const input = event.input ?? {}
      if (event.tool === "subagent") {
        const role = input.agent
        if (!specialists.has(role)) return
        await check(root, "check-agent-handoff.py", {
          tool_name: "Agent",
          tool_input: { subagent_type: role, prompt: input.prompt },
          cwd: root,
        })
        return
      }

      const directEdit = event.tool === "write" || event.tool === "edit"
      const paths = directEdit
        ? [input.filePath ?? input.file_path ?? input.path].filter(Boolean)
        : event.tool === "apply_patch" && typeof input.patchText === "string"
          ? patchPaths(input.patchText)
          : []
      for (const filePath of paths) {
        await check(root, "check-frozen-input.py", {
          tool_name: "Write",
          tool_input: { file_path: filePath },
          cwd: root,
        })
        // The existing producer hook checks whole Write contents and Edit additions.
        // For patches, the artifact gate still validates the resulting file.
        if (directEdit) {
          await check(root, "check-artifact-producer.py", {
            tool_name: event.tool === "write" ? "Write" : "Edit",
            tool_input: {
              file_path: filePath,
              content: input.content,
              new_string: input.newString ?? input.new_string,
            },
            cwd: root,
          })
        }
      }
    })
  },
}
