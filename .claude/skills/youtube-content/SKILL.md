---
name: youtube-content
description: YouTube content idea sub-skill. Fetches a video transcript and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: YouTube Content Ideas

## Purpose
Fetch a YouTube video transcript and generate 4-6 content ideas for Magnitude Finance or DSG Financial Services social content.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Get the URL
Ask B for the YouTube URL (or receive it from the orchestrator).

### Step 2 — Fetch the transcript
Run:
```bash
python3 ".claude/skills/youtube-content/fetch_transcript.py" "<url>"
```
If the script fails (private video, no captions), tell B and return to the orchestrator with no ideas.

### Step 3 — Generate ideas
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
| Angle | The specific hook that makes this worth posting — grounded in real detail from the video |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

Ideas must be specific to the actual video content. No generic angles. Pull in real details, facts, and quotes from the transcript.

### Step 4 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.

## Error handling
- Private or age-restricted video: tell B, skip this source
- No captions available: tell B, suggest trying a different video
- Script error: show the error message, skip
