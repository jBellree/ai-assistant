---
name: hubspot-log-meeting
description: Log a completed dealer meeting against a company in HubSpot by driving the UI in Chrome. No API, no OAuth, no IT exposure. Use when B says "log meeting", "/hubspot-log", "just spoke to [dealer]", "log a call with", or similar.
---

# HubSpot Log Meeting

## Purpose

Log a meeting against a dealer's HubSpot company record by driving the HubSpot UI in Chrome via Claude in Chrome. **No API, no OAuth, no integration installed in HubSpot.** All actions look like B using Chrome on the Mac Mini, because that's exactly what's happening.

## When to use

Trigger phrases: `log meeting`, `/hubspot-log`, `hubspot meeting`, `just spoke to [dealer]`, `log a call with`, `had a meeting with`, `visited [dealer]`.

If B mentions a meeting in passing without asking to log it (e.g. "had a great chat with Phantom yesterday"), do NOT auto-trigger. Ask: "Want me to log that in HubSpot?"

## Pre-requisites

- Mac Mini awake, Chrome open
- HubSpot logged in (B's session, normal browser)
- Claude in Chrome connector enabled

If HubSpot isn't open, the skill opens `app.hubspot.com` in a new tab. If not logged in, the skill stops and tells B to log in.

## Fixed values (never ask)

- **Attendees:** Brian Rothwell `<brian.rothwell@dsgfs.com>` — always tick this contact, no others
- **Meeting outcome:** `Completed` — always
- **Duration:** leave at HubSpot's default (15 minutes) unless B specifies otherwise

## Variable inputs (always ask via AskUserQuestion)

If `AskUserQuestion` isn't loaded, load it via `tool_search` query `select:AskUserQuestion` first.

### Question 1 — Company name
Free-text input. Parse from B's trigger sentence if present (e.g. "just spoke to Phantom" → company = "Phantom"). Confirm in the questionnaire.

### Question 2 — Meeting type
Single select, exactly these three values (HubSpot's exact strings):
- `Dealer Visit`
- `Prospect Call`
- `Key Account Call`

If B's trigger sentence implies one (e.g. "visited" → Dealer Visit, "called a prospect" → Prospect Call), default the selection but still show the question so B can override.

### Question 3 — Date and time
Free-text. Accept natural input: `now`, `just now`, `9:30 today`, `yesterday 2pm`, `28/04/2026 14:30`.
Parse to `DD/MM/YYYY HH:MM`. Show parsed result in confirmation gate so B can catch errors.

### Question 4 — Notes
Long text. What was discussed, next steps. No template — let B write what they want.

## Workflow

### Step 0 — Parse the trigger
Pull whatever's already in B's opening message (company, type hint, time hint, partial notes). Don't re-ask for things that are already clear.

### Step 1 — Gather missing inputs
One `AskUserQuestion` call covering only the gaps. Pre-fill defaults where parsed.

### Step 2 — Confirmation gate
Show the full proposed entry as plain text:

```
About to log:
  Company:  Phantom Motor Company Limited
  Attendee: Brian Rothwell (you)
  Outcome:  Completed
  Type:     Dealer Visit
  When:     28/04/2026 09:44 GMT+1
  Duration: 15 minutes
  Notes:    [first 200 chars, ellipsis if longer]

Go?
```

Wait for explicit `yes` / `go` / `ok` / `save`. Anything else means stop and ask what to change.

### Step 3 — Drive HubSpot

Using Claude in Chrome:

1. **Find HubSpot.** If a HubSpot tab is already open, switch to it. Otherwise navigate to `app.hubspot.com`.
2. **Search company.** Click the global search bar at the top of the page. Type the company name. Click the **Companies** filter chip.
3. **Open the record.** Click the matching company. If multiple matches, STOP and ask B to pick (see Failure modes).
4. **Open Activities.** Click the `Activities` tab on the company record.
5. **Open Meetings.** Click the `Meetings` sub-tab.
6. **Open the modal.** Click `Log Meeting` (NOT `Create Meeting`).
7. **Set attendee.** Click `0 contacts` under Attendees. Tick the box next to `Brian Rothwell <brian.rothwell@dsgfs.com>`. Click outside the popover to close it.
8. **Set outcome.** Click `Select meeting outcome`. Click `Completed`.
9. **Set type.** Click `Select meeting type` (or whatever's currently shown). Click the value B chose.
10. **Set date/time.** Click the meeting start time field. In the edit popover, set the date and time. Click `Apply`.
11. **Set duration.** Only if B specified something other than 15 minutes — otherwise skip.
12. **Set notes.** Click into the notes body (`Start typing to log a meeting...`). Type the notes verbatim.
13. **STOP.** Do NOT click `Log meeting` yet.

### Step 4 — Final visual check
Tell B in chat:

```
Modal filled, eyeball it on screen.
Say 'save' to log it, 'edit X' to change a field, or 'cancel' to bin it.
```

Wait for explicit input.

- `save` → click `Log meeting`, go to Step 5
- `edit [field]` → re-open that field, take new value, return to Step 4
- `cancel` → click the `X` to close the modal without saving, exit cleanly

### Step 5 — Confirm and exit
After clicking `Log meeting`, verify the entry now appears in the Meetings list at the top under "Logged meeting - Completed by Brian Rothwell".

Report:
```
Logged. Anything else?
```

Don't auto-suggest follow-up actions. B will say what's next.

## Failure modes

| Failure | Behaviour |
|---|---|
| HubSpot not open / not logged in | Stop. Tell B: "HubSpot's not logged in. Open it and try again." Do not attempt to log in. |
| Company search returns 0 results | Show what was searched. Ask: "No match for '[company]'. Try a different name?" |
| Multiple companies match | Show top 3 (name, location). Ask B to pick by number. |
| Modal doesn't open after clicking Log Meeting | Wait 3s, retry once. If still nothing, screenshot, tell B: "HubSpot UI didn't respond. Try manually?" Exit. |
| Outcome / type / attendee dropdown doesn't contain the expected value | Stop. Tell B: "HubSpot's [field] options have changed — expected '[value]', got [list]. Pick one or update the skill." |
| Session times out mid-flow | Stop. Tell B to log in again. Do NOT log in for them. |
| Date parsing ambiguous (e.g. "Tuesday") | Ask which Tuesday — last week's or next week's. |
| B says "edit X" with X unclear | Ask which field. Don't guess. |

## Hard rules

- **NEVER click `Log meeting` without explicit `save` from B in chat.** Two confirmation gates is deliberate.
- **NEVER touch any other record on the company** — no deal edits, no contact edits, no tasks, no notes outside the meeting modal.
- **NEVER change the attendee** away from Brian Rothwell. If B asks to add other attendees, STOP and ask — this is outside the skill's scope.
- **NEVER use the HubSpot API or any integration.** All actions through Chrome only.
- **NEVER auto-extend.** If B mentions logging a deal update, a task, an email, or anything else HubSpot-y, STOP and ask. Don't improvise other HubSpot actions inside this skill.
- **NEVER tick the "Create a To-do task to follow up" checkbox** at the bottom of the modal unless B explicitly asks.

## Why this skill exists (context for future Claudes)

HubSpot at DSG is owned by B's employer. IT can see installed integrations, OAuth grants, API call patterns, and non-browser user agents. B has explicitly ruled out any API integration. This skill exists so B gets the speed of automation without the visibility of an integration. Every action looks like B using Chrome — because it is.

If you're tempted to "improve" this by adding a HubSpot API call: don't. The constraint is the point.

## Example flow

```
B: just spoke to phantom for 30 mins, dealer visit. brad confirmed the
   tillotson paperwork's coming friday. follow up next week.

Claude: [parses: company=Phantom, type=Dealer Visit, duration=30, notes
        present, time=now]

        [AskUserQuestion: confirm date/time = "now" → 28/04/2026 09:44]

        About to log:
          Company:  Phantom (search will confirm match)
          Attendee: Brian Rothwell (you)
          Outcome:  Completed
          Type:     Dealer Visit
          When:     28/04/2026 09:44 GMT+1
          Duration: 30 minutes
          Notes:    Brad confirmed Tillotson paperwork coming Friday.
                    Follow up next week.

        Go?

B: go

Claude: [drives Chrome through Steps 3.1 - 3.13]

        Modal filled, eyeball it on screen.
        Say 'save' to log, 'edit X' to change, 'cancel' to bin it.

B: save

Claude: [clicks Log meeting]

        Logged. Anything else?
```
