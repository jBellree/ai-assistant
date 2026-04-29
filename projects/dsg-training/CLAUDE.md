# DSG Deal Placement Team Training — Project Brief

## Purpose of this file

This is the persistent context for this project. Any new Claude Code session should read this first before doing anything else. It captures the business context, the training goals, the tone rules, and the structure we've agreed.

---

## About B (the user) and DSG

- B works at **DSG**, a vehicle finance intermediary (broker).
- DSG places customers with lenders (funders) and earns commission as a % of the amount borrowed — dealer commission + DSG margin + debit provision.
- The deal placement team receives applications, profiles the customer, and writes proposals to send to lender underwriters.
- B has been asked to deliver training on reading **personal tax returns** and **company accounts** to help the team profile applications better.
- **B is not an expert** in tax returns or accounts — the training build is also a learning exercise for B. Claude's job is to tutor B first, then help B build the training.

## The deals

- **Typical deal size:** £25k–£250k, occasionally up to £1m.
- **Asset class:** 99% prestige supercars (Lamborghini, McLaren, Porsche, Ferrari, etc.). Occasional campervan or horsebox.
- **Key implication:** these are lifestyle/status assets, not income-generating business tools. Underwriters scrutinise personal affordability and wealth hard because the asset can't "pay for itself."
- **Lenders include:** Aldermore Bank, Haydock Finance, United Trust Bank, Arkle Finance, Metro Bank, Cambridge and Counties (and similar commercial lenders).

## The customers

A mix of three types — training must cover all three distinctly, no blurring of lines:

1. **Employed high earners** (City, finance, sports, entertainment — simplest scenario)
2. **Sole traders / self-employed** (professionals, consultants)
3. **Limited company directors** — the most complex and most common. Training needs to handle variations like:
   - Sole director, 100% shareholder of own Ltd co (lean on strengths of the whole business)
   - Minority shareholder director of a larger business (very different risk profile)

## The team being trained

- **5 people**, pitched to the least experienced — **treat as beginners**.
- Plain English only. **Zero jargon.** Every term explained the first time it appears.
- Training must be **reusable for future new starters**, not a one-off.
- Goal is a foundation, not expertise: "You won't walk out an expert, but you'll know where to look and what questions to ask."

## The live session

