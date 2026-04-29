---
name: social-content
description: Skill: Social Content Generator
---

# Skill: Social Content Generator

## Trigger phrases
"content", "create a post", "WhatsApp post", "LinkedIn post", "Instagram post", `/social-content`

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
- Deal Spotlight → the actual vehicle — use the **Vehicle image sub-workflow** below
- Rate Watch / Lender News → abstract relevant imagery (clean graphic, minimal, brand-aligned) — or skip image and use the branded template alone
- Underwriting Masterclass → infographic-style illustration (e.g. balancing scales for comparisons)
- Industry Insight → conceptual imagery tied to the topic

#### Vehicle image sub-workflow (cars, vans, trucks, plant, any physical vehicle)

**Ask the 6 questions ONE AT A TIME. Never batch them.** Offer the brand default with each, B can accept the default or override.

**Use the `AskUserQuestion` tool for every gate in this flow** (B's explicit preference — he doesn't want to type answers):
- Each of the 6 questions → `AskUserQuestion` with 2-4 radio options. Default option first, label it "(Recommended)" or similar, with alternatives beneath. User picks or uses the free-text "Other" fallback.
- The prompt-approval gate (after all 6 answered) → `AskUserQuestion` with "Approve and generate" vs "Tweak the prompt first" options.
- The post-generation verdict gate (after showing the image) → `AskUserQuestion` with "Lock in as canonical" / "RHD is wrong, regenerate" / "Something else to change" options.

If `AskUserQuestion` is not loaded in the current session, use `ToolSearch` with `query: "select:AskUserQuestion"` to load it at the start of the workflow.

Also applies when building the standalone vehicle library under `references/vehicle-library/`.

1. **Year / trim?** (e.g. 2018 first-gen, Performante, S, SE hybrid) — no default, needs B's input
2. **Colour and finish?** (solid gloss / metallic / pearl / matte / satin wrap) — no default
3. **Angle?** Default: **3/4 front from the driver's side (right side of the vehicle), slight low hero angle, camera pulled back so the full vehicle is in frame with generous negative space around it**. Critical: for UK/RHD vehicles the angle MUST be from the driver's (right) side. This is the only reliable way to force Gemini to render RHD correctly — aggressive RHD prompt text alone does not overcome training bias. Proven on Urus Performante v6 (2026-04-19).
4. **Setting?** The library has **two primary style categories**. Pick based on the post type:

   **A. Moody studio (hero shots, brand-consistent)** — Default for Deal Spotlight posts and anywhere the vehicle is the focus. Prompt cue: "moody dark studio with a soft graduated backdrop fading to near-black, clean void-like space, subtle rim-light along the top edge of the car separating the paint from the dark background, cinematic but not over-dramatic, polished dark studio floor with soft reflection pool". Works with 1:1 square aspect. Template: Urus v6, Roma v1.

   **B. Lifestyle / real-world UK location (storytelling, context)** — For posts where atmosphere, location, or UK authenticity adds value. Prompt cue: "UK countryside setting (Yorkshire Dales / Cotswolds / Lake District / Scottish Highlands / coastal), dry stone walls or hedgerows, rolling hills, period stone buildings in the middle-distance, overcast natural British daylight, candid magazine-press-car composition". Works with 16:9 landscape aspect so scenery wraps around the car. Template: 911 Carrera S v1 in Yorkshire Dales.

   Alternatives B may pick for either style: underground car park, private estate driveway, showroom, pro-set studio with visible softbox lamp stands (pro-photographer aesthetic), coastal cliff road at dusk, etc.
5. **Lighting / mood?** Default: **cinematic, clean, subtle rim-light, not over-dramatic**
6. **Aspect ratio?** Default: **1:1** (1080×1080 for WhatsApp/Instagram). LinkedIn hero: 16:9.

**Fixed brand rules (always in the prompt, never asked):**
- **UK right-hand drive (RHD) configuration, steering wheel on the right side of the vehicle.** B is UK-based, all library images must be RHD. Front-load this in the prompt with CRITICAL emphasis and repeat: "UK right-hand drive (RHD) specification vehicle. Steering wheel clearly visible on the RIGHT side of the cabin. Driver seat on the RIGHT. This is a UK-market car, not European or US. Right-hand drive, repeat: right-hand drive."
- **Camera angle must be from the driver's (right) side of the vehicle** — this is the RHD-forcing geometry. See Angle default in Q3.
- **Side profile is a valid RHD-agnostic fallback.** If the model keeps defaulting to LHD even with the driver-side angle (rare but can happen on hard cases), switch to a pure side profile shot. The steering wheel isn't visible from side profile, so LHD vs RHD becomes undetectable from the image, which sidesteps the training bias entirely. B flagged this tactic on the Ferrari Roma (2026-04-19).
- No number plates, no dealer logos, no people in shot
- Photorealistic, sharp focus, shallow depth of field
- Professional automotive photography

