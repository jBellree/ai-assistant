# Skill: Social Content Generator

## Trigger phrases
- "content"
- "create a post"
- "WhatsApp post"
- "LinkedIn post"
- "Instagram post"
- `/social-content`

## Purpose
Generate branded social content for B's dealer WhatsApp group, LinkedIn, and Instagram.
Produces: copy in B's voice + Gemini hero image + hcti.io branded card.
Archives every post locally for FCA record-keeping and updates Airtable so Content Hub's calendar stays in sync.

## Context to load (EA markdown — the main copies)
- @references/brand/tone-of-voice.md
- @references/brand/buyer-persona.md
- @references/brand/what-i-do.md
- @references/brand/social-post-checklist.md
- @references/brand/compliance-disclaimers.md
- @references/brand/colours.md
- @references/brand/fonts.md
- @references/content-pillars.md
- @.claude/rules/communication-style.md
- @.claude/rules/content-guidelines.md
- @.claude/rules/airtable-schema.md

## Workflow

### Step 0 — Pick the source of the idea
Ask B: "Three ways to start — which one?"
1. **Saved RSS article** — Claude reads Airtable `Articles` table (base `appwPT59GISaH3phA`, table `tblvNFPoyugMVT9FL`), filters to Status in (`Manual Idea`, `Idea`, `Saved Ideas` view), shows the list — B picks one. Capture the `recordId` for the archive + status update later.
2. **From `ideas.md` backlog** — Claude reads `projects/social-content/ideas.md`, shows recent entries grouped by audience, B picks one.
3. **Fresh idea** — B describes it inline. Claude appends a line to `ideas.md` as it goes.

If B jumps straight to describing something ("Northridge dropped their rates"), infer and skip the menu.

### Step 1 — Pick the pillar
Ask or infer: Deal Spotlight / Rate Watch / Lender News / Underwriting Masterclass / Industry Insight. Pillars are defined in `references/content-pillars.md`.

### Step 2 — Get the details
Minimum questions needed. Don't over-ask.

**Deal Spotlight:** vehicle (make/model/year), finance product (HP/PCP/balloon/interest-only), angle, photo URL if any
**Rate Watch / Lender News:** lender, what changed, effective date, public APR if called out (needs representative APR)
**Underwriting Masterclass:** teaching point, specific example
**Industry Insight:** angle (FCA news, market, plate change, EV finance)

### Step 3 — Pick the platform(s)
WhatsApp / LinkedIn / Instagram / all three.

Platform guidance:
- **WhatsApp dealer group** — direct, practical, "here's what this means for you"
- **LinkedIn** — slightly more polished, B's professional brand, broader audience
- **Instagram** — visual-first, more consumer-facing (D2C Magnitude angle)

If "all three", generate one piece of copy, adapt tone per platform. Same image works for WhatsApp + Instagram (1080×1080). LinkedIn needs 1200×628.

### Step 4 — Generate the copy
Rules:
- Mirror tone in `references/brand/tone-of-voice.md`
- Straight-talking, no jargon
- UK English, no Americanisms
- Never slag off competition or lenders
- Never salesy — value and clarity first
- Questions as engagement hooks (not demands)
- Always end with correct FCA disclaimer (from `references/brand/compliance-disclaimers.md`)
- WhatsApp: 100–200 words max, punchy
- LinkedIn: 150–300 words, slightly more considered
- Instagram: 80–150 words, visual-first, hashtags (3–5, clean, thematic, at end)

Run the copy through `references/brand/social-post-checklist.md` before showing B.

Show the draft to B, iterate if needed. Only move on once B's happy.

### Step 5 — Generate the hero image (Gemini)
Now that the copy is finished, write a Gemini image prompt that fits the post:
- Deal Spotlight → the actual vehicle ("Porsche Taycan 4S, dark grey, studio backdrop, 3/4 angle, professional automotive photography")
- Rate Watch / Lender News → abstract relevant imagery (clean graphic, minimal, brand-aligned) — or skip image and use the branded template alone
- Underwriting Masterclass → infographic-style illustration (e.g. balancing scales for comparisons)
- Industry Insight → conceptual imagery tied to the topic

Show the prompt to B before calling Gemini — he may tweak.

Call Gemini 2.5 Flash Image (nano banana) via API. API key in `CLAUDE.local.md` as `GEMINI_API_KEY`.
Save the returned image to: `archives/posts/YYYY-MM-DD-[slug]/hero.png`

### Step 6 — Compose the branded card (hcti.io)
Select the template:
- Deal Spotlight → `deal-spotlight.html`
- Rate Watch / Lender News → `rate-watch.html`
- Underwriting Masterclass → `underwriting-tip.html`
- Finance quote → `finance-quote.html`

Read the template, inject:
- Copy variables (headline, lender name, rate, body text, disclaimer)
- Hero image as base64 data URI (read the saved PNG, encode, embed)
- Logo as base64 (from `references/brand/logos/magnitude-full-white.b64`)

POST to hcti.io:
```
POST https://hcti.io/v1/image
Authorization: Basic base64(HCTI_API_USER_ID:HCTI_API_KEY)
Content-Type: application/json

{
  "html": "[template with variables injected]",
  "google_fonts": "Poppins:400,600,700,900|Montserrat:400,500",
  "viewport": { "width": 1080, "height": 1080 }
}
```

Credentials in `CLAUDE.local.md`. Get the returned `url` and show B.

### Step 7 — Archive locally (FCA)
Save `archives/posts/YYYY-MM-DD-[pillar]-[slug].md`:

```markdown
---
date: YYYY-MM-DD
pillar: [pillar]
platforms: [WhatsApp / LinkedIn / Instagram]
template: [template name]
hero_image: archives/posts/YYYY-MM-DD-[slug]/hero.png
hcti_url: [returned URL]
airtable_record_id: [recXXX or null]
source: [rss / ideas.md / fresh]
---

## Copy
[Full post copy]

## Gemini prompt
[The image prompt used]

## Image variables
[Values injected into the template]
```

This is the FCA paper trail.

### Step 8 — Update Airtable (if post came from an RSS article)
Only if Step 0 path was "Saved RSS article" (we have a `recordId`).

Propose the update to B:
> I'm about to update Articles record `recXYZ`:
> - Status: [current] → Posted
> - Published Date: (empty) → YYYY-MM-DD
> - Platforms: += LinkedIn (etc.)
> - Content Pillars: → [pillar]
> - Hashtags: [final hashtags]
> Confirm?

On "yes" / "go" / "ok": commit the write via Airtable MCP. Otherwise skip / edit.

If the post came from `ideas.md` or a fresh idea, skip this step (no Airtable record to update) — but strike through or annotate the `ideas.md` line if it came from there.

### Step 9 — Done
Show B:
- Copy (formatted, ready to paste)
- Image URL (hcti.io)
- Archive path
- Airtable record link (if updated)

Remind which platform(s) it's for. Keep it short.

---

## Brand reminders (always apply)
- Background: `#1A212E` (Darkest Slate)
- Accent: `#ED792B` (Burnt Orange)
- Heading font: Poppins Bold/ExtraBold
- Body font: Montserrat Regular/Medium
- Logo: top of image (use `magnitude-full-white.b64` for Magnitude content)
- FCA disclaimer: always at the bottom of every image and every post
- Rounded corners on all cards — brand rule
- Never use "DSG" branding on Magnitude content — they're separate brands
- "Magnitude Finance is a trading style of DSG Financial Services Ltd" only in the legal block
