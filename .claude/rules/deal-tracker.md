---
description: Rules for working with B's deal tracking system
globs: *
---

# Deal Tracker

## Deal lifecycle stages
1. **New Deal** -- deal entered into the system
2. **Accepted** -- finance application accepted by lender
3. **ASD** -- Awaiting Signed Documents
4. **In for Payout** -- documents signed, submitted for payout
5. **Converted** -- deal paid out and completed

## System
- The deal tracker lives in Airtable
- The DSG tooling (deal tracker, dealer call planner, KPI dashboard, content management) is in the `../DSG/` folder
- When B asks to update a deal, confirm the deal reference and the new status before making changes
