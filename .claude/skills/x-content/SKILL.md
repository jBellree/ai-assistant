---
name: x-content
description: X (Twitter) content idea sub-skill. Scrapes motor finance industry posts via Apify and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: X Content Ideas

## Purpose
Scrape recent X posts across fixed motor finance search queries and generate 4-6 content ideas.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Read the Apify API key
Read `APIFY_API_KEY` from `CLAUDE.local.md`. If not present, tell B to add it and abort.

### Step 2 — Fetch X posts
Run:
```bash
APIFY_API_KEY="<key>" python3 ".claude/skills/x-content/fetch_x.py"
```

Fixed search queries (baked into script):
- "motor finance UK"
- "car finance UK"
- "FCA motor finance"
- "used car market UK"
- "PCP finance UK"

If the script fails, tell B and return to the orchestrator with no ideas.

### Step 3 — Generate ideas
Read the fetched posts against:
- `@references/content-pillars.md`
- `@references/brand/tone-of-voice.md`
- `@references/brand/buyer-persona.md`
- `@.claude/rules/content-guidelines.md`

Generate 4-6 ideas. For each idea produce:

| Field | Description |
|---|---|
| Pillar | One of: Deal Spotlight / Rate Watch / Lender News / Underwriting Masterclass / Industry Insight |
| Audience | Dealer WhatsApp / LinkedIn D2C / Instagram / multiple |
| Angle | The specific hook that makes this worth posting — grounded in real detail from the fetched posts |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

Ideas must reference real content from the fetched posts. No generic angles.

### Step 4 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.

## Error handling
- Missing `APIFY_API_KEY`: tell B to add it to `CLAUDE.local.md`, abort
- Apify API error: show error, suggest checking the key or Apify account balance
- Zero posts returned: tell B, suggest trying again later
