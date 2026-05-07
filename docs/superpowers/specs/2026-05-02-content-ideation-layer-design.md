# Content Ideation Layer — Design Spec
_2026-05-02_

## Context

B creates social content for two brands (Magnitude Finance, DSG Financial Services) across three platforms (WhatsApp dealer group, LinkedIn, Instagram). The existing workflow has two content skills — `magnitude-social-content` and `dsg-social-content` — that produce polished posts and branded cards. What's been missing is a structured way to surface ideas before drafting begins.

Ideas come from multiple sources: YouTube videos, X (Twitter) industry threads, PLAUD voice note transcripts, and B's own daily work (deals funded, tricky cases solved). This spec defines a content ideation layer that sits upstream of the existing content skills, captures raw material from any source, generates ideas collaboratively, and hands off to the appropriate brand skill when ready.

---

## Architecture

Five skills: one orchestrator, four source sub-skills.

```
.claude/skills/
├── bs-ideate/              ← orchestrator
│   └── SKILL.md
├── youtube-content/        ← YouTube sub-skill
│   ├── SKILL.md
│   └── fetch_transcript.py
├── x-content/              ← X sub-skill (Apify)
│   ├── SKILL.md
│   └── fetch_x.py
├── plaud-content/          ← PLAUD transcript sub-skill
│   └── SKILL.md
└── daily-capture/          ← conversational daily sub-skill
    └── SKILL.md
```

All ideas land in `projects/social-content/ideas.md`. RSS articles stay in Airtable Content Hub unchanged. No migration needed.

---

## Orchestrator: `/bs:ideate`

### Trigger
Phrase: "ideate", "content ideas", "what should I post", `/bs:ideate`

### Flow

1. **Pick source** — `AskUserQuestion` with radio buttons:
   - YouTube video
   - X (motor finance news)
   - PLAUD transcript
   - My day / a deal I worked

2. **Invoke sub-skill** — the sub-skill handles all fetching and returns 4-6 raw ideas to the orchestrator.

3. **Present and iterate** — Claude shows the ideas. B gives feedback. Claude edits, merges, reangles specific ideas. Iteration continues until B is happy. One session may produce 1-4 finalised ideas.

4. **For each finalised idea, confirm:**
   - Brand: Magnitude or DSG?
   - Platform(s): WhatsApp / LinkedIn / Instagram / multiple?

5. **Save to `ideas.md`** — all ideas from the session (finalised and discarded) logged with source metadata and status.

6. **Hand off** — for each finalised idea, Claude invokes `magnitude-social-content` or `dsg-social-content` to produce copy, card, and archive. Ideation session ends.

---

## Sub-skill: `youtube-content`

### Trigger
Invoked by `bs-ideate` when YouTube is selected. Not invoked directly by B.

### Flow
1. Ask for YouTube URL
2. Run `fetch_transcript.py <url>` — returns plain text transcript
3. Claude reads transcript against content pillars, tone of voice, buyer personas
4. Returns 4-6 ideas to orchestrator

### `fetch_transcript.py`
- Library: `youtube-transcript-api` (PyPI, no API key)
- Extracts video ID from any YouTube URL format
- Fetches auto-generated captions
- Returns clean plain text to stdout
- No API keys in script — Claude calls it as a subprocess

### Known limitations
- Private or age-restricted videos will not work
- Auto-generated captions may have errors on heavy accents or fast speech
- Very short videos (under 2 min) may have no captions

---

## Sub-skill: `x-content`

### Trigger
Invoked by `bs-ideate` when X is selected. Not invoked directly by B.

### Flow
1. Run `fetch_x.py` — no input needed, searches are fixed
2. Script calls Apify X scraper actor, runs 5 fixed queries, returns top posts
3. Claude reads results against content pillars, tone of voice, buyer personas
4. Returns 4-6 ideas to orchestrator

### Fixed search queries (baked into `fetch_x.py`)
- "motor finance UK"
- "car finance UK"
- "FCA motor finance"
- "used car market UK"
- "PCP finance UK"

### `fetch_x.py`
- Library: `apify-client` (PyPI)
- API key: `APIFY_API_KEY` — stored in `CLAUDE.local.md`, read by Claude at runtime and passed to the subprocess via `os.environ`. Never hardcoded in the script.
- Fetches top 10-15 posts per query, deduplicates, returns clean text summary
- No idea generation in Python — Claude does that in-session

