# Content Ideation Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `/bs:ideate` orchestrator skill and four source sub-skills (YouTube, X, PLAUD, daily-capture) that surface content ideas from multiple sources, iterate them with B, save to `ideas.md`, and hand off to the existing brand content skills.

**Architecture:** One orchestrator skill (`bs-ideate`) invokes one of four source sub-skills based on B's choice. Each sub-skill fetches raw material (via Python script or conversation), Claude generates 4-6 ideas in-session, B iterates until happy, all ideas are saved to `projects/social-content/ideas.md`, and finalised ideas hand off to `magnitude-social-content` or `dsg-social-content`.

**Tech Stack:** Claude Code skills (SKILL.md), Python 3 (`youtube-transcript-api`, `apify-client`), `projects/social-content/ideas.md` as idea store.

---

## File Map

| Action | File | Responsibility |
|---|---|---|
| Create | `.claude/skills/bs-ideate/SKILL.md` | Orchestrator — source picker, iteration, save, handoff |
| Create | `.claude/skills/youtube-content/SKILL.md` | YouTube sub-skill — URL intake, script invocation, idea return |
| Create | `.claude/skills/youtube-content/fetch_transcript.py` | Fetch YouTube transcript via `youtube-transcript-api` |
| Create | `.claude/skills/x-content/SKILL.md` | X sub-skill — Apify invocation, idea return |
| Create | `.claude/skills/x-content/fetch_x.py` | Fetch X posts via Apify actor |
| Create | `.claude/skills/plaud-content/SKILL.md` | PLAUD sub-skill — paste intake, idea return |
| Create | `.claude/skills/daily-capture/SKILL.md` | Daily capture sub-skill — conversational intake, idea return |
| Modify | `projects/social-content/ideas.md` | Migrate to rich entry format, preserve existing content |
| Add key | `CLAUDE.local.md` | Add `APIFY_API_KEY=<value>` (B does this manually) |

---

## Task 1: Install Python dependencies

**Files:**
- No new files — system-level installs

- [ ] **Step 1: Install `youtube-transcript-api`**

```bash
pip install youtube-transcript-api
```

Expected output: `Successfully installed youtube-transcript-api-...`

- [ ] **Step 2: Install `apify-client`**

```bash
pip install apify-client
```

Expected output: `Successfully installed apify-client-...`

- [ ] **Step 3: Verify both installed**

```bash
python3 -c "import youtube_transcript_api; import apify_client; print('OK')"
```

Expected output: `OK`

---

## Task 2: Build `fetch_transcript.py`

**Files:**
- Create: `.claude/skills/youtube-content/fetch_transcript.py`

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p ".claude/skills/youtube-content"
```

- [ ] **Step 2: Write `fetch_transcript.py`**

```python
#!/usr/bin/env python3
"""
Fetch a YouTube video transcript and print it as plain text.
Usage: python3 fetch_transcript.py <youtube_url>
No API key required.
"""
import re
import sys
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def fetch_transcript(url: str) -> str:
    video_id = extract_video_id(url)
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video_id)
    return " ".join(segment.text for segment in transcript)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_transcript.py <youtube_url>", file=sys.stderr)
        sys.exit(1)
    print(fetch_transcript(sys.argv[1]))
```

- [ ] **Step 3: Test with the proven video URL**

```bash
python3 ".claude/skills/youtube-content/fetch_transcript.py" "https://youtu.be/qBoShOFyl8M" | head -c 500
```

Expected: First 500 characters of the transcript printed to stdout (no errors).

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/youtube-content/fetch_transcript.py"
git commit -m "feat: add YouTube transcript fetcher script"
```

---

## Task 3: Build `fetch_x.py`

