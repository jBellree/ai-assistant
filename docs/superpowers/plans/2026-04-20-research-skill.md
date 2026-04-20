# Research Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/bs:research` slash command + skill that pulls X (via Apify) and AutoTrader (via Apify) source material into structured markdown files in `research/`, behind a question-first gate so nothing is scraped without confirmation.

**Architecture:** Pure-config skill (markdown only, no Python). All logic lives in `SKILL.md` as instructions Claude follows in-session: question gates via `AskUserQuestion`, Apify calls via `curl`, response parsing into structured markdown by Claude itself, output written with the `Write` tool. Subagents only used when "Both" is picked or 3+ X queries fan out.

**Tech Stack:** Markdown configuration, Apify HTTP API (`apidojo/twitter-scraper-lite`, `epctex/autotrader-uk-scraper`), `curl`, `AskUserQuestion` tool, `superpowers:dispatching-parallel-agents` for fan-out.

**Spec reference:** [docs/superpowers/specs/2026-04-20-research-skill-design.md](../specs/2026-04-20-research-skill-design.md)

**Verification model:** This skill is configuration, not code, so there's no unit test framework. Each task ends with a manual verification step the executor runs (e.g. "open the file, confirm structure" or "fire the command in a fresh session, confirm gate appears"). The final task is an end-to-end smoke test through every branch of the workflow.