### Apify setup
B already has an Apify account. `APIFY_API_KEY` needs adding to `CLAUDE.local.md` before first use.

---

## Sub-skill: `plaud-content`

### Trigger
Invoked by `bs-ideate` when PLAUD transcript is selected. Not invoked directly by B.

### Flow
1. Ask B to paste the PLAUD transcript
2. Claude reads transcript against content pillars, tone of voice, buyer personas
3. Returns 4-6 ideas to orchestrator

### No Python scripts needed
PLAUD transcripts arrive as pasted text. No external dependencies.

### Note on PLAUD integration
Currently paste-in. Future upgrade path: if PLAUD exports to a known file path, the sub-skill can be updated to read the file directly. Design for paste-in now.

---

## Sub-skill: `daily-capture`

### Trigger
Invoked by `bs-ideate` when "My day / a deal I worked" is selected. Not invoked directly by B.

### Flow
1. Claude asks 3-4 conversational questions to draw out the detail:
   - What was the vehicle?
   - What made the deal or situation unusual?
   - What would a dealer learn from this?
   - What would a buyer take away?
2. Claude reads answers against content pillars, tone of voice, buyer personas
3. Returns 4-6 ideas to orchestrator

### No Python scripts needed
Fully conversational. No external dependencies.

---

## Idea Generation — shared approach across all sub-skills

All sub-skills use the same generation logic. Claude reads the source material against:
- `references/content-pillars.md`
- `references/brand/tone-of-voice.md`
- `references/brand/buyer-persona.md`
- `.claude/rules/content-guidelines.md`

For each idea, Claude produces:
| Field | Description |
|---|---|
| Pillar | One of the 5 content pillars |
| Audience | Dealer WhatsApp / LinkedIn D2C / Instagram / multiple |
| Angle | The specific hook that makes this worth posting |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

---

## `ideas.md` — data format

File: `projects/social-content/ideas.md`

Every idea from every source is logged here. Status tracks progression through the pipeline.

### Entry format

```markdown
## 2026-05-02 | YouTube | Magnitude | LinkedIn

**Source:** https://youtu.be/qBoShOFyl8M
**Pillar:** Underwriting Masterclass
**Status:** Saved

### Idea: Why dealers fear older diesels — and why finance still works

The angle: Car Dealer Magazine video flagged EcoBoom and Mazda 2.2 as
"scary" stock. Real talk: lenders still fund these with the right case.

**Hook:** "Dealers are avoiding certain engines. Here's what I'd actually do with one."

---
```

### Status values
- `Saved` — logged, not yet drafted
- `Drafted` — handed off to content skill, copy in progress
- `Posted` — published, FCA archive complete
- `Killed` — discarded, kept for reference

Status is updated by the content skills when a post ships, or manually when an idea is killed.

---

## Handoff to content skills

When B approves a finalised idea, `bs-ideate` invokes the appropriate brand skill:
- Magnitude content → `magnitude-social-content`
- DSG content → `dsg-social-content`

The ideation session ends at this point. The brand skill takes over from Step 1 of its own workflow, with the idea angle and hook pre-populated.

The `ideas.md` status for the idea is updated to `Drafted` at handoff.

---

## Dependencies

| Dependency | Install | Key required | Where key lives |
|---|---|---|---|
| `youtube-transcript-api` | `pip install youtube-transcript-api` | No | N/A |
| `apify-client` | `pip install apify-client` | Yes — `APIFY_API_KEY` | `CLAUDE.local.md` |

No Anthropic API key needed in Python — Claude generates ideas in-session.

---

## Verification

1. Run `/bs:ideate`, select YouTube, paste `https://youtu.be/qBoShOFyl8M` — confirm 4-6 ideas generated
2. Run `/bs:ideate`, select X — confirm `fetch_x.py` runs, results returned, ideas generated
3. Run `/bs:ideate`, select PLAUD — confirm paste flow works, ideas generated
4. Run `/bs:ideate`, select My day — confirm conversational flow draws out ideas
5. Iterate an idea — confirm Claude edits specific ideas without regenerating the full list
6. Confirm finalised idea saves correctly to `ideas.md` with correct format and status
7. Confirm handoff to `magnitude-social-content` or `dsg-social-content` works cleanly
8. Confirm discarded ideas also save to `ideas.md` with status `Killed`
