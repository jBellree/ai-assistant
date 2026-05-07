---
name: dsg-social-content
description: DSG-branded social content card generator. Use for DSG Prestige or DSG Vision WhatsApp, LinkedIn, and Instagram cards.
---

# Skill: DSG Social Content Generator

## Trigger phrases
"DSG post", "DSG content", "DSG WhatsApp", "DSG card", "DSG LinkedIn", "DSG Instagram", `/dsg-social-content`

## Purpose
Generate branded social content cards for DSG Prestige or DSG Vision.
Produces: copy in B's voice + hcti.io branded card as a working `card.html` saved to the library.
Archives every post locally for FCA record-keeping.

## First question: which sub-brand?

Always ask this before anything else. The answer determines the accent colour and logo token used throughout.

- **Prestige** — dealer-facing, prestige/specialist vehicles, accent `#017FFF` (Azure Blue), logo token `{{LOGO_DSG_PRESTIGE}}`
- **Vision** — accent `#0DB729` (Apple Green), logo token `{{LOGO_DSG_VISION}}`

If B says "DSG" without specifying, ask. Do not assume.

Use `AskUserQuestion` for this gate. If not loaded, run `ToolSearch` with `query: "select:AskUserQuestion"` first.

---

## DSG Brand Reference

### Colours