**Files:**
- Create: `.claude/skills/x-content/fetch_x.py`

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p ".claude/skills/x-content"
```

- [ ] **Step 2: Write `fetch_x.py`**

```python
#!/usr/bin/env python3
"""
Fetch recent X (Twitter) posts for fixed motor finance search queries via Apify.
Usage: python3 fetch_x.py
Requires: APIFY_API_KEY environment variable set by caller (Claude reads from CLAUDE.local.md).
Prints a plain text summary of top posts to stdout.
"""
import os
import sys
from apify_client import ApifyClient

SEARCH_QUERIES = [
    "motor finance UK",
    "car finance UK",
    "FCA motor finance",
    "used car market UK",
    "PCP finance UK",
]

ACTOR_ID = "apidojo/tweet-scraper"
MAX_ITEMS_PER_QUERY = 15


def fetch_posts(api_key: str) -> list[dict]:
    client = ApifyClient(api_key)
    all_posts = []
    seen_ids = set()

    for query in SEARCH_QUERIES:
        run_input = {
            "searchTerms": [query],
            "maxItems": MAX_ITEMS_PER_QUERY,
            "queryType": "Latest",
        }
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            post_id = item.get("id") or item.get("url", "")
            if post_id not in seen_ids:
                seen_ids.add(post_id)
                all_posts.append({
                    "query": query,
                    "text": item.get("text", ""),
                    "author": item.get("author", {}).get("userName", "unknown"),
                    "url": item.get("url", ""),
                    "created_at": item.get("createdAt", ""),
                })

    return all_posts


