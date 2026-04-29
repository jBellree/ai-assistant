---
description: Show and manage B's Apple Reminders — slice by category, mark items done
---

Show B's Apple Reminders, conversationally. Don't dump everything by default.

## Step 1 — figure out the slice

If `$ARGUMENTS` is non-empty, parse it loosely and skip straight to Step 2:

- `overdue` / `late` / `1` → **Overdue**
- `today` / `2` → **Due today**
- `week` / `this week` / `3` → **Due this week** (today + 7d)
- `flagged` / `starred` / `4` → **Flagged, no due date**
- `list <name>` / `show me <name>` / `<name>` that matches a list → **One list**
- `everything` / `all` / `dump` / `6` → **Everything incomplete** (full grouped view)

If `$ARGUMENTS` is empty OR ambiguous, respond with the menu below and stop. Do not fetch anything yet.

```
Which reminders do you want to see?
  1. Overdue
  2. Due today
  3. Due this week (next 7 days)
  4. Flagged with no due date
  5. One specific list — tell me the list name
  6. Everything incomplete (full grouped dump)
```

Wait for B's reply, then continue with Step 2.

## Step 2 — fetch the slice

All fetches go through one wrapper script: `.claude/scripts/reminders-slice.sh`. It calls the Swift helper at `~/code/apple-mcp/bin/reminders-helper`, projects the fields B cares about (`id,name,listName,dueDate,priority`), and handles the UK-local date filtering. `id` is kept so Step 3 (mark items done) can reference reminders without a re-fetch — **do not render it in the output**, but remember it for the rest of the turn.

The script is allowlisted in `.claude/settings.json`, so fetches don't prompt. It emits JSON on stdout; keep the output in a Bash tool call and let Claude read it directly.

### Invocations

```bash
.claude/scripts/reminders-slice.sh overdue
.claude/scripts/reminders-slice.sh today
.claude/scripts/reminders-slice.sh week
.claude/scripts/reminders-slice.sh flagged
.claude/scripts/reminders-slice.sh list "<list name>"
.claude/scripts/reminders-slice.sh lists                # list names only (for fuzzy-matching step 5)
.claude/scripts/reminders-slice.sh everything
```

### One specific list (option 5)

First resolve the list name. If B's input doesn't match a real list exactly, list the names with `.claude/scripts/reminders-slice.sh lists` and fuzzy-match. Then fetch with `.claude/scripts/reminders-slice.sh list "<matched name>"`. If no match, show B the list names and re-ask.

### Everything (option 6)