**Default model for vehicle library images:** `gemini-3-pro-image-preview` (Nano Banana Pro, ~$0.13/image). Pro renders trim-specific details (carbon bonnets, wider arches, RHD) and matte finishes correctly where Flash fumbles. Use `gemini-2.5-flash-image` for post-specific heroes where trim doesn't matter, or for quick iterations.

**Library folder structure:** vehicles are organised by manufacturer subfolder. Create a new folder when a new manufacturer is introduced.

```
references/vehicle-library/
├── lamborghini/
│   └── 2024-lamborghini-urus-performante-...png + .md
├── ferrari/
│   └── 2021-ferrari-roma-coupe-...png + .md
└── [new-manufacturer]/  ← add as needed
```

**Never overwrite an existing library image.** Every generation gets a unique filename using this convention:

`[year]-[make]-[model]-[trim]-[colour]-[angle]-v[N]-[notes].png`

Example: `2024-lamborghini-urus-performante-matte-black-34front-v6-moody-studio-rhd-driverside-wide.png` (lives in `references/vehicle-library/lamborghini/`)

If a regeneration is needed, increment the `v[N]`. Each PNG gets its own sidecar `.md` with the prompt and metadata. The current canonical version for a vehicle is marked `canonical: true` in its sidecar frontmatter; superseded versions stay on disk as `canonical: false` with a `status:` note explaining why they were archived. Nothing gets deleted or overwritten.

**API aspect ratio:** pass `generationConfig.imageConfig.aspectRatio` in the request body. Supported: `"1:1"` `"4:5"` `"3:4"` `"9:16"` `"16:9"` `"2:3"` `"3:2"`.

Once all 6 answered, write the Gemini prompt using this skeleton:

> Professional automotive photography of a [year] [make] [model] [trim] in [colour + finish]. [Angle]. [Setting]. [Lighting / mood]. Photorealistic, sharp focus, shallow depth of field. No number plates, no logos, no people in shot. Aspect ratio [X].

Show the prompt to B before calling Gemini — he may tweak.

#### Non-vehicle images
For abstract / infographic / conceptual imagery, write the prompt and show B directly (no question flow needed).

Call Gemini 2.5 Flash Image (Nano Banana) via API. Model ID: `gemini-2.5-flash-image`. API key in `CLAUDE.local.md` as `GEMINI_API_KEY`.

Endpoint: `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GEMINI_API_KEY`

The returned image is base64 under `candidates[0].content.parts[].inlineData.data`. Decode and save to: `archives/posts/YYYY-MM-DD-[slug]/hero.png`.

Cost is ~$0.04 per image. If a post clearly needs higher fidelity (prestige / supercar hero), ask B before switching to `gemini-3-pro-image-preview` (Nano Banana Pro, ~3x cost).

### Step 6 — Compose the branded card (hcti.io)

All branded card HTML templates live in `.claude/skills/social-content/templates/`.

**Templates that exist today:**
- `magnitude-explainer.html` — 1080×1350 vertical explainer card (4 sections, checklists). Used for onboarding / "who is Magnitude" dealer posts.
- `testimonial-of-the-week.html` — 1080×1350 pull-quote card with vehicle image. Single slide. For a quote from B or a customer testimonial.
- `quote-of-the-week-01-hero.html` / `quote-of-the-week-02-breakdown.html` / `quote-of-the-week-03-contact.html` — 3-slide Instagram/LinkedIn/WhatsApp carousel for real finance quote examples (vehicle hero → full PCP/HP breakdown → contact CTA).

**Templates to build as the need comes up** (listed in the skills backlog — build-on-demand, not upfront):
- `deal-spotlight.html` — for Deal Spotlight posts
- `underwriting-tip.html` — for Underwriting Masterclass posts

If the pillar doesn't have a matching template yet, either (a) pick the closest existing template and adapt, or (b) stop and build the new template first with B. Do not invent template names that don't exist.

