# Apple Reminders — integration rules

The EA reads and writes B's Apple Reminders via a self-hosted MCP server (a private fork of Dhravya/apple-mcp). Used primarily by the `daily-planning` skill, and on demand whenever B wants to capture a task mid-session.

## Where the code lives

| | |
|---|---|
| Fork | `jBellree/apple-mcp` (private, detached from upstream network) |
| Local clone | `~/code/apple-mcp/` (outside Dropbox to avoid syncing `node_modules`) |
| Runtime | Bun at `~/.bun/bin/bun` |
| Registered with | `claude mcp add apple-mcp --scope user` (user scope, all sessions) |
| Tools exposed | Reminders, Calendar, Notes, Contacts, Messages, Mail, Maps |

All handlers are kept intact. EA currently only calls Reminders tools; other handlers stay dormant until B asks for them, at which point macOS prompts for the relevant Automation permission on first use.

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

If apple-mcp stops working — a dep has a CVE, macOS changes break AppleScript, the server won't start, whatever — tell Claude in this repo:

> update apple-mcp — [reason]

Claude then reads the code at `~/code/apple-mcp/`, proposes a fix as a diff, you review and approve, Claude commits to the fork on GitHub. Pull from the other Mac when the fix is in.

## Per-machine setup (e.g. adding the MacMini)

```
curl -fsSL https://bun.sh/install | bash        # if Bun not present
mkdir -p ~/code && cd ~/code
git clone git@github.com:jBellree/apple-mcp.git
cd apple-mcp && bun install
claude mcp add apple-mcp --scope user -- /Users/<user>/.bun/bin/bun run /Users/<user>/code/apple-mcp/index.ts
```

Each Mac needs its own macOS Automation permission grant. First tool call prompts; manual fallback is **System Settings → Privacy & Security → Automation → (terminal app or Claude Code) → enable Reminders**.

Reminders content itself syncs via iCloud, so both machines see the same data regardless of which one the server is running on.
