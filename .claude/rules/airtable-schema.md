# Airtable Schema — Content Hub base

This is the Airtable base that powers DSG's Content Hub app and the EA social-content skill. **EA reads from these tables (RSS-curated article list) and writes back when a post ships** (status + published date). Everything else brand/pillar/drafts lives in EA markdown.

**Write permission:** Claude can read AND write to this base freely (within the fields below). The CRM base `appCXdGmjsg5dxUIC` also has a **scoped** write exception defined in [.claude/rules/deal-tracker.md](.claude/rules/deal-tracker.md) (stage checkboxes, Dealer Contact Log creates, task completions — nothing else). Every other Airtable base remains read-only. Always show B the proposed change before committing a write.

## Base

| | |
|---|---|
| Base ID | `appwPT59GISaH3phA` |
| Workspace | DSG / Content Hub |
| Web URL | https://airtable.com/appwPT59GISaH3phA |

## Tables

### Articles — `tblvNFPoyugMVT9FL`
The RSS-curated article queue. B flags interesting articles in the Content Hub web UI; EA reads this table to offer "want to post about one of these?" When a post ships, EA updates Status + Published Date here.

Fields EA uses:

| Field | ID | Type | Used by EA for |
|---|---|---|---|
| Title | `fldGka52EhiB9kpTu` | singleLineText | Article headline (shown to B when picking) |
| URL | `fld14xbAkFrxt0dW9` | url | Source URL (reference in archive) |
| Excerpt | `fldPp7wUy6wx2mf4a` | multilineText | Short summary (context for drafting) |
| Status | `fldALIKSvL9GzeGZk` | singleSelect | Filter on "Saved Ideas" / "Manual Idea" / "Idea" to offer for drafting. Set to "Posted" when shipped. |
| Tags | `fldNdRSATQB0SKp4Q` | multipleSelects | PCP / HP / EV / Finance / Legal / Compliance / Industry / Trends |
| Content Pillars | `fldHDhRPGlhfzjzOr` | singleSelect | Set after drafting (once EA pillar merge is done) |
| Image | `fld1lVxT9PBSdXfm0` | url | Not currently used by EA (we generate via Gemini → hcti.io) |
| Published Date | `fldSfb4QIvrG7viho` | date (D/M/YYYY) | Set when a post ships |
| Platforms | `fldIkKmHcXDeb3ZiB` | multipleSelects | LinkedIn / Instagram (WhatsApp to be added by B if he wants CH to track dealer posts) |
| Hashtags | `fldAMKQub3lL1HFmo` | singleLineText | Set from the final post copy |

Status values: `New` / `Manual Idea` / `Idea` / `Drafting` / `Ready` / `Posted` / `Archived`

### Content Pillars — `tblro5krkRZ99LKdx`
Pillar taxonomy. Currently 4 generic pillars; plan to merge to EA's 5-pillar set. Fields: Name, Description, Content Ideas, Color.

### Brand Settings — `tblIpNLuWXJzPiDPJ`
Key/Value store for brand docs. Three records: Company Description, Buyer Persona, Tone of Voice. The `Value` field mirrors EA markdown at `references/brand/what-i-do.md`, `buyer-persona.md`, `tone-of-voice.md`. EA keeps the markdown as the main copy and syncs to Airtable when the markdown changes.

### RSS Feeds — `tblkoXs9sqN6o4Tg2`
RSS source list. B manages this in Content Hub UI. EA doesn't touch this table.

## Write pattern (safety default)

Before any Airtable write, Claude shows the proposed change to B:

> I'm about to update record `recXYZ` in Articles:
> - Status: Ready → Posted
> - Published Date: (empty) → 2026-04-18
> - Platforms: +LinkedIn
> Confirm?

Only commit after B's "yes" / "go" / "ok".