Pillar → template mapping:
- **Deal Spotlight** → `deal-spotlight.html` (to build) or adapt `testimonial-of-the-week.html` for now
- **Rate Watch / Lender News** → no dedicated template; use plain copy + a Gemini hero image, no branded card, OR adapt `magnitude-explainer.html`
- **Underwriting Masterclass** → `underwriting-tip.html` (to build)
- **Industry Insight** → no dedicated template; plain copy + Gemini hero
- **Finance quote example** → use the `quote-of-the-week-01/02/03` carousel set

**Render via `render.py`, not hand-rolled curl.** Every template in this folder is rendered through `.claude/skills/social-content/templates/render.py`, which handles token substitution, logo base64 injection, local image inlining, the em/en dash safety check, and the hcti.io POST. Do not build the payload manually.

Canonical command shape:
```
python3 .claude/skills/social-content/templates/render.py \
  <template-name> \
  --var TOKEN=VALUE \
  --var TOKEN=VALUE \
  [--local]
```

- `<template-name>` is the `.html` filename without the extension, e.g. `quote-of-the-week-01-hero`.
- Every `{{TOKEN}}` placeholder in the template needs a matching `--var`. The per-template token list lives in the comment block at the top of that template's `.html` file (read the template first).
- `--local` writes a wrapped HTML to `/tmp/hcti-previews/` and opens it in the browser. No hcti.io call, no credits, no PNG. Use this while iterating on copy, layout, fades, typography.
- Drop `--local` when B says "ship" or "render it". render.py then POSTs to hcti.io, downloads the returned PNG to `/tmp/hcti-previews/<template>-TIMESTAMP.png`, and prints the URL and saved path. The PNG is what gets uploaded to Instagram / WhatsApp / LinkedIn.
- Browser preview and hcti.io output are very close but not pixel-identical (font loading, subpixel rendering, blend mode behaviour can differ). Always eyeball one final hcti.io render before posting.
- Credentials `HCTI_API_USER_ID` and `HCTI_API_KEY` are in `CLAUDE.local.md`. render.py reads them automatically.

### Vehicle image path convention

Templates that reference a library vehicle expect a **relative path from the template file**. From `.claude/skills/social-content/templates/` up to the vehicle library is four levels:

```
../../../../references/vehicle-library/<make>/<filename>.png
```

Pass this as `--var VEHICLE_IMG="../../../../references/vehicle-library/..."`. render.py's `inline_local_images` walks every `<img src="relative/path">` and rewrites it to a base64 data URI before sending to hcti.io, so the same `src` works when you open the template directly in a browser and when it ships to hcti.io.

Logos follow the same pattern but with tokens: `{{LOGO_BRAND}}`, `{{LOGO_WHITE}}`, `{{LOGO_ORANGE}}`, `{{LOGO_CREST}}`. render.py substitutes these with base64 from `references/brand/logos/*.b64`. Never inline logos by hand.

### Vehicle image compositing pattern

Templates that blend a library vehicle into the dark card background (`testimonial-of-the-week.html`, `quote-of-the-week-01-hero.html`) follow a consistent recipe:

- `mix-blend-mode: lighten` on the `<img>` so dark studio shots fuse with `#1A212E` and bright lifestyle shots stay punchy.
- Bottom gradient overlay (~220px tall) fading the image into a clean dark strip so overlay text sits on solid background.
- Side fades (~160px wide) covering **bottom edge only** (e.g. `top:620px; bottom:0` on an 820px image box). Their job is to merge the bottom-left and bottom-right corners into the dark strip. No top fade. Never run side fades full-height, they create visible banding up the sides.
- Optional radial mask on the `<img>` for a softer floated feel. Keeps edges feathered top and sides so the image does not sit in a hard rectangle.

If you add a new vehicle-image template, copy the image block from one of the two validated references (do not rebuild from scratch):

- **Primary**: [quote-of-the-week-01-hero.html](templates/quote-of-the-week-01-hero.html) — 820px image box, side fades at `top:620; bottom:0`.
- **Alternate**: [testimonial-of-the-week.html](templates/testimonial-of-the-week.html) — 700px image box, side fades at `top:520; bottom:0`.

Both use the same recipe (mix-blend-mode: lighten + radial mask + bottom gradient + bottom-edge-only side fades). The `top` value on the side fades scales with the image box height: aim for roughly `height minus 200` so the fades cover only the last ~200px of the image.

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
Show B the copy, hcti.io URL, archive path, and Airtable link (if updated). One platform reminder. Keep it short.

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
