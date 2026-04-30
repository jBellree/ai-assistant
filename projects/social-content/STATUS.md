# Social Content System — Current Status

**Last updated:** 2026-04-30

Read this first if you're a fresh Claude session picking up social-content work. It captures what's in flight and what the stable docs don't cover. For the architecture overview see [README.md](README.md). For the workflow see [.claude/skills/magnitude-social-content/SKILL.md](../../.claude/skills/magnitude-social-content/SKILL.md).

---

## Build status

### Done

- Markdown-first architecture: EA is the system of record, Airtable (Content Hub base `appwPT59GISaH3phA`) is secondary (RSS curation + calendar only)
- Brand docs migrated from `.docx` to markdown in [references/brand/](../../references/brand/) (tone-of-voice.md, buyer-persona.md, what-i-do.md, social-post-checklist.md)
- Root `.docx` originals archived to [archives/brand-docs-original/](../../archives/brand-docs-original/)
- Airtable Content Pillars table updated to the EA 5-pillar set (Deal Spotlight, Rate Watch, Lender News, Underwriting Masterclass, Industry Insight)
- Airtable Brand Settings: Tone of Voice record synced from markdown (Buyer Persona + Company Description deferred, existing Airtable values are semantically equivalent)
- Airtable write permission unblocked for the Content Hub base only (exception in memory; every other base stays read-only)
- hcti.io credentials in CLAUDE.local.md, working
- Gemini API key in CLAUDE.local.md (nano banana, free tier via AI Studio), not yet wired into the skill flow
- Logos: white, orange, brand (orange crest + white text), and crest-only all saved as both PNG and `.b64` in [references/brand/logos/](../../references/brand/logos/)
- First template designed and iterated to v9: [.claude/skills/magnitude-social-content/templates/explainer.html](../../.claude/skills/magnitude-social-content/templates/explainer.html)
- Render helper: [.claude/skills/magnitude-social-content/templates/render.py](../../.claude/skills/magnitude-social-content/templates/render.py) with `--local` for free browser preview and default mode for hcti.io PNG
- VS Code workspace configured: Claude docks to sidebar; Live Preview extension recommended for in-editor HTML preview

### Pending

- [ ] Finalise `explainer.html` design (substantially done, awaiting B's final sign-off)
- [ ] Redesign `rate-watch.html` template (stub in place, originally `references/brand/template-preview.html`)
- [ ] Redesign `single-quote-example.html` template (stub in place, was "deal spotlight")
- [ ] Build `underwriting-tip.html` template (education card)
- [ ] Wire Gemini image generation into the skill flow (Step 5 of SKILL.md) so Claude calls the Gemini API after copy is finalised and saves the hero image locally
- [ ] Run first end-to-end post through the skill
- [ ] Sync remaining 2 Brand Settings records to Airtable (Buyer Persona + Company Description) when B starts actively using Content Hub

---

## How B iterates on templates (key workflow)

### Design iteration loop (no hcti credits used)
1. Edit the HTML file directly in VS Code
2. Either: click the Live Preview icon in the editor toolbar for a split-pane preview, OR `python3 .claude/skills/magnitude-social-content/templates/render.py <template_name> --local` to open a polished preview in the browser
3. Iterate until B signs off

### Production render (uses 1 hcti credit per call)
`python3 .claude/skills/magnitude-social-content/templates/render.py <template_name> --slug <slug>` (no `--local`)
Returns a PNG URL from hcti.io and saves `card.png` to `library/posts/magnitude/YYYY-MM-DD-<slug>/`.

### hcti.io free tier
**50 images/month.** Earlier in the build we burned several credits iterating. **Default to `--local` or Live Preview; only hit hcti for the final production render.** The `render.py --local` path is pixel-identical to hcti (both use Chrome to render).

---

## Key design decisions from this session

- **Canvas size:** 1080×1350 (Instagram portrait) for content-dense explainer cards. 1080×1080 works for sparse cards like Rate Watch but can't fit multi-section content at readable font sizes.
- **Logo:** orange crest + white wordmark is the brand-correct version for dark backgrounds (per `references/brand/logos/README.md`). File: `magnitude-full-brand.png` / `magnitude-full-brand.b64`. Centered at top of explainer cards.
- **Fonts:** Poppins (headings, 38px/800), Montserrat (body, 28px/regular). Loaded via Google Fonts in hcti.io and the local preview wrapper.
- **Colours:** `#1A212E` (dark slate bg), `#ED792B` (brand orange), white on orange for the top accent bar.
- **Em dashes banned universally.** render.py refuses to render any template containing `—` or `–`. Rule lives in [.claude/rules/communication-style.md](../../.claude/rules/communication-style.md) and auto-memory.
- **Template files use relative image paths**, not base64 placeholders. render.py inlines images as base64 when sending to hcti.io. Means you can double-click any template HTML and see the rendered result.

---

## Known constraints / things to remember

| Thing | Constraint |
|---|---|
| Em dashes | **Never use**, anywhere, chat or copy or image text. Use commas, full stops, brackets. |
| Airtable writes | Allowed ONLY on base `appwPT59GISaH3phA` (Content Hub). Every other base is read-only. Always propose writes to B before committing. |
| hcti.io | 50 image free tier/month. Prefer local preview during iteration. |
| Gemini | Free tier via AI Studio, generous (hundreds/month). Key in CLAUDE.local.md. |
| Representative APR | When rates are quoted publicly in a card, FCA disclaimer at the bottom must include a representative APR matching the lowest rate shown. |
| WhatsApp vs LinkedIn | WhatsApp dealer group is the primary channel for most trade content. LinkedIn is B's personal brand (D2C angle). Instagram is Magnitude consumer brand. |

---

## Next natural step

Finalise the explainer template design with B, then tackle the `rate-watch.html` template (simplest, next most useful).
