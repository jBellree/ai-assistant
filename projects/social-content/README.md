# Social Content System

**Status:** Active, markdown-first architecture
**Goal:** Consistent branded content for WhatsApp dealer group, LinkedIn, and Instagram

> **Picking up where we left off?** Read [STATUS.md](STATUS.md) first. It captures the current build state, design decisions, and constraints that aren't in the architecture docs.

## What this is

Two-system workflow:

- **EA (this workspace)** — the drafting + design environment. Claude Code skill drafts copy in B's voice, generates a Gemini hero image, composes a branded card via hcti.io, archives the post locally for FCA record-keeping, and updates Airtable so Content Hub's calendar stays in sync.
- **Content Hub** (DSG/Content Hub, deployed at content-hub-opal-xi.vercel.app) — specialised web tool for RSS curation and calendar viewing. Not the system of record; reads from Airtable base `appwPT59GISaH3phA`.

## Where things live (one place per thing)

| Thing | Location |
|---|---|
| Brand docs (Tone of Voice, Buyer Persona, What I do, Social Post Checklist) | [references/brand/](../../references/brand/) — markdown |
| Content pillars (the 5) | [references/content-pillars.md](../../references/content-pillars.md) |
| Post ideas / brain dump | [ideas.md](ideas.md) |
| Curated RSS articles queue | Airtable `Articles` table (written by Content Hub UI, read by EA) |
| Calendar (scheduled post dates) | Airtable `Articles.Published Date` → Content Hub calendar view |
| Logos | [references/brand/logos/](../../references/brand/logos/) — base64 |
| hcti.io card templates | [.claude/skills/magnitude-social-content/templates/](../../.claude/skills/magnitude-social-content/templates/) |
| Gemini hero images | `library/posts/magnitude/YYYY-MM-DD-[slug]/hero.png` |
| Rendered card PNGs | `library/posts/magnitude/YYYY-MM-DD-[slug]/card.png` |
| FCA post archive | [library/posts/magnitude/](../../library/posts/magnitude/) |
| Vehicle image library | [library/vehicles/](../../library/vehicles/) |

## How to use it

Open a Claude Code session, say "content" or `/bs:content`. The skill will:

1. Ask you where the idea comes from (saved RSS, `ideas.md`, or fresh)
2. Walk through pillar → details → platform → copy
3. Generate a Gemini hero image prompt from the finished copy, call the API, save locally
4. Compose the branded card via hcti.io
5. Archive locally
6. Propose an Airtable update (mark article Posted, set Published Date) — confirm and commit

## Platforms

- **WhatsApp dealer group** (primary — rate updates, deal spotlights, lender news)
- **LinkedIn** (B's personal brand — same content, slightly more polished)
- **Instagram** (D2C / Magnitude brand — visual-first, consumer angle)

## Content pillars

See [references/content-pillars.md](../../references/content-pillars.md) for the full definitions.

1. Deal Spotlight
2. Rate Watch
3. Lender News
4. Underwriting Masterclass
5. Industry Insight

## Suggested weekly rhythm

| Day | Type |
|---|---|
| Monday | Rate Watch or Lender News |
| Wednesday | Deal Spotlight or Underwriting Masterclass |
| Friday | Industry Insight or Deal Spotlight |

## Tech stack

- **Copy generation:** Claude (in Claude Code)
- **Hero image generation:** Gemini 2.5 Flash Image (nano banana) via Google AI API
- **Branded card composition:** hcti.io (HTML → PNG)
- **Templates:** HTML files in `.claude/skills/magnitude-social-content/templates/`
- **Logos:** Base64-encoded, stored in `references/brand/logos/*.b64`, embedded into templates at render time
- **API credentials:** `CLAUDE.local.md` (git-ignored) — `HCTI_API_USER_ID`, `HCTI_API_KEY`, `GEMINI_API_KEY`
- **Post library:** `library/posts/magnitude/` — rendered card PNGs + FCA compliance records
- **Airtable schema reference:** [.claude/rules/airtable-schema.md](../../.claude/rules/airtable-schema.md)

## Airtable write permission

Claude has **read + write** permission on Airtable base `appwPT59GISaH3phA` (Content Hub) only. Every other Airtable base remains read-only. Writes are always proposed to B for confirmation before committing — no silent edits.

## Setup checklist

- [x] Brand colours documented
- [x] Fonts documented
- [x] Compliance disclaimers written
- [x] Content pillars defined
- [x] Social content skill built
- [x] Logo files in `references/brand/logos/` (base64)
- [x] hcti.io credentials in CLAUDE.local.md
- [x] Brand docs converted from .docx to markdown
- [x] Airtable schema documented in `.claude/rules/airtable-schema.md`
- [x] Airtable write permission unblocked for Content Hub base
- [ ] Gemini API key added to CLAUDE.local.md (`GEMINI_API_KEY`)
- [ ] Template HTML files built and signed off (design phase)
- [ ] Airtable Content Pillars table updated to the 5-pillar set
- [ ] Airtable Brand Settings synced from EA markdown
- [ ] First content session run end-to-end
