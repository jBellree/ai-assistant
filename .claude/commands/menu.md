---
description: List every available slash command in this workspace
---

List every slash command available in this EA workspace.

Use the Glob tool to find `.claude/commands/*.md` (relative to the current working directory). For each file:

1. Read its frontmatter `description` field.
2. Output one line: `/<name> — <description>`.

Sort alphabetically by command name. Group nothing — just a flat list. Keep it scannable — no preamble, no trailing summary. Just the list.

If a command file has no `description` in frontmatter, output `/<name> — (no description)`.