Run `.claude/scripts/reminders-slice.sh everything`, then group the output into **Overdue / Due today / Due tomorrow / Rest of this week / Flagged (no due date)** using the UK-local date conversion (the script's projected output still carries the raw UTC `dueDate` for Claude to band). Skip empty groups.

## Output format

- One-line header: `<weekday> <date> <month> <year>. <N> <slice label>.` e.g. `Saturday 18 April 2026. 8 overdue.`
- **Group items by list.** Within a slice, sub-group reminders by their `listName`, render each list as a `###` heading, and show items as a bulleted list underneath. Lists are sorted alphabetically by name.
- The list heading **uses the emoji already in the list name** when present (e.g. `### 💳 Bills & Payments (2)`). For lists without an emoji (e.g. `Waiting a Reply`, `Inbox`, `Shopping`, `Working On`), pick a sensible one from this map and prepend it:
  - `Waiting a Reply` → ⏳
  - `Inbox` → 📥
  - `Shopping` → 🛒
  - `Working On` → 🛠️
  Any other un-emoji'd list → 📌 as a safe default.
- Within each list, **sub-group items by due date**. Render the date as a bold sub-heading (`**Fri 17 Apr**`) and put the task name(s) as bullets underneath. Do not put the date on the task line.
- Item line: `- <name>` only. Plain task name. **Do not repeat the list name on each line** (the heading already tells us) and **do not repeat the date** (the sub-heading already tells us).
- Append ` [flagged]` at the end of the task line when `priority > 0`.
- Per-list counts in the heading: `### <emoji> <list name> (<count>)`.
- Sort date sub-headings within a list by date ascending (earliest first). Items with no due date sit under a final `**No due date**` sub-heading.
- Empty slice → `No <slice> reminders.` Don't render empty headings.

### Example (overdue slice)

```
Saturday 18 April 2026. 8 overdue.

### ⏳ Waiting a Reply (2)

**Thu 16 Apr**
- Re: Horbury Drive - Gas Check [flagged]

**Fri 17 Apr**
- Chase MySpace regarding scaffolding

### 💳 Bills & Payments (2)

**Thu 16 Apr**
- Claim Parking Back from DSG

**Fri 17 Apr**
- Check credit cards

### 💻 Digital & Tech (1)

**Fri 17 Apr**
- Install what's this YouTube video says

### 👵 Mum (1)

**Fri 17 Apr**
- Renewal Proposal for 69 Swinton Crescent, Bury, Lancashire, BL9 8PB

### 🔧 Repairs & Maintenance (2)

**Thu 16 Apr**
- Get boiler serviced

**Fri 17 Apr**
- RE: Warranty Claim, Gronodec Decking
```

### "Everything" view (option 6)

For the full dump, keep the urgency-band structure as the top level (`## Overdue / ## Due today / ...`), and within each band apply the same list-sub-grouping format above.

### "One specific list" view (option 5)

Drop the list heading entirely — the whole response is one list. Just show the one-line header (`Saturday 18 April 2026. 4 in 💳 Bills & Payments.`) and the bulleted items.

## Step 3 — mark items done (optional)

After a slice has been shown, B may want to check items off. He'll say something like:

- *"tick off the boiler one"* / *"done, boiler"* — single item, name match
- *"complete Chase MySpace and Check credit cards"* — batch, name match
- *"mark 2, 5 done"* — by position (1-based index across the rendered slice, skipping headings)
- *"done all of Waiting a Reply"* — all items in a sub-group

**Resolution rules:**

1. Match against the **most recent slice shown in this turn**. Use the `id` from the jq projection — do not re-fetch unless the cache is stale or B asks for a different slice.
2. **Name matches** use case-insensitive substring on the task name. If the substring matches >1 item, ask B to disambiguate (show the candidates with list + date).
3. **Position numbers** refer to the 1-based order in the rendered output, scanning top-to-bottom, bullets only (headings skipped). If the slice used position numbers, the disambiguation message should too.
4. **If 0 matches**: say so and re-show the slice.

**Confirm before commit (per `.claude/rules/apple-reminders.md`)** — never silently write. Show B the full batch in one preview block:

```
About to mark done:
- ⏳ Chase MySpace regarding scaffolding (Waiting a Reply, due Fri 17 Apr)
- 🔧 Get boiler serviced (Repairs & Maintenance, due Thu 16 Apr)

Confirm?
```

Wait for `yes` / `go` / `ok`. On confirm, run one `complete` call per id:

```bash
~/code/apple-mcp/bin/reminders-helper complete <id>
```

**After completion**: quickly confirm what was ticked off (one line: `Done. Ticked off 2 reminders.`) and re-render the current slice — recurring reminders may have spawned a new instance with a later due date, and completed items should drop out of the view. Use the same slice the earlier fetch was for.

If any `complete` call fails, surface the error per item without rolling back the rest — Apple Reminders doesn't support transactional batches and a half-done batch is still useful.

### Uncomplete / delete

Out of scope for this skill. If B asks to undo a tick-off or delete a reminder, point him to run `~/code/apple-mcp/bin/reminders-helper uncomplete <id>` or `delete <id>` manually, or invoke it one-off with the id from the last slice.

## Rules

- Writes (`complete`) require preview + confirmation per `.claude/rules/apple-reminders.md`. Never silently write.
- Do not call `mcp__apple-mcp__reminders` with `{operation: "list"}` — it returns the full dataset with bodies and timestamps and will blow past the token ceiling. The Swift helper + jq projection is the only data path.
- Never use em dashes or en dashes in the output (universal rule).
