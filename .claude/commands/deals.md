---
description: Current month deals by stage — counts and £ totals vs monthly targets
---

Show B the current month's deal pipeline from Airtable.

**Base:** `appCXdGmjsg5dxUIC` (CRM base — **READ ONLY**, never write, per `.claude/rules/deal-tracker.md` and `references/sops/airtable-crm-base.md`)

**Table:** Income Summary — `tblyizBxLUboB6814`

**Important schema note:** status is NOT a single-select field. It's a set of **checkbox fields** representing stages the deal has passed through:
- `Awaiting Decision`
- `Awaiting Info`
- `Accepted`
- `Declined`
- `A.S.D` (Awaiting Signed Docs)
- `In for Payout`
- `Converted`
- `Logged` (post-Converted, numbers reconciled)
- `Cancelled Proposal`
- `Cancelled Acceptance`

A deal typically has multiple checkboxes set as it progresses (a Converted deal will also have Accepted ticked, etc). Group each deal by its **furthest stage** — the latest checkbox that's true in the order above. That's the deal's current state.

**Steps:**

1. Use the Airtable MCP to list records in Income Summary, filtered to current month (use `mcp__claude_ai_Airtable__list_records_for_table` or similar). If a direct month filter isn't simple, pull the last ~200 records and filter client-side by a date field (likely `Created`, `Proposal Date`, or similar — inspect the schema first via `get_table_schema` if unsure).
2. For each record, determine its furthest stage from the checkbox fields above.
3. Also pull the Targets table (`tblsijrcgLyEEIP7U`) for the current month to show current vs target.
4. Output format:

```
## Deals — <Month Year>

| Stage | Count | £ Advance |
|---|---|---|
| Awaiting Decision | N | £... |
| Accepted | N | £... |
| A.S.D | N | £... |
| In for Payout | N | £... |
| Converted | N | £... |
| Cancelled | N | £... |

**Targets this month:**
- Converted: N / 63
- Proposals: N / 150
- Advances: £N / £2.5m
- Dealer sources: N / 20
```

Highlight any stage where the current-month trajectory is behind target (e.g. halfway through the month with less than half the target).

**Do not modify any records.** This is a read-only dashboard view.
