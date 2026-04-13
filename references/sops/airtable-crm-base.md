# Airtable: CRM Base

**Base ID:** `appCXdGmjsg5dxUIC`
**Rule:** READ ONLY. Never write.

## Tables

### Income Summary (`tblyizBxLUboB6814`)
B's main deal tracker. Every proposal is a row. Status is a set of checkbox fields that represent the deal lifecycle:
- Awaiting Decision -> Awaiting Info -> Accepted / Declined -> A.S.D (Awaiting Signed Docs) -> In for Payout -> Converted
- Cancellation branches: Cancelled Proposal, Cancelled Acceptance
- **Logged** = after Converted, B cross-references numbers (advance, income, payaway, debit back) against an internal system. If correct, deal is "Logged".
- **Checked** = back-end only visual. Used when end-of-month totals don't match the internal system and B has to re-verify each Logged deal. Rarely needed.

### Deal Tasks (`tblBTnl0O4USdkaQz`)
Tasks linked to specific deals in Income Summary.

### General Tasks (`tblyyeVpepmnKjXrf`)
Standalone to-do items not linked to a deal.

### Dealer Database (`tbldEZLgMGhHahWge`)
Master dealer list. Contacts, addresses, FCA numbers, notes.
- **Category** = A/B/C/D relationship tier (see dealer strategy memory)
- **Status** vs **Dealer Status** -- need to clarify difference

### Dealer Contacts (`tblc8DK0SVSZIZ93D`)
Contact details for individual people at each dealership.

### Dealer Task (`tbl4NeGnai5q9HvDe`)
Tasks linked to specific dealers.

### Dealer Notes (`tblAbDDKGUxvlH2bd`)
Notes linked to dealers.

### Dealer Proposal Stats (`tblCy5Rq3tLVUnpkp`)
Monthly proposal counts by dealer, by year.

### Dealer Call Planner (`tblEUwKPuDGBHXbwm`)
Contact frequency tracking, overdue alerts, priority flagging.
**Should** be B's daily point of focus but isn't, because DSG also uses HubSpot and B currently maintains two systems.

### Dealer Call Planner Assignments (`tbl88VJ5Su99Vtu0J`)
Scheduled calls with planned contact methods.

### Dealer Contact Log (`tblnVlE0OUD7futzx`)
History of every dealer contact.

### Dealer Converted Stats (`tblR7o5y5R6KKxPw5`)
Monthly converted deal counts by dealer, by year.

### Finance Companies (`tblLvbgrO35Vqc54l`)
Lender panel with commission terms and debit back provisions.

### Bonus (`tblU5wwdRIdZ8Ftro`)
Legacy. B's old bonus plan (volume-based with tiers 2.00% to 3.25%). Kept as a comparison reference via a tooltip on his dashboard. Not operationally used.

### Targets (`tblsijrcgLyEEIP7U`)
Monthly targets: proposals, converted, dealers, advances, retained, margin.

### User Settings (`tblHXN686ueZficlR`)
App settings (filters, theme, sorting).

### Conversion Stats (`tblHSx7dIuxtM3PTO`)
Not in active use. B built it as a scenario modelling tool to show that reducing the ~20/month cancelled acceptances has more impact on payouts than increasing proposals. See cancellation insight memory.

## Other Bases
- AM Referral List May 2025 (`appN8whZr5vW38k8d`) -- legacy
- Commercial Lenders Bible (`appfdlvMVwpbozF9Q`) -- lender reference
- Content Hub (`appwPT59GISaH3phA`) -- content management
- Consumer Lender Bible (`appocYI9TeYzX9FlU`) -- lender reference