**Worktree note:** This project is a single-user assistant repo with no CI. Work directly on `main` (matches B's existing pattern, no worktree needed). Commit after each task.

---

## File Structure

**Create:**
- `.claude/skills/research/SKILL.md` — workflow instructions (the heart of the skill)
- `.claude/skills/research/config/x-queries.md` — editable X query list
- `.claude/skills/research/config/autotrader-watchlists/.gitkeep` — placeholder so folder exists; B adds watchlist files later
- `.claude/skills/research/config/autotrader-watchlists/EXAMPLE-defenders-under-100k.md` — annotated example watchlist
- `.claude/commands/bs/research.md` — slash command shim
- `research/x/.gitkeep` — output folder placeholder
- `research/autotrader/single/.gitkeep`
- `research/autotrader/searches/.gitkeep`
- `research/autotrader/watchlists/.gitkeep`

**Modify:**
- `CLAUDE.local.md` — add `APIFY_API_TOKEN=...` line under a new "Apify" section
- `.claude/skills/social-content/SKILL.md` — add 4th option to Step 0 (idea source): "From `research/` folder"
- `CLAUDE.md` — add `/bs:research` to the Commands section, add Research skill to the Skills section
- `.gitignore` — confirm `research/` is NOT ignored (output files commit alongside the rest of the assistant state)

---

## Task 1: Scaffold folders and add Apify token

**Files:**
- Modify: `CLAUDE.local.md`
- Create: `.claude/skills/research/config/autotrader-watchlists/.gitkeep`
- Create: `research/x/.gitkeep`
- Create: `research/autotrader/single/.gitkeep`
- Create: `research/autotrader/searches/.gitkeep`
- Create: `research/autotrader/watchlists/.gitkeep`

- [ ] **Step 1: Get the Apify token from B**

Ask B:
> "I need your Apify API token to add to CLAUDE.local.md. You can get it from https://console.apify.com/account/integrations — copy the 'Personal API token'. Paste it here when ready."

Wait for B to paste. Store as a variable in this session for the next step.

- [ ] **Step 2: Add the token to CLAUDE.local.md**

Open `CLAUDE.local.md`, append the following block at the bottom (preserving existing content):

```markdown
----------------------------------------------
Apify (X scraper, AutoTrader scraper)
----------------------------------------------

APIFY_API_TOKEN=<paste-the-token-from-step-1>

----------------------------------------------
----------------------------------------------
```

- [ ] **Step 3: Create the placeholder folders**

Run:

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
mkdir -p .claude/skills/research/config/autotrader-watchlists
mkdir -p research/x
mkdir -p research/autotrader/single
mkdir -p research/autotrader/searches
mkdir -p research/autotrader/watchlists
touch .claude/skills/research/config/autotrader-watchlists/.gitkeep
touch research/x/.gitkeep
touch research/autotrader/single/.gitkeep
touch research/autotrader/searches/.gitkeep
touch research/autotrader/watchlists/.gitkeep
```

- [ ] **Step 4: Verify the token works**

Test the token with a free Apify endpoint (no actor run, no cost):

```bash
source <(grep APIFY_API_TOKEN "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md" | head -1)
curl -s "https://api.apify.com/v2/users/me?token=$APIFY_API_TOKEN" | head -c 500
```

Expected output: a JSON blob that includes `"username":` and `"id":`. If you see `"error"` or HTTP 401, the token is wrong — go back to Step 1 and ask B for the correct one.

- [ ] **Step 5: Verify folder structure**

Run:

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
find .claude/skills/research research -type d | sort
```

Expected output (exact):

```
.claude/skills/research
.claude/skills/research/config
.claude/skills/research/config/autotrader-watchlists
research
research/autotrader
research/autotrader/searches
research/autotrader/single
research/autotrader/watchlists
research/x
```

- [ ] **Step 6: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/config/autotrader-watchlists/.gitkeep research/
git commit -m "Scaffold research skill folders"
```

Note: `CLAUDE.local.md` is git-ignored (it contains secrets), so it does NOT get committed. That's intentional. The token lives only on B's machine.

---

## Task 2: Create the slash command shim

**Files:**
- Create: `.claude/commands/bs/research.md`

- [ ] **Step 1: Read an existing command for the pattern**

Read `.claude/commands/bs/content.md` to see the exact frontmatter shape and trigger format used in this project. Match that pattern in Step 2.

- [ ] **Step 2: Write the research command file**

Create `.claude/commands/bs/research.md`:

```markdown
---
description: Pull research from X and/or AutoTrader into research/ folder
---

Run the `research` skill. The skill will ask question gates first (source pick, query/input details, cost preview) before any scraping fires. Never skip the gates.
```

- [ ] **Step 3: Verify file exists and is well-formed**

Run:

```bash
cat "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/commands/bs/research.md"
```

Expected: file content matches Step 2 exactly. Frontmatter has a `description:` line.

- [ ] **Step 4: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/commands/bs/research.md
git commit -m "Add /bs:research slash command"
```

---

## Task 3: Create the X queries config

**Files:**
- Create: `.claude/skills/research/config/x-queries.md`

- [ ] **Step 1: Write the config file**

Create `.claude/skills/research/config/x-queries.md`:

```markdown
---
queries:
  - name: pcp-watch
    type: keyword
    terms: ["PCP car finance", "balloon payment"]
    lang: en
  - name: fca-news
    type: keyword
    terms: ["FCA car finance", "FCA motor finance"]
    lang: en
  - name: industry-voices
    type: accounts
    handles: ["MotorFinanceMag", "FCA"]
---

# X Research Queries

Edit this file to add, remove, or change queries. The `name` field becomes the
output filename slug (e.g. `pcp-watch` → `research/x/2026-04-20-pcp-watch.md`).

## Query types

- `type: keyword` — pair with `terms: [...]` (one or more strings, OR'd together).
  Use double quotes around multi-word terms so they're treated as exact phrases.
- `type: accounts` — pair with `handles: [...]` (X handles WITHOUT the `@`).
  Pulls recent posts from those accounts.

Both types support `lang:` (default `en`) and inherit the time-window and
min-engagement filters chosen at runtime in the question gate.

## Adding a new query

1. Add a new `- name: ...` block above. Pick a slug-friendly name (lowercase,
   hyphens, no spaces).
2. Save the file.
3. Run `/bs:research` — the new query appears in the "pick one" list automatically.
```

- [ ] **Step 2: Verify YAML frontmatter parses**

Run:

```bash
python3 -c "
import yaml
with open('/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/config/x-queries.md') as f:
    raw = f.read()
fm = raw.split('---')[1]
data = yaml.safe_load(fm)
print('Queries found:', len(data['queries']))
for q in data['queries']:
    print(f\"  - {q['name']} ({q['type']})\")
"
```

Expected output:

```
Queries found: 3
  - pcp-watch (keyword)
  - fca-news (keyword)
  - industry-voices (accounts)
```

- [ ] **Step 3: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/config/x-queries.md
git commit -m "Add starter X queries config"
```

---

## Task 4: Create the example AutoTrader watchlist

**Files:**
- Create: `.claude/skills/research/config/autotrader-watchlists/EXAMPLE-defenders-under-100k.md`

- [ ] **Step 1: Write the example watchlist file**

Create `.claude/skills/research/config/autotrader-watchlists/EXAMPLE-defenders-under-100k.md`:

```markdown
---
name: defenders-under-100k
search_url: https://www.autotrader.co.uk/car-search?make=LAND%20ROVER&model=DEFENDER&price-to=100000
last_run: null
---

# Run history

(empty until first run)

---

## How to add a new watchlist

1. Copy this file. Name the new file `<your-watchlist-name>.md` (no `EXAMPLE-` prefix).
2. Edit the frontmatter:
   - `name`: same as the filename slug, lowercase with hyphens.
   - `search_url`: build the search on autotrader.co.uk in your browser, copy the full URL from the address bar.
   - `last_run`: leave as `null` until first run.
3. Save. The watchlist appears in `/bs:research` → AutoTrader → "Run a watchlist" automatically.

## Notes

- The skill will update `last_run` and append to `# Run history` after each run.
- "New since last run" is computed by diffing listing URLs against the previous run's output file in `research/autotrader/watchlists/`.
- The `EXAMPLE-` prefix on this file's name is what excludes it from the watchlist picker. Real watchlist files have no prefix.
```

- [ ] **Step 2: Verify file exists**

Run:

```bash
ls -la "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/config/autotrader-watchlists/"
```

Expected: shows `.gitkeep` and `EXAMPLE-defenders-under-100k.md`.

- [ ] **Step 3: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/config/autotrader-watchlists/EXAMPLE-defenders-under-100k.md
git commit -m "Add example AutoTrader watchlist"
```

---

## Task 5: Confirm the Apify actor field shapes

**Files:** No file changes. This task gathers data needed for Tasks 6-7.

This step exists because the spec flagged it as the one open question for the implementation phase — the parsers in the SKILL.md need to reference real field names from the Apify actors, not guesses.

- [ ] **Step 1: Run a tiny X scrape and inspect the response shape**

Run a one-tweet scrape using `apidojo/twitter-scraper-lite`:

```bash
source <(grep APIFY_API_TOKEN "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md" | head -1)
curl -s -X POST "https://api.apify.com/v2/acts/apidojo~twitter-scraper-lite/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["FCA car finance"],
    "maxItems": 2,
    "lang": "en"
  }' | python3 -m json.tool | head -80
```

Expected: a JSON array with 2 tweet objects. Note the exact field names for: tweet text, posted timestamp, like count, retweet count, tweet URL, author handle. Likely candidates per the actor's schema (verify against the actual response): `text` / `fullText`, `createdAt`, `likeCount` / `favoriteCount`, `retweetCount`, `url`, `author.userName` / `username`.

Write the confirmed field names down — you'll embed them into the SKILL.md parser instructions in Task 6.

- [ ] **Step 2: Run a tiny AutoTrader scrape and inspect the response shape**

Pick an arbitrary current AutoTrader search URL (e.g. one Defender listing) and run:

```bash
source <(grep APIFY_API_TOKEN "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md" | head -1)
curl -s -X POST "https://api.apify.com/v2/acts/epctex~autotrader-uk-scraper/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "search": "https://www.autotrader.co.uk/car-search?make=LAND%20ROVER&model=DEFENDER&price-to=100000",
    "maxItems": 2
  }' | python3 -m json.tool | head -100
```

Expected: a JSON array with 2 listing objects. Note the exact field names for: registration / number plate, date of first registration, make, model, derivative / variant, mileage, price, listing URL. Critical: confirm whether registration and DOR are first-class fields or whether they sit inside a free-text `keyFeatures` / `vehicleHistory` block (if the latter, the SKILL.md parser instructions need to extract them with regex).

Write the confirmed field shape down — you'll embed it into the SKILL.md parser instructions in Task 6.

- [ ] **Step 3: Note the actual costs**

Both responses include cost metadata in the Apify run summary. Check your Apify console at https://console.apify.com/actors/runs to see the exact `chargedEventsForDataset` cost for each test run. Use these as the basis for the cost estimates the skill shows at Gate 3.

Note (sample): X ~$X per Y tweets, AutoTrader ~$X per Y listings.

- [ ] **Step 4: No commit — this task produces notes, not files**

The notes from Steps 1-3 feed directly into Task 6's SKILL.md content. Keep them in your scratchpad.

---

## Task 6: Write the SKILL.md — gates and source dispatch

**Files:**
- Create: `.claude/skills/research/SKILL.md`

This task creates the SKILL.md scaffold and the question gates (Steps 0-3 of the workflow). Tasks 7 and 8 fill in the Apify execution, parsing, watchlist bookkeeping, and summary. Splitting the SKILL.md across three tasks keeps each commit focused and reviewable.

- [ ] **Step 1: Write the skeleton + Step 0 (token check) + Gates 1-3**

Create `.claude/skills/research/SKILL.md`:

```markdown
---
name: research
description: Pull source material for social content from X (Apify) and AutoTrader (Apify). Question-first gate, config-driven targets, structured markdown output saved to research/. Used by /bs:research.
---

# Skill: Research

## Trigger phrases
- `/bs:research`
- "research X"
- "research AutoTrader"
- "find me some content angles"
- "scrape AutoTrader"

## Purpose
Pull source material for B's social content from two channels:
1. **X (Twitter)** — industry chatter, FCA news, market trends
2. **AutoTrader** — live UK vehicle listings (B runs the actual finance quotes on his own broker stack)

Output saved to `research/x/` and `research/autotrader/` as structured markdown. Drafting is decoupled — B reviews saved research conversationally in any session, then hands off to `/bs:content` (which has a 4th idea source: "From research/ folder").

## Hard rules
- **Never call Apify without passing all three question gates and getting an explicit "yes" / "go" / "ok" at Gate 3.** B set this rule because Apify charges per-result and unfocused scrapes burn cash.
- **All gates use `AskUserQuestion`** (radio buttons). If the tool isn't loaded in this session, load it first with `ToolSearch` query `select:AskUserQuestion`.
- **No em or en dashes anywhere** (B's universal rule, applies even to scratch output).

## Context to load
- `.claude/skills/research/config/x-queries.md` — X query list (read at Gate 2 if X picked)
- `.claude/skills/research/config/autotrader-watchlists/*.md` — watchlists (read at Gate 2 if AutoTrader → watchlist picked). Files prefixed with `EXAMPLE-` are NOT real watchlists — exclude them from the picker.

## Workflow

### Step 0 — Token check (fail fast)

Before any gate, confirm `APIFY_API_TOKEN` is set in `CLAUDE.local.md`:

```bash
grep -q "^APIFY_API_TOKEN=" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md"
```

If grep returns non-zero, stop immediately and tell B:

> "I can't find `APIFY_API_TOKEN` in CLAUDE.local.md. Get one from https://console.apify.com/account/integrations and paste it here, then I'll add it for you."

Do not proceed to gates until the token is set.

### Step 1 — Gate 1: Source pick

Use `AskUserQuestion`:

- Question: "What do you want to research?"
- Header: "Source"
- Options:
  - "X" — "Pull recent posts from X queries (industry news, FCA, trends)."
  - "AutoTrader" — "Pull live UK vehicle listings."
  - "Both (parallel)" — "Run X and AutoTrader at the same time via subagents."

### Step 2 — Gate 2: Branch-specific follow-ups

Branch on Gate 1's answer.

#### If X:

1. Read `.claude/skills/research/config/x-queries.md`. Parse the YAML frontmatter into a list of query objects. Note their `name` values.

2. `AskUserQuestion`: "Which queries?"
   - Header: "X queries"
   - Options:
     - "All configured queries" — "Run every query in x-queries.md."
     - "Pick one" — "Pick a single query from the list."
     - "New ad-hoc query" — "Type a one-off keyword search, won't be saved to config."
   - If "Pick one" → second `AskUserQuestion` with one option per query name (max 4). If there are >4 queries, batch as: first 3 + "Show more" (recurse).
   - If "New ad-hoc query" → ask B in chat (free text) for the search terms.

3. `AskUserQuestion`: "How far back?"
   - Header: "Window"
   - Options: "24 hours", "7 days", "30 days"

4. `AskUserQuestion`: "Min engagement filter?"
   - Header: "Engagement"
   - Options: "None", "50+ likes", "200+ likes"

#### If AutoTrader:

1. `AskUserQuestion`: "What's the input?"
   - Header: "AT input"
   - Options:
     - "Paste a URL" — "A single AutoTrader listing URL."
     - "Ad-hoc search" — "Make/model/price ceiling/year — I'll build the search URL."
     - "Run a watchlist" — "Pick from saved watchlists in config/autotrader-watchlists/."

2. Per branch:
   - "Paste a URL" → ask B in chat for the AutoTrader listing URL. Validate it starts with `https://www.autotrader.co.uk/`.
   - "Ad-hoc search" → ask B for the criteria in chat (free text). Construct an AutoTrader search URL from the criteria.
   - "Run a watchlist" → list files in `.claude/skills/research/config/autotrader-watchlists/` excluding `.gitkeep` and anything starting with `EXAMPLE-`. If 0 real watchlists, tell B and offer to create one. If 1-4, show as `AskUserQuestion` options. If >4, batch with "Show more".

#### If Both:

Run the X branch (steps 1-4 above), then the AutoTrader branch (steps 1-2 above), in order. Collect all answers before moving to Gate 3.

### Step 3 — Gate 3: Cost preview

Build a preview block summarising every scrape that's about to fire:

```
About to scrape:
- X for `pcp-watch` query (terms: "PCP car finance", "balloon payment"), last 7 days, 50+ likes. Estimated ~80 results, ~$0.03.
- AutoTrader watchlist `defenders-under-100k`. Estimated ~12 results, ~$0.01.
Total estimated cost ~$0.04. Go?
```

Use rough cost rates from Task 5 Step 3 notes. Estimate result count conservatively (better to over-estimate than surprise B with a bigger bill).

`AskUserQuestion`:
- Question: "Fire the scrapes?"
- Header: "Confirm"
- Options:
  - "Go" — "Run the scrapes as previewed."
  - "Tweak first" — "Go back to the gates."
  - "Cancel" — "Abort, no scrapes."

Only on "Go" → proceed to Step 4 (next task: Apify execution).

### Step 4 — Apify execution

(Filled in by Task 7.)

### Step 5 — Parse and save

(Filled in by Task 7.)

### Step 6 — Watchlist bookkeeping

(Filled in by Task 8.)

### Step 7 — Summary and exit

(Filled in by Task 8.)
```

- [ ] **Step 2: Verify the file is well-formed**

Run:

```bash
head -30 "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: shows the YAML frontmatter, then `# Skill: Research`, then the trigger phrases section.

Run:

```bash
grep -c "^### Step" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: `8` (Steps 0 through 7).

- [ ] **Step 3: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/SKILL.md
git commit -m "Add research SKILL.md scaffold and question gates"
```

---

## Task 7: Fill in Steps 4-5 of SKILL.md — Apify execution and parsing

**Files:**
- Modify: `.claude/skills/research/SKILL.md` (replace placeholder Steps 4-5)

- [ ] **Step 1: Read the current SKILL.md to find the exact replace boundaries**

Read `.claude/skills/research/SKILL.md` and locate the `### Step 4 — Apify execution` and `### Step 5 — Parse and save` placeholder blocks added in Task 6.

- [ ] **Step 2: Replace Steps 4 and 5 with the full content**

Use `Edit` to replace the block from `### Step 4 — Apify execution` through (and including) the `(Filled in by Task 7.)` line under Step 5, with this content:

```markdown
### Step 4 — Apify execution

#### Single-source path (no parallelism)

Runs in the main session if any of these is true:
- Only X picked AND only one query (configured pick-one OR ad-hoc) → 1 scrape
- Only AutoTrader picked AND only one URL/search/watchlist → 1 scrape
- Only X picked, "All configured queries" with exactly 2 queries → 2 sequential scrapes (subagent overhead not worth it)

For each scrape:

**X (per query):**

```bash
source <(grep APIFY_API_TOKEN "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md" | head -1)

# Map the gate answers to actor params:
# - searchTerms: query.terms (keyword type) OR ["from:" + handle for handle in query.handles] (accounts type)
# - maxItems: 100 (or lower if scope is small)
# - lang: query.lang or "en"
# - sort: "Latest"
# Time window and min-engagement: applied client-side after fetch by Claude (the actor doesn't expose these natively in twitter-scraper-lite)

curl -sS --max-time 60 -X POST \
  "https://api.apify.com/v2/acts/apidojo~twitter-scraper-lite/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": [...],
    "maxItems": 100,
    "lang": "en",
    "sort": "Latest"
  }' \
  > /tmp/research-x-<query-name>.json

# Check exit status. If non-zero or output is empty, treat as a failure (see Failure handling below).
```

**AutoTrader (per input):**

```bash
source <(grep APIFY_API_TOKEN "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.local.md" | head -1)

# Map gate answers to actor params:
# - search: the full AutoTrader URL (single listing URL OR search results URL OR watchlist search_url)
# - maxItems: 50 (or lower if scope is small)

curl -sS --max-time 60 -X POST \
  "https://api.apify.com/v2/acts/epctex~autotrader-uk-scraper/run-sync-get-dataset-items?token=$APIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "search": "<full-url>",
    "maxItems": 50
  }' \
  > /tmp/research-at-<slug>.json
```

#### Parallel path (subagent fan-out)

Use the `superpowers:dispatching-parallel-agents` skill if any of these is true:
- "Both" picked at Gate 1 (one subagent for X side, one for AutoTrader side)
- X "All configured queries" with 3+ queries (one subagent per query)

Each subagent receives a self-contained brief: which actor, the exact `curl` body, the output file path, and the parsing instructions from Step 5 below. Subagent returns a one-line summary string. Do NOT have subagents update watchlist bookkeeping (Step 6) — the parent does that after all subagents return.

#### Failure handling

| Failure | Action |
|---|---|
| `curl` non-zero exit OR `--max-time` timeout | Report "Apify timeout for <scrape>". Continue with other scrapes. |
| Response is empty or `[]` | Tell B "0 results for <scrape>". Do NOT write an output file. |
| Response is malformed (not JSON) | Save raw to `research/<source>/_failed/YYYY-MM-DD-<slug>-raw.txt`. Report the failure. |
| Response is valid JSON but missing expected fields | Save raw to `research/<source>/_failed/...-raw.json`. Report. Do NOT guess field names. |

### Step 5 — Parse and save

For each successful scrape, parse the JSON and write a markdown file using the templates below. Use the field names confirmed in Task 5 (X actor: `text`, `createdAt`, `likeCount`, `retweetCount`, `url`, `author.userName` — confirm from your Task 5 notes; adjust if the actor returns different keys).

#### Output paths

| Scrape | Path pattern |
|---|---|
| X (configured query) | `research/x/YYYY-MM-DD-<query-name>.md` |
| X (ad-hoc query) | `research/x/YYYY-MM-DD-adhoc-<slugified-first-term>.md` |
| AutoTrader URL | `research/autotrader/single/YYYY-MM-DD-<make-model>-<stockNo>.md` |
| AutoTrader ad-hoc search | `research/autotrader/searches/YYYY-MM-DD-<search-slug>.md` |
| AutoTrader watchlist | `research/autotrader/watchlists/YYYY-MM-DD-<watchlist-name>.md` |

If the same path already exists for today (re-run on the same day), append `-2`, `-3`, etc.

#### Client-side filters (apply BEFORE writing)

For X scrapes:
- Time window: drop tweets where `createdAt` is older than the gate's window (24h / 7 days / 30 days).
- Min engagement: drop tweets where `likeCount` < threshold (50 or 200).

For AutoTrader scrapes: no client-side filtering, write all results.

#### X output template

```markdown
---
date: <YYYY-MM-DD>
source: x
query: <query name OR "adhoc">
terms: [<terms array>]
window: <24h | 7d | 30d>
min_engagement: <none | 50_likes | 200_likes>
result_count: <N after filtering>
apify_run_id: <runId from Apify response — the run-sync-get-dataset-items endpoint returns it in the X-Apify-Run-Id response header, OR leave blank if not captured>
cost_usd: <numeric, from Apify console or your Task 5 notes>
---

## Tweet 1
- **Handle:** @<userName>
- **Posted:** <createdAt formatted as YYYY-MM-DD HH:MM>
- **Engagement:** <likeCount> likes, <retweetCount> retweets
- **URL:** <url>
- **Text:** <text, escaped if it contains backticks>

## Tweet 2
...
```

If `result_count` is 0 after filtering, do NOT write the file. Report "0 results after filter" to B in the summary instead.

#### AutoTrader output template

```markdown
---
date: <YYYY-MM-DD>
source: autotrader
input_type: <url | search | watchlist>
input_ref: <the URL string OR search slug OR watchlist name>
result_count: <N>
apify_run_id: <runId>
cost_usd: <numeric>
---

## Listing 1
- **Reg:** <registration if present, else "(not shown)">
- **DOR:** <date of registration, format YYYY-MM-DD if parseable>
- **Make / Model:** <make> <model>
- **Derivative:** <derivative / variant>
- **Mileage:** <mileage with comma separators, e.g. 24,500>
- **Price:** £<price with comma separators>
- **Link:** <listing URL>

## Listing 2
...
```

If a field is genuinely missing from the Apify response (e.g. registration not shown on the AutoTrader listing), write `(not shown)` — do NOT invent values or omit the bullet.
```

- [ ] **Step 3: Verify the edit landed cleanly**

Run:

```bash
grep -c "^### Step" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: `8` (still all 8 step headings).

Run:

```bash
grep "Filled in by Task" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: only Steps 6 and 7 still show `(Filled in by Task 8.)`. Step 5 should NOT match anymore.

- [ ] **Step 4: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/SKILL.md
git commit -m "Add research skill Apify execution and parsing steps"
```

---

## Task 8: Fill in Steps 6-7 of SKILL.md — watchlist bookkeeping and summary

**Files:**
- Modify: `.claude/skills/research/SKILL.md` (replace placeholder Steps 6-7)

- [ ] **Step 1: Replace Steps 6 and 7**

Use `Edit` to replace the block from `### Step 6 — Watchlist bookkeeping` through (and including) the `(Filled in by Task 8.)` line under Step 7, with this content:

```markdown
### Step 6 — Watchlist bookkeeping (AutoTrader watchlist runs only)

For each watchlist run that wrote an output file in Step 5, update the watchlist's config file:

1. Read `.claude/skills/research/config/autotrader-watchlists/<name>.md`.
2. Compute "new since last run" by reading the previous run's output file (most recent file in `research/autotrader/watchlists/` matching `*-<name>.md` excluding the one just written) and diffing listing URLs.
3. Update frontmatter `last_run` to today's date (YYYY-MM-DD).
4. Append one line to the `# Run history` section:

```
- YYYY-MM-DD: <result_count> results, <new_count> new since last run
```

If this is the first run (no previous output file), the line is:

```
- YYYY-MM-DD: <result_count> results, first run
```

This step runs in the parent session, never in subagents, so the watchlist file gets exactly one update per run.

### Step 7 — Summary and exit

Show B in chat:

```
Research run complete.

✓ X / pcp-watch: 12 tweets → research/x/2026-04-20-pcp-watch.md ($0.04)
✓ AutoTrader / defenders-under-100k watchlist: 14 listings (3 new) → research/autotrader/watchlists/2026-04-20-defenders-under-100k.md ($0.01)
✗ X / fca-news: 0 results after 50_likes filter (no file written)

Total cost: $0.05.

Say `/bs:content` and pick "From research/ folder" when you want to draft a post off any of this.
```

(Use ✓/✗ as plain Unicode, no emojis.)

Then exit. Do NOT auto-fire `/bs:content`. Decoupling is deliberate — B may want to scan multiple research files across days before picking an angle.
```

- [ ] **Step 2: Verify no placeholders remain**

Run:

```bash
grep "Filled in by Task" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: no output (all placeholders replaced).

Run:

```bash
wc -l "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/research/SKILL.md"
```

Expected: somewhere between 200 and 300 lines.

- [ ] **Step 3: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/research/SKILL.md
git commit -m "Add research skill watchlist bookkeeping and summary steps"
```

---

## Task 9: Wire research/ into /bs:content as a 4th idea source

**Files:**
- Modify: `.claude/skills/social-content/SKILL.md` (Step 0 only)

- [ ] **Step 1: Read the current Step 0 to locate the edit**

Read lines 36-45 of `.claude/skills/social-content/SKILL.md` to find the exact text of Step 0's three-option list.

- [ ] **Step 2: Add the 4th option**

Use `Edit` to modify the Step 0 list. The current text (around line 38-40) reads:

```markdown
1. **Saved RSS article** — Claude reads Airtable `Articles` table (base `appwPT59GISaH3phA`, table `tblvNFPoyugMVT9FL`), filters to Status in (`Manual Idea`, `Idea`, `Saved Ideas` view), shows the list — B picks one. Capture the `recordId` for the archive + status update later.
2. **From `ideas.md` backlog** — Claude reads `projects/social-content/ideas.md`, shows recent entries grouped by audience, B picks one.
3. **Fresh idea** — B describes it inline. Claude appends a line to `ideas.md` as it goes.
```

Replace with:

```markdown
1. **Saved RSS article** — Claude reads Airtable `Articles` table (base `appwPT59GISaH3phA`, table `tblvNFPoyugMVT9FL`), filters to Status in (`Manual Idea`, `Idea`, `Saved Ideas` view), shows the list — B picks one. Capture the `recordId` for the archive + status update later.
2. **From `ideas.md` backlog** — Claude reads `projects/social-content/ideas.md`, shows recent entries grouped by audience, B picks one.
3. **Fresh idea** — B describes it inline. Claude appends a line to `ideas.md` as it goes.
4. **From `research/` folder** — Claude lists `.md` files in `research/x/` and `research/autotrader/**/` (including `single/`, `searches/`, `watchlists/`; excluding any `_failed/` subfolder), newest-first, B picks one. The selected file's content loads as the angle/context for Step 1 (pillar pick) onwards. Source path: populated by `/bs:research`.
```

- [ ] **Step 3: Verify the edit landed**

Run:

```bash
grep -A 1 "From .research/. folder" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/.claude/skills/social-content/SKILL.md"
```

Expected: shows the new 4th option line.

- [ ] **Step 4: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add .claude/skills/social-content/SKILL.md
git commit -m "Wire research/ folder into /bs:content as 4th idea source"
```

---

## Task 10: Update CLAUDE.md (commands and skills sections)

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read CLAUDE.md to find the Commands and Skills sections**

Read `CLAUDE.md`, specifically the "Current commands:" list and the "Skills" section (under `## Skills`).

- [ ] **Step 2: Add `/bs:research` to the Commands list**

Find the existing "Current commands:" block (around lines 51-57). It currently ends with:

```markdown
- `/bs:calls` -- today's dealer call priorities (Airtable Call Planner, read-only)
```

Add a new line after it:

```markdown
- `/bs:research` -- pull source material from X (Apify) and AutoTrader (Apify) into research/ folder (question-first gate, never scrapes without confirmation)
```

- [ ] **Step 3: Add the research skill to the Skills section**

In the `## Skills` section, the current text says skills live in `.claude/skills/`. Add a new explicit reference under that section, after the "Skills to Build (Backlog)" list. Append a new subsection:

```markdown
### Active skills

- `social-content` -- branded social posts (copy + Gemini image + hcti.io card + FCA archive + Airtable update)
- `daily-planning` -- morning check-in, Apple Reminders triage
- `research` -- on-demand research from X and AutoTrader via Apify, output to research/. Used by /bs:research and feeds /bs:content via the "From research/ folder" idea source.
```

If an `### Active skills` section already exists, just add the `research` line to it instead of creating a duplicate.

- [ ] **Step 4: Verify both edits**

Run:

```bash
grep "/bs:research" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.md"
```

Expected: at least one match (the Commands list line).

Run:

```bash
grep "research.*on-demand research" "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/CLAUDE.md"
```

Expected: one match (the Skills section line).

- [ ] **Step 5: Commit**

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git add CLAUDE.md
git commit -m "Document /bs:research command and research skill in CLAUDE.md"
```

---

## Task 11: End-to-end smoke test

**Files:** No file changes. Manual verification across all branches.

This task verifies the skill works end-to-end. Each step is a real run through `/bs:research` in a fresh session. Stop and report any failure immediately — don't try to "fix in place."

- [ ] **Step 1: Smoke test — single X query**

Open a fresh Claude Code session in the AI Assistant project. Type: `/bs:research`.

Expected sequence:
1. Token check passes silently.
2. Gate 1 appears (radio: X / AutoTrader / Both). Pick **X**.
3. Gate 2: query picker appears. Pick **"Pick one"** → pick **fca-news**.
4. Gate 2: window picker appears. Pick **7 days**.
5. Gate 2: engagement picker appears. Pick **None**.
6. Gate 3: cost preview shows estimated count and cost. Pick **Go**.
7. Apify call fires. Output file written to `research/x/YYYY-MM-DD-fca-news.md`.
8. Summary in chat shows the file path and cost.

Verify the output file:

```bash
ls -la "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant/research/x/" | tail -5
```

Open the newest file. Confirm:
- Frontmatter has `source: x`, `query: fca-news`, `result_count: <N>`, `cost_usd: <number>`.
- Body has one `## Tweet N` block per tweet with all five bullets (Handle, Posted, Engagement, URL, Text).

If any step fails, report and stop.

- [ ] **Step 2: Smoke test — AutoTrader URL paste**

Same project, fresh session. Type: `/bs:research`.

Pick **AutoTrader** at Gate 1, then **Paste a URL**. Paste any current AutoTrader listing URL (find one on autotrader.co.uk in your browser). Pass Gate 3.

Verify the output file in `research/autotrader/single/`. Confirm all 8 listing fields are present (Reg, DOR, Make/Model, Derivative, Mileage, Price, Link), with `(not shown)` where the listing genuinely lacks a field.

- [ ] **Step 3: Smoke test — AutoTrader watchlist (first run)**

Create a real watchlist file (not the `EXAMPLE-` one):

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
cp .claude/skills/research/config/autotrader-watchlists/EXAMPLE-defenders-under-100k.md \
   .claude/skills/research/config/autotrader-watchlists/defenders-under-100k.md
```

(B may also choose a different make/model — adjust the filename and frontmatter `name` + `search_url` accordingly.)

Fresh session. Type `/bs:research`. Pick **AutoTrader → Run a watchlist → defenders-under-100k**. Pass Gate 3.

Verify:
- Output file written to `research/autotrader/watchlists/`.
- The watchlist config file (`config/autotrader-watchlists/defenders-under-100k.md`) now has `last_run:` set to today AND a new line under `# Run history` saying `<N> results, first run`.

- [ ] **Step 4: Smoke test — watchlist second run (diff logic)**

Same session OR fresh, type `/bs:research` again. Pick the same watchlist. Pass Gate 3.

Verify the watchlist config now has TWO history lines, the second saying `<N> results, <K> new since last run`. The `<K>` value should be small (most listings are unchanged between runs minutes apart).

- [ ] **Step 5: Smoke test — "Both" parallel branch**

Fresh session. Type `/bs:research`. Pick **Both**. Walk through the X branch (single query, 7 days, none) and the AutoTrader branch (URL paste, use the same URL as Step 2). Pass Gate 3.

Verify in the summary that BOTH scrapes ran in parallel (the agent should mention dispatching subagents). Verify both output files exist with today's date.

- [ ] **Step 6: Smoke test — handoff to /bs:content**

Fresh session. Type `/bs:content`. At Step 0, the menu should now show 4 options (RSS / ideas.md / Fresh / **From research/ folder**). Pick option 4.

Verify the picker lists the files written in Steps 1-5, newest first. Pick one. Confirm the skill loads its content as the angle/context for Step 1 (pillar pick) and proceeds normally.

- [ ] **Step 7: Smoke test — failure paths**

Test the missing-token failure:
1. Comment out the `APIFY_API_TOKEN` line in `CLAUDE.local.md` (prefix with `#`).
2. Fresh session, type `/bs:research`.
3. Expected: skill stops at Step 0, tells you the token is missing, doesn't show Gate 1.
4. Restore the token line.

Test the cancel path:
1. Fresh session, type `/bs:research`. Walk to Gate 3. Pick **Cancel**.
2. Expected: skill exits cleanly, no Apify call, no files written.

- [ ] **Step 8: Final commit**

If anything was tweaked during smoke testing (which the spec didn't anticipate), commit it now with a clear message. Otherwise, no commit needed — Task 11 is verification only.

```bash
cd "/Users/brianrothwell/Library/CloudStorage/Dropbox/AI Development/AI Assistant"
git status
```

Expected: clean working tree (or only smoke-test artefacts in `research/` to optionally commit).

---

## Done

After Task 11 passes all 7 smoke-test steps, the research skill is shippable. Tell B:

> "Research skill is live. Type `/bs:research` in any session. The first 7 smoke tests passed end-to-end. The watchlist for `defenders-under-100k` is set up — add more by copying the EXAMPLE file in `.claude/skills/research/config/autotrader-watchlists/`."
