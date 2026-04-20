---
description: Rules for working with B's deal tracking system (CRM base appCXdGmjsg5dxUIC)
globs: *
---

# Deal Tracker

## Deal lifecycle stages

Status is a set of **checkbox fields** on Income Summary, not a single-select. A deal typically has multiple boxes ticked as it progresses — the deal's "current" stage is the furthest true checkbox in this order:

1. **Awaiting Decision** — proposal submitted to lender
2. **Awaiting Info** — missing info from applicant
3. **Accepted** — finance application accepted by lender
4. **Declined** — end state (rejection)
5. **A.S.D** — Awaiting Signed Documents
6. **In for Payout** — documents signed, submitted for payout
7. **Converted** — deal paid out
8. **Logged** — post-Converted, B has reconciled numbers against internal system
9. **Cancelled Proposal** / **Cancelled Acceptance** — branch cancellations

## System

- The deal tracker lives in Airtable CRM base `appCXdGmjsg5dxUIC`.
- The DSG tooling (deal tracker, dealer call planner, KPI dashboard, content management) is in the `../DSG/` folder.
- When B asks to update a deal, confirm the deal reference and the new status before making changes.

## Write rule — scoped exception, confirm before commit

The CRM base is **read-only by default**. EA may write **only** to the tables and fields listed below, and every write follows the same preview → confirm → commit pattern used for Apple Reminders (see [apple-reminders.md](apple-reminders.md)) and Content Hub (see [airtable-schema.md](airtable-schema.md)).

### What EA can write

| Table | Table ID | Permitted writes |
|---|---|---|
| Income Summary | `tblyizBxLUboB6814` | Stage checkbox updates only (the 9 stages above). Never edit Customer, Dealer, Advance, or any other field. |
| Dealer Contact Log | `tblnVlE0OUD7futzx` | **Create** new contact log rows (dealer, date, contact type, notes). No edits/deletes of existing rows. |
| Deal Tasks | `tblBTnl0O4USdkaQz` | Create new tasks (title, linked Deal, Task Date, Reminder DateTime). Edit Task Date to defer. Mark complete (Status + Completed Date). No deletes. Never edit the linked Deal. |
| Dealer Task | `tbl4NeGnai5q9HvDe` | Create new tasks (Title, linked Dealer, Description, Due Date, Priority, Reminder DateTime). Edit Due Date to defer. Mark complete. No deletes. Never edit the linked Dealer. |
| General Tasks | `tblyyeVpepmnKjXrf` | Create new tasks (Task Title, Description, Due Date, Priority, Reminder DateTime). Edit Due Date to defer. Mark complete. No deletes. |

Everything else in the CRM base — Dealer Database, Dealer Contacts, Finance Companies, Targets, Stats rollups, User Settings, etc. — stays **strictly read-only**.

### Todoist sync — side-effect to be aware of

Deal Tasks, Dealer Task, and General Tasks each have a `Todoist Task ID` field and a live two-way sync with Todoist. When EA writes to any of these tables, **Todoist will update automatically** — that is the intended behaviour (B sees the same task state on his iPhone via Todoist when out on the road). No separate Todoist writes are needed. Just know that every Airtable task write propagates.

### Write pattern

Before any write, show B the exact change and wait for "yes" / "go" / "ok":

> I'm about to update record `recXYZ` in Income Summary:
> - A.S.D: ☐ → ☑
> - In for Payout: ☐ → ☐ (unchanged)
> Confirm?

For new Dealer Contact Log rows:

> I'm about to add a Dealer Contact Log row:
> - Dealer: Proctors (linked)
> - Date: 2026-04-19
> - Contact Type: Phone Call
> - Notes: Spoke to Glyn, Defender prop coming
> Confirm?

Batch writes get a single combined preview before a single confirmation.

### What still requires B to do it manually in Airtable

- Creating new deal records (Income Summary rows).
- Editing any deal field other than the stage checkboxes.
- Creating new dealers, contacts, finance companies.
- Updating Targets.
- Anything that touches rollup fields or formulas.

If B asks for one of these, EA proposes the change and gives him the Airtable URL to do it himself.