def format_output(posts: list[dict]) -> str:
    lines = []
    current_query = None
    for post in posts:
        if post["query"] != current_query:
            current_query = post["query"]
            lines.append(f"\n=== Search: {current_query} ===\n")
        lines.append(f"@{post['author']} ({post['created_at'][:10]})")
        lines.append(post["text"])
        lines.append(f"URL: {post['url']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    api_key = os.environ.get("APIFY_API_KEY")
    if not api_key:
        print("Error: APIFY_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    posts = fetch_posts(api_key)
    print(format_output(posts))
    print(f"\n[Total posts fetched: {len(posts)}]", file=sys.stderr)
```

- [ ] **Step 3: Add `APIFY_API_KEY` to `CLAUDE.local.md`**

B does this manually. Open `CLAUDE.local.md` and add:

```
----------------------------------------------
Apify
----------------------------------------------

APIFY_API_KEY=<paste your key from apify.com/account/integrations>

----------------------------------------------
----------------------------------------------
```

- [ ] **Step 4: Test the script (requires key to be set)**

```bash
APIFY_API_KEY="$(grep 'APIFY_API_KEY' 'CLAUDE.local.md' | cut -d= -f2)" \
  python3 ".claude/skills/x-content/fetch_x.py" | head -c 1000
```

Expected: First 1000 characters of X posts printed, covering at least one search query section.

- [ ] **Step 5: Commit**

```bash
git add ".claude/skills/x-content/fetch_x.py"
git commit -m "feat: add X/Twitter Apify scraper script"
```

---

## Task 4: Migrate `ideas.md` to rich format

**Files:**
- Modify: `projects/social-content/ideas.md`

The existing file uses a simple one-liner format sectioned by platform. Migrate to the richer per-idea entry format defined in the spec, preserving the existing backlog sections as a legacy block.

- [ ] **Step 1: Rewrite `ideas.md` with new format**

Replace the entire contents of `projects/social-content/ideas.md` with:

```markdown
# Post Ideas Backlog

All content ideas regardless of source. Captured by `/bs:ideate` and its sub-skills.

**Status values:** `Saved` | `Drafted` | `Posted` | `Killed`

**Source types:** YouTube | X | PLAUD | Daily | RSS | Fresh

---

<!-- NEW ENTRIES GO ABOVE THIS LINE — newest at top -->

---

## Legacy entries (pre-ideation layer)

Audience: LinkedIn (D2C / consumer)
Audience: WhatsApp (Dealer group)

_(No ideas were logged before the ideation layer was built.)_
```

- [ ] **Step 2: Verify the file reads correctly**

```bash
head -20 "projects/social-content/ideas.md"
```

Expected: New header and format visible.

- [ ] **Step 3: Commit**

```bash
git add "projects/social-content/ideas.md"
git commit -m "feat: migrate ideas.md to rich entry format for ideation layer"
```

---

## Task 5: Write `youtube-content` sub-skill SKILL.md

**Files:**
- Create: `.claude/skills/youtube-content/SKILL.md`

- [ ] **Step 1: Write the SKILL.md**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add ".claude/skills/youtube-content/SKILL.md"
git commit -m "feat: add youtube-content sub-skill"
```

---

## Task 6: Write `x-content` sub-skill SKILL.md

**Files:**
- Create: `.claude/skills/x-content/SKILL.md`

- [ ] **Step 1: Write the SKILL.md**

```markdown
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
Read `APIFY_API_KEY` from `CLAUDE.local.md`. If not present, tell B to add it (see Task 3 of the implementation plan) and abort.

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
```

- [ ] **Step 2: Commit**

```bash
git add ".claude/skills/x-content/SKILL.md"
git commit -m "feat: add x-content sub-skill"
```

---

## Task 7: Write `plaud-content` sub-skill SKILL.md

**Files:**
- Create: `.claude/skills/plaud-content/SKILL.md`

- [ ] **Step 1: Create the skill directory and write SKILL.md**

```bash
mkdir -p ".claude/skills/plaud-content"
```

```markdown
---
name: plaud-content
description: PLAUD voice note transcript sub-skill. Takes a pasted transcript and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: PLAUD Content Ideas

## Purpose
Take a PLAUD voice note transcript pasted by B and generate 4-6 content ideas.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Get the transcript
Ask B to paste the PLAUD transcript. Wait for the paste.

### Step 2 — Generate ideas
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
| Angle | The specific hook that makes this worth posting — grounded in real detail from the transcript |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

Voice notes are raw and conversational. Extract the substance — the deal detail, the observation, the insight. Polish the angle; keep it grounded in what B actually said.

### Step 3 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.

## Note on PLAUD integration
Currently paste-in. Future upgrade: if PLAUD exports transcripts to a known file path, update Step 1 to read the file directly instead of requesting a paste.
```

- [ ] **Step 2: Commit**

```bash
git add ".claude/skills/plaud-content/SKILL.md"
git commit -m "feat: add plaud-content sub-skill"
```

---

## Task 8: Write `daily-capture` sub-skill SKILL.md

**Files:**
- Create: `.claude/skills/daily-capture/SKILL.md`

- [ ] **Step 1: Create the skill directory and write SKILL.md**

```bash
mkdir -p ".claude/skills/daily-capture"
```

```markdown
---
name: daily-capture
description: Daily work capture sub-skill. Draws out the detail of B's day through conversation and returns 4-6 content ideas. Invoked by bs-ideate, not directly by B.
---

# Sub-skill: Daily Capture Content Ideas

## Purpose
Draw out the content-worthy detail from B's day — deals funded, tricky cases solved, observations from the trade — and generate 4-6 content ideas.

## Invoked by
`bs-ideate` orchestrator only. Not triggered directly.

## Flow

### Step 1 — Draw out the detail
Ask these questions ONE AT A TIME using `AskUserQuestion` where possible. Stop when you have enough to generate ideas — you don't need all four if the first two give you plenty.

1. "What happened today that was interesting — a deal, a case, a conversation?"
2. "What made it unusual or tricky?"
3. "What would a dealer take away from this if you told them?"
4. "What would a buyer take away from this?"

Listen for: vehicle type, finance product used, lender, anything that made the case harder than normal, the outcome, any lesson learned.

### Step 2 — Generate ideas
Read B's answers against:
- `@references/content-pillars.md`
- `@references/brand/tone-of-voice.md`
- `@references/brand/buyer-persona.md`
- `@.claude/rules/content-guidelines.md`

Generate 4-6 ideas. For each idea produce:

| Field | Description |
|---|---|
| Pillar | One of: Deal Spotlight / Rate Watch / Lender News / Underwriting Masterclass / Industry Insight |
| Audience | Dealer WhatsApp / LinkedIn D2C / Instagram / multiple |
| Angle | The specific hook that makes this worth posting — rooted in the real detail B gave |
| Hook line | Opening sentence, ready to use |
| Why it works | One line connecting it to B's audience |

The best ideas come from the ugly, unpolished details — the specific lender, the weird edge case, the thing that surprised B. Those are the things no AI can invent and no competitor can copy.

### Step 3 — Return to orchestrator
Hand all 4-6 ideas back to `bs-ideate` for iteration with B.
```

- [ ] **Step 2: Commit**

```bash
git add ".claude/skills/daily-capture/SKILL.md"
git commit -m "feat: add daily-capture sub-skill"
```

---

## Task 9: Write `bs-ideate` orchestrator SKILL.md

**Files:**
- Create: `.claude/skills/bs-ideate/SKILL.md`

- [ ] **Step 1: Create the skill directory and write SKILL.md**

```bash
mkdir -p ".claude/skills/bs-ideate"
```

```markdown
---
name: bs-ideate
description: Content ideation orchestrator. Picks a source, invokes the matching sub-skill, iterates ideas with B, saves to ideas.md, and hands off to the brand content skill. Trigger: "ideate", "content ideas", "what should I post", /bs:ideate
---

# Skill: Content Ideation Orchestrator (`/bs:ideate`)

## Trigger phrases
"ideate", "content ideas", "what should I post", "ideas", `/bs:ideate`

## Purpose
Surface content ideas from any source, iterate them with B until they're sharp, save everything to `projects/social-content/ideas.md`, and hand off finalised ideas to `magnitude-social-content` or `dsg-social-content`.

---

## Step 1 — Pick the source

Use `AskUserQuestion` (load via `ToolSearch` with `query: "select:AskUserQuestion"` if not available):

```
Which source are we working from today?
- YouTube video
- X (motor finance news)
- PLAUD transcript
- My day / a deal I worked
```

---

## Step 2 — Invoke the sub-skill

| Selection | Sub-skill to invoke |
|---|---|
| YouTube video | `youtube-content` |
| X (motor finance news) | `x-content` |
| PLAUD transcript | `plaud-content` |
| My day / a deal I worked | `daily-capture` |

The sub-skill handles all fetching and idea generation. It returns 4-6 ideas.

---

## Step 3 — Present and iterate

Show the ideas clearly numbered. For each idea show:
- **Pillar**
- **Audience**
- **Angle**
- **Hook line**
- **Why it works**

Then invite feedback. B may:
- Accept an idea as-is
- Ask to change the angle, pillar, or audience on a specific idea
- Merge two ideas
- Kill an idea
- Ask for a completely new idea

Edit specific ideas in response to feedback. Do not regenerate the full list unless asked. Continue iterating until B is happy.

One session may produce anywhere from 1 to 4 finalised ideas.

---

## Step 4 — Confirm brand and platform for each finalised idea

For each idea B has approved, confirm using `AskUserQuestion`:

**Brand:**
- Magnitude Finance
- DSG Financial Services (Prestige or Vision)

**Platform(s):**
- WhatsApp dealer group
- LinkedIn
- Instagram
- Multiple (specify)

---

## Step 5 — Save all ideas to `ideas.md`

Save ALL ideas from the session — finalised AND discarded — to `projects/social-content/ideas.md`.

Add new entries at the TOP of the file, above the `<!-- NEW ENTRIES GO ABOVE THIS LINE -->` marker.

**Entry format:**

```markdown
## YYYY-MM-DD | [Source] | [Brand] | [Platform]

**Source:** [URL or description]
**Pillar:** [pillar name]
**Status:** Saved

### Idea: [idea title]

[2-3 sentence description of the angle]

**Hook:** "[opening line]"

---
```

For discarded ideas, use `**Status:** Killed` and add a brief note on why it was dropped.

Source values: `YouTube` / `X` / `PLAUD` / `Daily` / `RSS` / `Fresh`
Brand values: `Magnitude` / `DSG Prestige` / `DSG Vision`

---

## Step 6 — Hand off to the brand content skill

For each finalised idea, invoke the appropriate skill:
- **Magnitude** → invoke `magnitude-social-content`
- **DSG** → invoke `dsg-social-content`

Pass the finalised idea's angle, hook line, and platform(s) to the brand skill so it can skip straight to copy drafting.

Update the idea's status in `ideas.md` from `Saved` to `Drafted` at handoff.

The ideation session ends here. The brand skill takes over.

---

## Context to load
- `@references/content-pillars.md`
- `@references/brand/tone-of-voice.md`
- `@references/brand/buyer-persona.md`
- `@.claude/rules/content-guidelines.md`
- `@.claude/rules/communication-style.md`
```

- [ ] **Step 2: Commit**

```bash
git add ".claude/skills/bs-ideate/SKILL.md"
git commit -m "feat: add bs-ideate orchestrator skill"
```

---

## Task 10: Register `bs:ideate` in CLAUDE.md commands section

**Files:**
- Modify: `CLAUDE.md`

`bs:menu` is a superpowers plugin skill that lists commands — it reads available skills automatically. The only registration needed is adding the trigger to CLAUDE.md's Commands section so it appears in the menu alongside the other `/bs:` commands.

- [ ] **Step 1: Open `CLAUDE.md` and find the Commands section**

Look for the line that starts with:
```
`/bs:menu` | `/bs:plan` | ...
```

- [ ] **Step 2: Add `/bs:ideate` to the commands line**

```
`/bs:menu` | `/bs:plan` | `/bs:reminders` | `/bs:content` | `/bs:deals` | `/bs:calls` | `/bs:ideate`
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: register bs:ideate in CLAUDE.md commands"
```

---

## Task 11: End-to-end verification

No new files — this is a manual test run.

- [ ] **Step 1: Test YouTube flow**

Run `/bs:ideate`, select YouTube, use `https://youtu.be/qBoShOFyl8M`.
Confirm: transcript fetches, 4-6 ideas appear, each has all 5 fields.

- [ ] **Step 2: Test X flow**

Run `/bs:ideate`, select X.
Confirm: `fetch_x.py` runs with the key from `CLAUDE.local.md`, posts returned, 4-6 ideas appear.

- [ ] **Step 3: Test PLAUD flow**

Run `/bs:ideate`, select PLAUD, paste a short sample transcript.
Confirm: 4-6 ideas appear.

- [ ] **Step 4: Test daily capture flow**

Run `/bs:ideate`, select My day.
Confirm: 4 questions asked one at a time, 4-6 ideas appear from the answers.

- [ ] **Step 5: Test iteration**

From any flow, ask Claude to change the angle on one specific idea.
Confirm: only that idea changes, the rest stay as-is.

- [ ] **Step 6: Test save to `ideas.md`**

Approve one idea and kill one.
Confirm: both appear in `projects/social-content/ideas.md` — approved with `Status: Saved`, killed with `Status: Killed`.

- [ ] **Step 7: Test handoff**

Finalise one Magnitude idea.
Confirm: `magnitude-social-content` skill is invoked with the angle and hook pre-populated.

---

## Dependencies checklist before starting

- [ ] `youtube-transcript-api` installed (`pip install youtube-transcript-api`)
- [ ] `apify-client` installed (`pip install apify-client`)
- [ ] `APIFY_API_KEY` added to `CLAUDE.local.md` by B
