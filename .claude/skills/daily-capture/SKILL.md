---
name: daily-capture
description: Daily work capture sub-skill. Draws out the detail of B's day through conversation and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: Daily Capture Content Ideas

## Purpose
Draw out the content-worthy detail from B's day — deals funded, tricky cases solved, observations from the trade — and generate 4-6 content ideas.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Draw out the detail
Ask these questions ONE AT A TIME using `AskUserQuestion` where possible. Stop when you have enough to generate ideas — you don't need all four if the first two give you plenty.

1. "What happened today that was interesting — a deal, a case, a conversation?"
2. "What made it unusual or tricky?"
3. "What would a dealer take away from this if you told them?"
4. "What would a buyer take away from this?"

Listen for: vehicle type, finance product used, lender, anything that made the case harder than normal, the outcome, any lesson learned.

### Step 2 — Generate ideas
Read B's answers against:
- `@references/content-pillars.md`
- `@references/brand/tone-of-voice.md`
- `@references/brand/buyer-persona.md`
- `@.claude/rules/content-guidelines.md`

Generate 4-6 ideas. For each idea produce:

| Field | Description |
|---|---|
| Pillar | One of: Deal Spotlight / Rate Watch / Lender News / Underwriting Masterclass / Industry Insight |
| Audience | Dealer WhatsApp / LinkedIn D2C / Instagram / multiple |
| Angle | The specific hook that makes this worth posting — rooted in the real detail B gave |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

The best ideas come from the ugly, unpolished details — the specific lender, the weird edge case, the thing that surprised B. Those are the things no AI can invent and no competitor can copy.

### Step 3 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.
