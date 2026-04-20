---
description: Show today's Apple Reminders grouped — overdue, due today, tomorrow, week, flagged
---

Pull B's current incomplete Apple Reminders and show them grouped.

**Preferred path:** use the `mcp__apple-mcp__reminders` tool with `operation: "list"` if it's available in this session.

**Fallback if MCP tool is missing or returns empty:** shell out to the Swift helper directly via Bash:
```
~/code/apple-mcp/bin/reminders-helper list-reminders --completed incomplete
```
The helper outputs a JSON array. Parse it.

**Grouping (UK timezone, today = local date):**

- **Overdue** — any reminder with a `dueDate` before today's date
- **Due today** — `dueDate` matches today's date
- **Due tomorrow** — `dueDate` matches tomorrow
- **Rest of this week** — `dueDate` within the next 7 days after tomorrow
- **Flagged (no due date)** — `priority > 0` and `dueDate` is null

Within each group, sort by `listName` then reminder name.

**Output format** — use markdown headings per group and a bulleted list per item:
```
## <Group name> (<count>)
- [<listName>] <name> — <short date like Fri 17 Apr>
```

Skip empty groups entirely. Start the response with a one-line header: `<weekday> <date> <month> <year>. N incomplete reminders total.`

If a reminder has `priority > 0`, append `[flagged]` at the end of its line. Don't include body/notes or ID fields — keep it scannable.

Do not mark anything complete, create anything, or modify anything. This is read-only.
