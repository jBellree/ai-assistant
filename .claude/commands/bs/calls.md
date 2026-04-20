---
description: Today's dealer call priorities from the Dealer Call Planner
---

Show B today's priority dealer calls from the Airtable CRM.

**Base:** `appCXdGmjsg5dxUIC` (CRM base — read-only for this command; logging call outcomes happens inside the `daily-planning` skill, see `.claude/rules/deal-tracker.md` for the scoped write rule)

**Primary table:** Dealer Call Planner — `tblEUwKPuDGBHXbwm`
**Cross-reference table:** Dealer Database — `tbldEZLgMGhHahWge` (has the A/B/C/D Category field — see dealer strategy memory)

**Steps:**

1. Inspect the Dealer Call Planner schema first with `get_table_schema` to identify the relevant fields (likely: Dealer, Last Contact, Next Contact Due, Priority, Frequency, Status). Use the actual field IDs returned, don't guess.
2. Pull records where Next Contact Due is today or overdue, OR where a Priority flag is set. If the table uses a different model, adapt — the goal is "who does B need to call today".
3. For each row, look up the dealer in Dealer Database to get the A/B/C/D tier (per the dealer strategy memory: A = top, D = bottom; build breadth not just depth).
4. Output format:

```
## Dealer calls — <weekday> <date>

**Overdue** (count)
- [Tier A] <Dealer name> — last touched <date>, due <X> days ago

**Due today** (count)
- [Tier B] <Dealer name> — <brief context if any>

**Flagged / priority** (count)
- [Tier A] <Dealer name> — <reason>
```

Sort within each bucket by tier (A > B > C > D) then by days overdue.

If the table has no overdue or due-today records, say so in one line and suggest B check whether the Call Planner is being maintained (the memory note says it's underused due to HubSpot dual-tracking).

**This command is a read-only dashboard view.** Logging call outcomes (new Dealer Contact Log rows) happens inside the `daily-planning` skill under the scoped write rule.
