# Slack Personal Assistant — Build Plan

## Overview
Transform "The Daily Hub" Slack workspace into B's proactive personal assistant for his finance broking business. All data lives in Airtable (base `appCXdGmjsg5dxUIC`). No Supabase — everything goes through Airtable.

## Architecture
```
Airtable (source of truth)
    ↓ queried by
Airtable Automations (scheduled triggers + scripts)
    ↓ posts to
Slack — "The Daily Hub" (proactive alerts & interaction)
    ↓ optionally
Claude API bot (answers questions in Slack)
```

## Phase 1: Slack Channels + Automated Briefings

### Channels to Create
| Channel | Purpose | Notifications |
|---|---|---|
| `#morning-briefing` | Automated daily plan (e.g. 7am) | Push |
| `#deal-alerts` | Deal stuck 5+ days, new acceptance, payout chase | Push |
| `#dealer-contact` | "You haven't spoken to [Cat A dealer] in 12 days" | Push |
| `#dealer-opportunities` | Dealer sent deals last month but 0 this month | Push |
| `#prospecting` | New dealer research results | Check when ready |

### Morning Briefing Content (mirrors existing CLAUDE.md briefing system)
- Active deals by status (Awaiting Decision, Awaiting Info, Accepted, ASD, In for Payout)
- Deals needing attention (aging thresholds per status)
- Outstanding deal tasks, dealer tasks, general tasks
- Priority dealer calls (Cat A/B overdue)
- Cancelled acceptances needing customer calls
- Today's assigned calls from Call Planner Assignments

### Automation Engine
- Airtable Automations with scripts that POST to Slack via webhook
- Scheduled: morning briefing (daily), dealer contact check (daily), deal aging alerts (every few hours)
- Triggered: when deal status changes, when a deal has been in a status too long

## Phase 2: Interactive Slack Bot
- Ask questions in Slack: "what's my pipeline value?" "who haven't I called this week?"
- Mark tasks done from Slack
- Log dealer contacts from Slack
- Powered by Claude API with Airtable context

## Phase 3: Voice
- Option A: Voice clips in Slack (transcribe → Claude → text reply)
- Option B: Dedicated voice assistant (web app with mic, works on phone)
- Option C: Phone call integration (Vapi/Bland.ai — could call B with morning briefing)

## Key Decisions Made
- No Supabase — everything through Airtable
- Slack workspace: "The Daily Hub" (already exists)
- Proactive > reactive — push notifications, not dashboards
- CLAUDE.md already has full briefing logic, table references, and field IDs

## Slack Channel IDs
| Channel | ID |
|---|---|
| `#morning-briefing` | `C0ALUM8FSE5` |
| `#deal-alerts` | `C0ALDNA382J` |
| `#dealer-contact` | `C0ALKBYCAP6` |
| `#dealer-opportunities` | `C0ALDNER5V4` |
| `#prospecting` | `C0ALDNFUF9U` |
| `#main-chat` (default) | `C08QLP44VPX` |

## Status
- [x] Slack MCP connected to Claude Code (global config)
- [x] CLAUDE.md with full briefing system written
- [x] Check existing Slack channels in The Daily Hub
- [x] Create Slack channels (old pipeline channels deleted, new ones created)
- [ ] Build Airtable Automations for morning briefing
- [ ] Build deal alert automations
- [ ] Build dealer contact alert automations
- [ ] Set up Slack bot for interactive queries
