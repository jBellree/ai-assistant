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

Work through finalised ideas one at a time. For each, ask brand first, then platform, using two separate `AskUserQuestion` calls:

**Brand:**
- Magnitude Finance
- DSG Financial Services (Prestige or Vision)

**Platform(s):**
- WhatsApp dealer group
- LinkedIn
- Instagram
- Multiple

If B selects Multiple, follow up with a free-text question: "Which platforms?" then note the answer alongside the idea.

---

## Step 5 — Save all ideas to `ideas.md`

Save ALL ideas from the session — finalised AND discarded — to `projects/social-content/ideas.md`.

If the file does not exist, create it with the standard header from the plan before writing entries.

Add new entries at the TOP of the file, above the `<!-- NEW ENTRIES GO ABOVE THIS LINE -->` marker.

**Entry format:**

```markdown
## YYYY-MM-DD | [Source] | [Brand] | [Platform]

**Source:** [URL or description]
**Pillar:** [pillar name]
**Audience:** [audience]
**Status:** Saved

### Idea: [idea title]

[Angle: 2-3 sentence description]

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
