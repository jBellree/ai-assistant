# Apple Reminders — integration rules

The EA reads and writes B's Apple Reminders via a self-hosted MCP server (`jBellree/apple-mcp`, private fork, running locally via Bun). Used primarily by the `daily-planning` skill, and on demand whenever B wants to capture a task mid-session.

## Scope and defaults

- **Reads:** all Reminders lists. EA sees everything B has.
- **Writes target:** back into Apple Reminders. Single source of truth.
- **Default list on write:** if B doesn't specify, **ask which list** rather than guessing. Don't silently pick the system default.
- **Default due date:** today, unless B specifies otherwise.

## Write pattern — confirm before commit

Mirror the Airtable write rule. Before any create / update / complete / delete, show B the proposed change and wait for "yes", "go", or "ok". Never silently write.

> I'm about to add a reminder to the **DSG** list:
> - Title: Call Dealer X re: payout status
> - Due: today (17 Apr, 14:00)
> - Notes: (none)
> Confirm?

For batch writes (e.g. ticking off 5 completed reminders at end-of-day), preview the full batch in one block before committing the batch.

## When things break

If apple-mcp stops working, say "update apple-mcp — [reason]". Claude reads `~/code/apple-mcp/`, proposes a fix, commits to the fork. Setup instructions for new machines: see `reference_apple_mcp.md` in memory.
