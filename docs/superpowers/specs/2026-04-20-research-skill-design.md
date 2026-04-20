# Research Skill — Design Spec

**Date:** 2026-04-20
**Status:** Approved, ready for implementation plan
**Owner:** B
**Related:** [.claude/skills/social-content/SKILL.md](../../../.claude/skills/social-content/SKILL.md), [projects/social-content/](../../../projects/social-content/)

## Purpose

A research agent that pulls source material for B's social content from two channels:

1. **X (Twitter)** — industry chatter, FCA news, market trends
2. **AutoTrader** — live UK vehicle listings B can run real finance quotes against on his own broker stack

Output is saved to a structured `research/` folder. Drafting is decoupled — B reviews the saved research conversationally in any session, then hands off to the existing `/bs:content` flow when ready to draft a post.

## Why this exists

B's #1 priority is consistency. The biggest blocker to consistent posting is "I don't know what to post about today." This skill turns that into a one-command research run that produces a small pile of concrete, source-backed angles to choose from.

Today the only structured idea sources are: the RSS-curated Articles table in Airtable, the `ideas.md` backlog, or fresh ideas. None of those surface live X conversations or live vehicle listings. This skill closes that gap.

## Scope

**In scope:**
- New skill at `.claude/skills/research/SKILL.md`
- New slash command `/bs:research` at `.claude/commands/bs/research.md`
- Apify integration for both X and AutoTrader scrapers
- Editable config files for X queries and AutoTrader watchlists
- Structured markdown output saved to `research/`
- Single-line addition to `social-content/SKILL.md` Step 0 to add a 4th idea source ("From research/ folder")
- Subagent fan-out for parallel scraping ("both" source pick, or multiple X queries)

**Out of scope (deliberately):**
- Quote calculation. B runs quotes on his own broker systems. The skill only extracts vehicle data.
- Scheduled / background runs. On-demand only — fires when B types `/bs:research`.
- A standalone "research review" skill. Reviewing saved research is just Claude reading markdown files in any session.
- Updating Airtable. Research output stays in the local filesystem.
- FCA paper trail. Research files are working notes, not published content.

## Architecture

### Files to create

```
.claude/
├── skills/
│   └── research/
│       ├── SKILL.md
│       └── config/
│           ├── x-queries.md                     # editable list of X queries
│           └── autotrader-watchlists/
│               └── .gitkeep                     # B adds watchlist files here over time
└── commands/
    └── bs/
        └── research.md                          # triggers the skill

research/                                        # new top-level folder, output destination
├── x/
└── autotrader/
    ├── single/
    ├── searches/
    └── watchlists/
```

### Files to modify

- `.claude/skills/social-content/SKILL.md` — add 4th option to Step 0 (idea source): "From `research/` folder"
- `CLAUDE.local.md` — add `APIFY_API_TOKEN`
- `CLAUDE.md` — add `/bs:research` to the Commands section, add Research skill to the Skills section

## Workflow

### Step 0 — Question gate (always runs first, no exceptions)