- **Length:** ~1 hour (hard ceiling — B doesn't want brain-drain).
- **Deadline:** one week from project kickoff (kickoff date in main chat — B will confirm in session 1).
- **Structure agreed:**
  1. Overview of all three customer types (10–15 min)
  2. Deep dive: Ltd company accounts + personal tax return, with worked examples showing how they link (40–45 min)
  3. Q&A / wrap (5–10 min)
- The **written manual** is the main asset; the session is the kickoff. The manual does the heavy lifting and becomes the onboarding resource for future new starters.

## Training goals (what "good" looks like after the session)

The team should be able to:

1. **Spot the strengths** when profiling an application and build the write-up around the strengths.
2. **Acknowledge weaknesses honestly but briefly** — don't hide them, don't dwell on them.
3. **Spot obvious red flags AND obvious green flags.** Both matter equally. Green flags turn borderline deals into approvals.
4. **Feel more confident** — the training is a start, not a finish line.

## Tone and style rules — NON-NEGOTIABLE

### For the training materials themselves

- **Plain English. Zero jargon.** Any technical term must be defined the first time it's used.
- **Bullet points over prose** where possible.
- **Worked examples with real numbers** — people learn from examples, not definitions.
- **Red flags / green flags cheat sheets** for each document type.
- **Glossary** at the back of the manual.
- **Self-test questions** for new starters to check understanding.

### For the proposal-writing section specifically

This is critical — B's team writes proposals that go to underwriters (UWs):

- **Bullet points, not paragraphs.** UWs scan, they don't read.
- **Lead with the headline strength** in one line.
- **Key facts up front:** income, deposit, asset, term, affordability.
- **Address weaknesses honestly and briefly.**
- **End with a clear ask** — what decision do you want from the UW?
- **NO "AI-generated" feel.** UWs spot generic adjective-heavy writing instantly and stop reading. Avoid: "strong, robust, established, comprehensive, extensive." Write like an experienced human who respects the reader's time.
- **Factual and to the point.** If an adjective isn't doing real work, cut it.

---

## Deliverables

### 1. Training manual (the main asset — reusable forever)

Sections:

1. The three customer types — overview
2. Reading a personal tax return (plain English, section by section)
3. Reading company accounts (plain English, section by section)
4. Linking the two — how a director's personal income shows up in their company accounts (THE most valuable section — this is where people get confused)
5. Writing the proposal — the DSG way (bullets, facts, lead with strength)
6. Worked examples (3–4 fictional customer profiles with full documents)
7. Red flags / green flags cheat sheets
8. Glossary
9. Self-test questions for new starters

### 2. Session slide deck

- Condensed version of the manual
- Built around 1–2 of the worked examples
- Designed to run in ~50 min + Q&A

### 3. Worked example customer profiles

Fabricated (not real — GDPR), designed to teach specific lessons:

- Strong Ltd co director (clean, obvious approval)
- Messy Ltd co director (strong underneath, but you have to dig for it — teaches "lead with strength")
- Sole trader (different document set, same principles)
- Employed high earner (simplest scenario, good starting point)

---

## How to work with B

- **Tutor B first, build second.** B needs to understand the material well enough to deliver it confidently and answer questions. Don't skip the tutoring to rush to deliverables.
- **Small chunks, check understanding, then continue.** Don't dump a wall of information.
- **Ask before assuming.** If there's ambiguity, ask one question at a time rather than a list.
- **Plain English with the user too**, not just in the materials. No jargon when tutoring.
- **Be direct but kind.** Push back if an idea is problematic. Don't sycophant.
- **User preferences (from their profile):** TL;DR first, then short answer. Bullets for complex topics. Wait for confirmation on multi-step processes. Plain English. For casual chat keep it short.

---

## Progress so far

- Project brief fully scoped (this document).
- Agreed to start tutoring with **personal tax returns** first (simpler conceptually than company accounts).
- Chunk 1 complete: What a personal tax return is, who files one, why it matters for DSG.
- Chunk 2 complete: The four documents (SA100, SA302, Tax Year Overview, supplementary pages). DSG gets and needs the full SA100 for HNW/Ltd co customers.
- Chunk 3 complete: How a Ltd co director's income works (small PAYE + dividends + DLA). Why the SA100 alone is misleading. Director's Loan Account explained in full.
- Chunk 4 complete: SA100 walkthrough section by section. Practical approach for when one lands. Two-year rule: always ask for last two years of SA100s.
- **Next up:** Chunk 5 — company accounts. The other half of the picture. What the documents look like, what to read, where to find the DLA and director income that doesn't appear on the SA100.

---

## Folder structure

```
dsg-training/
├── CLAUDE.md                          # This file
├── README.md                          # Quick project overview for humans
├── 00-tutoring-notes/                 # B's personal learning notes (where Claude tutors B)
│   ├── 01-personal-tax-returns.md
│   ├── 02-company-accounts.md
│   ├── 03-linking-the-two.md
│   └── 04-proposal-writing.md
├── 01-manual/                         # The training manual (main deliverable)
│   ├── 00-introduction.md
│   ├── 01-three-customer-types.md
│   ├── 02-reading-personal-tax-returns.md
│   ├── 03-reading-company-accounts.md
│   ├── 04-linking-accounts-and-tax-returns.md
│   ├── 05-writing-the-proposal.md
│   ├── 06-worked-examples.md
│   ├── 07-red-and-green-flags.md
│   ├── 08-glossary.md
│   └── 09-self-test-questions.md
├── 02-worked-examples/                # Detailed fictional customer profiles
│   ├── customer-01-employed-high-earner.md
│   ├── customer-02-sole-trader.md
│   ├── customer-03-ltd-director-strong.md
│   └── customer-04-ltd-director-messy.md
├── 03-slide-deck/                     # For the live 1-hour session
│   └── session-outline.md
└── 04-reference/                      # Quick-reference sheets
    ├── red-flags-cheat-sheet.md
    ├── green-flags-cheat-sheet.md
    └── glossary.md
```

---

## Working rhythm

Suggested day-by-day (1-week deadline):

- **Day 1–2:** Claude tutors B on personal tax returns. Notes captured in `00-tutoring-notes/01-personal-tax-returns.md`. Manual section drafted in `01-manual/02-reading-personal-tax-returns.md`.
- **Day 2–3:** Tutor B on company accounts. Same pattern.
- **Day 3:** Link the two (the critical section).
- **Day 4:** Build the worked examples together (B involved in scenario design).
- **Day 5:** Draft the proposal-writing section + red/green flags + glossary.
- **Day 6:** Build the slide deck from the manual.
- **Day 7:** Dress rehearsal / final tweaks.

Flex as needed. Don't sacrifice B's understanding for speed — if B isn't solid on a section, the training will fall apart when a team member asks a real question.