| Name | Hex | Usage |
|---|---|---|
| Deep Slate | `#252E3F` | Background on all cards |
| Teal | `#29D9D9` | DSG Group primary accent (chevron, group-level content) |
| Azure Blue | `#017FFF` | Prestige sub-brand accent (headings H3, bullets, bars) |
| Apple Green | `#0DB729` | Vision sub-brand accent |
| Platinum | `#C6C6C6` | Prestige chevron in logo (don't use as text colour) |
| White | `#FFFFFF` | All body text and H1/H2 on dark backgrounds |
| Light Grey | `#FBFBFB` | Supporting use only |

Quick reference by sub-brand:

| Sub-brand | Background | Accent | Logo token |
|---|---|---|---|
| Prestige | `#252E3F` | `#017FFF` | `{{LOGO_DSG_PRESTIGE}}` |
| Vision | `#252E3F` | `#0DB729` | `{{LOGO_DSG_VISION}}` |

### Typography

| Element | Font | Weight | Colour |
|---|---|---|---|
| H1 | Montserrat | SemiBold (600) | White |
| H2 | Montserrat | SemiBold (600) | White |
| H3 / accent text | Montserrat | Medium (500) | Sub-brand accent colour |
| Body | Fira Sans | Light (300) | White at 85-90% opacity |
| Bold body | Fira Sans | Medium (500) | White |
| Disclaimer | Fira Sans | Light (300) | White at 45% opacity |

Google Fonts load string for hcti.io / preview wrapper:
`Montserrat:500,600|Fira+Sans:300,500`

### Logos

Both `.b64` files already exist in `references/brand/logos/`:
- `dsg-prestige-dark.b64` — white wordmark + silver/grey chevron, for dark backgrounds
- `dsg-vision-dark.b64` — white wordmark + green chevron, for dark backgrounds

Use the `{{LOGO_DSG_PRESTIGE}}` or `{{LOGO_DSG_VISION}}` token in templates. render.py substitutes these automatically.

### Brand features and rules

- **Bullet points:** use the DSG chevron `›` (U+203A) styled in the sub-brand accent colour. Do not use orange dots (that is Magnitude).
- **Quotes:** large `"` mark top-left in Montserrat SemiBold in the sub-brand accent colour.
- **Rounded corners:** all inner boxes, cards, and featured sections must have `border-radius: 12px` minimum. No sharp corners.
- **Logo placement:** top-left or top-centre, horizontal only. Never angled, never stretched.
- **Accent bar:** 8-10px top bar in sub-brand accent colour (same pattern as Magnitude's orange bar).
- Never use Magnitude's orange (`#ED792B`) on DSG content.
- Never use DSG Prestige's Azure Blue on a DSG Vision card and vice versa.

### FCA disclaimer

DSG Financial Services Ltd is the entity directly (no "trading style" wrapper needed):

> We are a credit broker, not a lender. DSG Financial Services Ltd is authorised and regulated by the Financial Conduct Authority. FRN: 649675.

If a rate is quoted on the card, prepend: `[X.X%] APR Representative.`

---

## Workflow

### Step 1 — Pick the content type
Ask or infer. Common DSG card types:
- **Rate Watch** — lender rate news, useful for dealers
- **Lender Update** — policy change, new product, panel addition
- **Industry Insight** — FCA news, market update, plate changes
- **Dealer Tip** — underwriting insight, proposal tips
- **Testimonial** — dealer or employer quote card

### Step 2 — Get the details
Minimum questions. Don't over-ask.

**Rate Watch / Lender Update:** lender name, what changed, effective date, APR if quoted (needs representative APR in disclaimer)
**Industry Insight:** the angle, what it means for dealers
**Dealer Tip:** the tip, an example if helpful
**Testimonial:** quote text, attribution (name and company)

### Step 3 — Platform
WhatsApp dealer group / LinkedIn / both. DSG cards are primarily dealer-facing (B2B), not consumer.

### Step 4 — Draft the copy
- Straight-talking, plain English, dealer audience
- No jargon, no buzzwords
- UK English
- Never slag off lenders or competitors
- Value and clarity first
- FCA disclaimer always at the bottom of both image and post copy
- WhatsApp: 100-200 words, punchy
- LinkedIn: 150-300 words, slightly more considered

Run through `references/brand/social-post-checklist.md` before showing B. Show draft, iterate if needed.

### Step 5 — Build the card

#### If a matching template exists in `.claude/skills/dsg-social-content/templates/`:
Read it to get the token list, substitute all tokens, write `card.html` to the library.

#### If no matching template exists — build one first:
See the **Building a new template** section below. Design the template, save it to `.claude/skills/dsg-social-content/templates/[name].html`, then create the `card.html` from it.

**Save the working copy to the library:**

```
library/posts/dsg/YYYY-MM-DD-[slug]/card.html
```

The `card.html` is a complete HTML file with all tokens already substituted. No tokens remaining. B can open it directly in a browser, edit it between sessions, and pick up exactly where he left off.

**Preview (free, no hcti.io credits):**
```
python3 .claude/skills/magnitude-social-content/templates/render.py \
  --file library/posts/dsg/YYYY-MM-DD-[slug]/card.html \
  --local
```

**Render final PNG (one hcti.io credit):**
```
python3 .claude/skills/magnitude-social-content/templates/render.py \
  --file library/posts/dsg/YYYY-MM-DD-[slug]/card.html
```

PNG saves to the same folder as `card.html`.

### Step 6 — Archive locally (FCA)

Save `library/posts/dsg/YYYY-MM-DD-[slug]/post.md`:

```markdown
---
date: YYYY-MM-DD
brand: dsg-[prestige|vision]
pillar: [content type]
platforms: [WhatsApp / LinkedIn]
template: [template name or "bespoke"]
card: library/posts/dsg/YYYY-MM-DD-[slug]/card.png
source: [fresh / ideas.md]
---

## Copy
[Full post copy]

## FCA disclaimer used
[Exact disclaimer text from the card]
```

### Step 7 — Done
Show B the copy, local preview command, and archive path. Keep it short.

---

## Building a new template from scratch

When no existing template matches the content type, build one. Follow this recipe exactly.

### HTML skeleton

```html
<!--
DSG [Sub-brand] [Card type] template.
Size: 1080 x 1350 (portrait) or 1080 x 1080 (square).

Workflow: do not render this template directly.
1. Substitute all tokens and save to library/posts/dsg/YYYY-MM-DD-[slug]/card.html
2. Preview: python3 .claude/skills/magnitude-social-content/templates/render.py \
     --file library/posts/dsg/YYYY-MM-DD-[slug]/card.html --local
3. Render PNG: same command, drop --local.

Tokens:
  {{LOGO_DSG_PRESTIGE}} or {{LOGO_DSG_VISION}}  — logo (render.py inlines as base64)
  {{ACCENT}}            — sub-brand accent colour hex (e.g. #017FFF)
  [... other tokens specific to this card ...]

Rules:
1. Never use em or en dashes. render.py refuses to render if any slip in.
2. If a rate is quoted, DISCLAIMER must include representative APR matching the lowest quoted.
3. Rounded corners on all inner boxes (border-radius: 12px minimum).
-->
<div style="width:1080px;height:1350px;background:#252E3F;position:relative;overflow:hidden;
            font-family:'Fira Sans',sans-serif;box-sizing:border-box;padding:56px;">

  <!-- Top accent bar — sub-brand colour -->
  <div style="position:absolute;top:0;left:0;right:0;height:10px;background:{{ACCENT}};"></div>

  <!-- Logo, top left -->
  <div style="margin-bottom:40px;">
    <img src="{{LOGO_DSG_PRESTIGE}}" style="height:72px;" />
    <!-- swap to {{LOGO_DSG_VISION}} for Vision cards -->
  </div>

  <!-- === card body here === -->

  <!-- FCA disclaimer, pinned bottom -->
  <div style="position:absolute;bottom:32px;left:56px;right:56px;">
    <div style="height:1px;background:rgba(255,255,255,0.1);margin-bottom:14px;"></div>
    <div style="font-family:'Fira Sans',sans-serif;font-size:14px;font-weight:300;
                color:rgba(255,255,255,0.45);line-height:1.45;">{{DISCLAIMER}}</div>
  </div>

</div>
```

### Bullet chevron pattern (replaces Magnitude orange dots)

```html
<div style="display:flex;align-items:flex-start;margin-bottom:8px;">
  <span style="color:{{ACCENT}};font-weight:600;margin-right:12px;flex-shrink:0;">›</span>
  <span style="font-size:26px;line-height:1.45;">Copy here</span>
</div>
```

### H1 / H2 heading pattern

```html
<div style="font-family:Montserrat,sans-serif;font-size:48px;font-weight:600;
            color:#fff;margin-bottom:12px;">Heading here</div>
```

### H3 / accent heading pattern

```html
<div style="font-family:Montserrat,sans-serif;font-size:28px;font-weight:500;
            color:{{ACCENT}};margin-bottom:8px;">Section label here</div>
```

### Google Fonts string for render.py preview wrapper
`Montserrat:500,600|Fira+Sans:300,500`

Note: render.py's `--local` preview wrapper currently loads Poppins and Montserrat. When building a DSG template, confirm the preview wrapper includes Fira Sans. If not, the local preview will fall back to system sans-serif — hcti.io will still render correctly as long as the font string is correct in render.py's `payload`.

### Save the template
Once the template HTML is finalised with B:
- Save to `.claude/skills/dsg-social-content/templates/[descriptive-name].html`
- The template keeps `{{TOKEN}}` placeholders — never bake in actual content
- Document all tokens in the HTML comment block at the top

---

## Templates that exist today

None yet. First template will be built when the first DSG card is requested.

Candidates for first build (based on Magnitude equivalents):
- `rate-watch.html` — lender rate news (1080x1080 square, dealer-focused)
- `lender-update.html` — policy/product change announcement
- `dealer-tip.html` — underwriting or proposal tip card

---

## Vehicle image path convention

`card.html` files live at `library/posts/dsg/YYYY-MM-DD-[slug]/card.html`. Relative path to the vehicle library:

```
../../../vehicles/<make>/<filename>.png
```

render.py inlines all relative image paths as base64 data URIs before sending to hcti.io.

---

## Brand reminders (always apply)

- Background: `#252E3F` — never Magnitude's `#1A212E`
- Never use Magnitude's Burnt Orange `#ED792B` on DSG cards
- Accent colour is sub-brand specific: Azure Blue for Prestige, Apple Green for Vision
- Font stack: Montserrat for headings, Fira Sans for body
- All inner boxes: `border-radius: 12px` minimum
- Logo: horizontal only, never stretch
- FCA disclaimer: every card, every post, pinned to bottom
- DSG Financial Services Ltd is the FCA-registered entity — no "trading style" wrapper
