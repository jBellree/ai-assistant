---
name: plaud-content
description: PLAUD voice note transcript sub-skill. Takes a pasted transcript and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: PLAUD Content Ideas

## Purpose
Take a PLAUD voice note transcript pasted by B and generate 4-6 content ideas.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Get the transcript
Ask B to paste the PLAUD transcript. Wait for the paste.

### Step 2 — Generate ideas
Read the transcript against:
- `@references/content-pillars.md`
- `@references/brand/tone-of-voice.md`
- `@references/brand/buyer-persona.md`
- `@.claude/rules/content-guidelines.md`

Generate 4-6 ideas. For each idea produce:

| Field | Description |
|---|---|
| Pillar | One of: Deal Spotlight / Rate Watch / Lender News / Underwriting Masterclass / Industry Insight |
| Audience | Dealer WhatsApp / LinkedIn D2C / Instagram / multiple |
| Angle | The specific hook that makes this worth posting, grounded in real detail from the transcript |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

Voice notes are raw and conversational. Extract the substance, the deal detail, the observation, the insight. Polish the angle; keep it grounded in what B actually said.

### Step 3 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.

## Note on PLAUD integration
Currently paste-in. Future upgrade: if PLAUD exports transcripts to a known file path, update Step 1 to read the file directly instead of requesting a paste.