The skill **never** fires Apify without explicit confirmation. All gates use the `AskUserQuestion` tool (radio buttons, B's stated preference for multi-gate flows). If `AskUserQuestion` is not loaded in session, load it with `ToolSearch` query `select:AskUserQuestion` at the top of the workflow.

**Gate 1 — Source pick:**

> "What do you want to research?"
> - X
> - AutoTrader
> - Both (parallel)

**Gate 2 — Branch-specific follow-ups (one or more `AskUserQuestion` calls per branch):**

If **X**:
- "Run all configured queries, or a specific one?" — All / Pick one / New ad-hoc query
- "How far back?" — 24h / 7 days / 30 days
- "Min engagement filter?" — None / 50+ likes / 200+ likes

If **AutoTrader**:
- "What's the input?" — Paste a URL / Ad-hoc search / Run a watchlist
  - URL → text input for the AutoTrader listing URL
  - Ad-hoc search → text input for search criteria (make/model/price ceiling/year), agent constructs an AutoTrader search URL
  - Watchlist → list available watchlists from `config/autotrader-watchlists/`, B picks

If **Both**: run gate 2 for X then gate 2 for AutoTrader, in order, before any scraping.

**Gate 3 — Final preview before firing Apify:**

> "About to scrape:
> - X for `pcp-watch` query (terms: PCP car finance, balloon payment), last 7 days, 50+ likes. Estimated ~80 results, ~$0.03.
> - AutoTrader watchlist `defenders-under-100k`. Estimated ~12 results, ~$0.01.
> Total estimated cost ~$0.04. Go?"

Only on explicit "yes" / "go" / "ok" does the skill call Apify.

### Step 1 — Run Apify

**Single-source path** (just X or just AutoTrader, single query / single URL / single watchlist) — runs in the main session, no subagent.

**Parallel path** (Both selected, or multiple X queries via "All configured queries"):
- Use the `superpowers:dispatching-parallel-agents` skill
- One subagent per scrape job
- Each subagent: calls Apify, parses the result, writes its own output file, returns a one-line summary to the parent
- Main session aggregates summaries and shows them together

**Apify call mechanics:**
- Token in `CLAUDE.local.md` as `APIFY_API_TOKEN`
- Plain `curl` to `https://api.apify.com/v2/acts/<actor>/run-sync-get-dataset-items?token=$APIFY_API_TOKEN`
- No SDK, no extra deps — keeps the skill portable
- Actors:
  - X: `apidojo/twitter-scraper-lite`
  - AutoTrader: `epctex/autotrader-uk-scraper`
- 60-second timeout per call

### Step 2 — Parse and save

Each scrape produces one markdown file with YAML frontmatter (provenance) and a structured body (per-result blocks).

**X output** — `research/x/YYYY-MM-DD-<query-name>.md`:

```markdown
---
date: 2026-04-20
source: x
query: pcp-watch
terms: ["PCP car finance", "balloon payment"]
window: 7d
min_engagement: 50_likes
result_count: 12
apify_run_id: abc123
cost_usd: 0.04
---

## Tweet 1
- **Handle:** @SomeJournalist
- **Posted:** 2026-04-19 14:22
- **Engagement:** 340 likes, 41 retweets
- **URL:** https://x.com/...
- **Text:** "FCA just dropped guidance on PCP affordability tests..."

## Tweet 2
...
```

**AutoTrader output** — same frontmatter pattern, different body:

```markdown
---
date: 2026-04-20
source: autotrader
input_type: watchlist          # or "url" or "search"
input_ref: defenders-under-100k
result_count: 14
apify_run_id: def456
cost_usd: 0.01
---

## Listing 1
- **Reg:** AB12 CDE
- **DOR:** 2022-03-15
- **Make / Model:** Land Rover Defender
- **Derivative:** 90 D250 X-Dynamic SE
- **Mileage:** 24,500
- **Price:** £78,995
- **Link:** https://www.autotrader.co.uk/car-details/...

## Listing 2
...
```

**Filename slug** (X, configured query): `YYYY-MM-DD-<query-name>.md` (the `name` field from `x-queries.md`).
**Filename slug** (X, ad-hoc query): `YYYY-MM-DD-adhoc-<slugified-first-term>.md` (e.g. `2026-04-20-adhoc-pcp-affordability.md`).
**Filename slug** (AutoTrader single URL): `YYYY-MM-DD-<make>-<model>-<stockNo>.md`.
**Filename slug** (AutoTrader search): `YYYY-MM-DD-<search-slug>.md`.
**Filename slug** (AutoTrader watchlist): `YYYY-MM-DD-<watchlist-name>.md`.

### Step 3 — Watchlist bookkeeping (AutoTrader watchlist runs only)

After a watchlist run, the skill updates the watchlist file's frontmatter `last_run` and appends a one-line entry to its run history block:

```yaml
---
name: defenders-under-100k
search_url: https://www.autotrader.co.uk/car-search?make=LAND%20ROVER&model=DEFENDER&price-to=100000
last_run: 2026-04-20
---

# Run history
- 2026-04-20: 14 results, 3 new since last run
- 2026-04-18: 11 results, first run
```

"New since last run" is computed by diffing listing URLs against the previous run's output file.

### Step 4 — Show summary, exit

After all scrapes finish, the skill shows B in chat:
- One line per scrape: source, query/input, result count, output file path, cost
- Total cost for the run
- A reminder: "Say `/bs:content` and pick 'From research/ folder' when you want to draft a post off any of this."

The skill does **not** auto-handoff to `/bs:content`. Decoupling is deliberate — B may want to scan multiple research files across days before picking an angle.

## Config file formats

### `x-queries.md`

```yaml
---
queries:
  - name: pcp-watch
    type: keyword
    terms: ["PCP car finance", "balloon payment"]
    lang: en
  - name: fca-news
    type: keyword
    terms: ["FCA car finance", "FCA motor finance"]
  - name: industry-voices
    type: accounts
    handles: ["MotorFinanceMag", "FCA"]
---

Notes for B: add new queries above. `name` becomes the output filename slug.
Use `type: keyword` with a `terms` list, or `type: accounts` with a `handles` list.
```

### `autotrader-watchlists/<name>.md`

```yaml
---
name: defenders-under-100k
search_url: https://www.autotrader.co.uk/car-search?make=LAND%20ROVER&model=DEFENDER&price-to=100000
last_run: null
---

# Run history
(empty until first run)
```

B builds search URLs by running the search on autotrader.co.uk in a browser and copying the URL. The skill never constructs watchlist URLs from scratch — only from B-defined input.

## Handoff to `/bs:content`

The existing skill `.claude/skills/social-content/SKILL.md` Step 0 currently lists 3 idea sources:
1. Saved RSS article (Airtable)
2. `ideas.md` backlog
3. Fresh idea

Add a 4th:
4. **From `research/` folder** — list files in `research/x/` and `research/autotrader/` (excluding `watchlists/`), newest-first, B picks one. The selected file's content gets loaded as the angle/context for Step 1 (pillar pick) onwards.

This is the only change to `social-content/SKILL.md`. The rest of that skill (pillar pick, copy gen, image gen, branded card, archive, Airtable update) is untouched.

## Conversational review

No additional skill or command needed. In any session B can say things like:
- "What did I pull from X this week?"
- "Show me the Defender watchlist results"
- "Anything in research from the last 3 days worth posting?"

Claude reads the relevant files in `research/` directly. Markdown frontmatter + per-result blocks make this cheap to scan and easy to summarise.

## Subagent strategy

The skill uses subagents only when there's real parallelism to win. Subagents add latency (a few seconds per dispatch) and main-session token overhead (the parent has to summarise their results), so single-source single-query runs stay in the main session.

**Subagent dispatched in three cases:**

1. **"Both" picked at Gate 1** — one subagent for X, one for AutoTrader, run in parallel via `superpowers:dispatching-parallel-agents`. Even if each side has only one job, the X+AutoTrader split itself is the parallelism win.
2. **"All configured queries" picked for X with 3+ queries** — one subagent per query, parallel.
3. **2 X queries with "All configured queries"** — runs sequentially in main session (subagent overhead not worth it for 2 jobs).

**Subagent contract:**
- Input: which actor, which query/URL/watchlist, which output file path
- Subagent calls Apify, parses results, writes the output file, returns a one-line summary string (e.g. "X pcp-watch: 12 tweets saved to research/x/2026-04-20-pcp-watch.md, cost $0.04")
- Subagent does NOT update watchlist bookkeeping — the parent session does that after all subagents return, to keep the watchlist file's edit history clean (single update per run, not interleaved with other concurrent jobs)

## Failure modes

| Failure | Behaviour |
|---|---|
| `APIFY_API_TOKEN` missing in `CLAUDE.local.md` | Fail at Gate 1, before any scraping. Tells B which file to add it to and the exact line format. |
| Apify returns 0 results | Tell B in the summary, do NOT write an empty output file. |
| Apify timeout (>60s) | Report the failure for that scrape, continue with any other scrapes in the run. B chooses whether to retry. |
| Apify returns malformed data | Save raw response to `research/<source>/_failed/YYYY-MM-DD-<slug>-raw.json` for debugging, report the failure. |
| Watchlist file references a search URL that AutoTrader has changed/broken | Apify will return 0 or an error; surface clearly so B can rebuild the watchlist URL. |
| Subagent crashes | Parent reports which scrape failed, other scrapes still complete. |

## Cost expectations

Rough order-of-magnitude (Apify pricing as of Q2 2026):
- X: ~$0.30 per 1000 tweets → 100 tweets ~$0.03
- AutoTrader: ~$1 per 1000 listings → 20 listings ~$0.02

Typical `/bs:research` run pulling 1 X query + 1 watchlist: well under $0.10.

If B runs "Both" with "All queries" daily, monthly cost still likely under $5 — a fraction of the Gemini image budget.

The Gate 3 preview always shows estimated cost before firing, so B has a chance to scope down expensive runs.

## Open questions for implementation phase

None at design level. Implementation plan should resolve:
- Exact JSON shape returned by `apidojo/twitter-scraper-lite` and `epctex/autotrader-uk-scraper` (read each actor's docs and confirm field names before writing the parsers).
- Whether `epctex/autotrader-uk-scraper` exposes vehicle registration / DOR fields directly, or whether they need to be parsed out of the listing's free-text body.
- Sensible defaults for the Gate 3 cost estimates (per-result × expected count) — refine after first few real runs.

## Success criteria

- B can type `/bs:research`, walk through the question gates, get structured research saved to disk, and feed any file into `/bs:content` to draft a post.
- B never has Apify fired without seeing exactly what's about to be scraped.
- The X target list is editable in a single markdown file; adding a new query takes under 30 seconds.
- Adding a new AutoTrader watchlist is a single markdown file; defining one takes under 60 seconds.
- A typical research run costs under $0.10 and completes in under 90 seconds.
