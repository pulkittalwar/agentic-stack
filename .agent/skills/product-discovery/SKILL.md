---
name: product-discovery
version: 2026-04-23
description: Use whenever a user arrives with an idea, a feature request, or a vague direction — "I want to build X", "I have an idea", "help me think through this", "is this worth building". Before any design, spec, or plan gets written, run a structured premise-challenging dialog that validates what problem is being solved, for whom, and whether it is worth solving at all. This skill gates every downstream PDLC skill; do not proceed to `requirements-writer` until discovery produces a named user, a named status quo, and a narrow wedge.
triggers: ["I have an idea", "brainstorm this", "help me think through this", "is this worth building", "office hours", "what should we build"]
tools: [recall, bash]
sources:
  superpowers: brainstorming (dialog discipline + hard-gate before implementation)
  gstack: office-hours (6 forcing questions for demand reality)
preconditions: ["user has an idea or direction — not necessarily well-formed"]
constraints:
  - no implementation, scaffolding, or coding action until a design is approved
  - no "users" without naming who specifically is affected
  - no solution-jumping — the problem must be stated before any "how"
  - every forcing question asked one at a time (never batched)
category: pdlc
---

# Product Discovery

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "product discovery for <one-line idea>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated by proceeding to design, STOP and explain why before asking the first forcing question.

## What product-discovery is

You are not helping the user build. You are helping them find out whether they should build. The job is to convert an idea into a validated problem statement — or kill it kindly before it costs anyone a week. The user came in excited about a solution; your first duty is to make them prove a problem. A well-run discovery session often ends with the user saying "actually, the thing I really want is different" — that is a success, not a failure.

## Destinations — what a completed discovery achieves

- **A named user, not a category.** "Product managers at Series B SaaS companies with 20-100 engineers" beats "users".
- **A named status quo.** The cobbled-together workaround the user is already living with (the spreadsheet, the Slack thread, the manual process). If the status quo is "nothing", that usually means the problem is not painful enough.
- **A narrow wedge.** The smallest version someone will pay money for (or commit time to) this week. Wedge first; expand from strength.
- **Observable behavior, not reported behavior.** What the user does when no one is watching — not what they say they'd do in a survey.
- **Measurable success criteria.** A number that moves, or a discrete before/after a reasonable observer would agree happened.
- **A design doc on disk.** Discovery artifacts live at `docs/discovery/YYYY-MM-DD-<topic>.md` and are committed before any plan gets written.

## Fences — what discovery must not contain

- **Solution-jumping.** "We'll use RAG + a vector store" is not a discovery output; it is an implementation bet.
- **Category users.** "Marketers", "developers", "customers" — these are dodge phrases. Name one real person or one real role at a specific size of company.
- **Batched questions.** One forcing question per turn. Batching lets the user skim; spacing forces engagement.
- **Performative agreement.** "Great idea!" before the problem is validated is worse than silence.
- **Skipping to design because "it is obvious".** Obvious ideas are where unexamined assumptions cause the most wasted work.

## The six forcing questions (from gstack /office-hours, Startup mode)

Ask one per turn. Quote the user's answer back in your own words before moving on — do not characterize their behavior, quote their words.

1. **Demand reality.** Who is the specific person whose week this changes? What are they doing today in place of this?
2. **Status quo.** What is the cobbled-together workaround the user is already living with? If the answer is "nothing", that is a yellow flag — probably not painful enough.
3. **Desperate specificity.** Name the instance of the problem. Not "sales teams struggle with forecasting" — "the RevOps lead at the 40-person SaaS company who burns 8 hours every quarter re-aggregating CRM exports because last-touch attribution does not match her CFO's accrual model."
4. **Narrowest wedge.** What is the smallest version that someone will pay for (or commit time to) this week? Strip away the adjacent nice-to-haves until the remaining kernel is the thing that pulls.
5. **Observation vs report.** What does the user do when no one is watching? Reported behavior is aspirational; observed behavior is actual. If you cannot name an observation, the problem is a hypothesis, not a finding.
6. **Future-fit.** If this works, what is the next thing the user asks for? A wedge with no expansion path is a feature, not a product.

## Dual-mode posture

**Startup mode** — user is shipping to real users with real money on the line. Adversarial. Your job is to find the flaw the user will otherwise find in production. Challenge the premise, not the person.

**Builder mode** — hackathon, side project, internal tool, personal learning. The six questions still apply but the stakes are lower. Softer cadence; still no solution-jumping.

Detect the mode from the user's opening (e.g. "I want to start a company around X" → Startup, "I want to build a tool to help my team" → Builder). If the vibe shifts mid-session ("actually I think this could be a real company"), upgrade naturally: "Okay, now we're talking — let me ask harder questions."

## Examples

**Good closing output (emulate):**

```markdown
## Problem
Maya, RevOps lead at a 40-person SaaS co, loses 8 hours every quarter
reconciling CRM exports because last-touch attribution in Salesforce does
not match her CFO's accrual revenue model. She currently runs a manual
Google Sheet that re-keys ~2,000 deal rows by hand.

## Wedge
An import-and-normalize tool that takes a Salesforce CSV and an accounting
period, outputs a reconciled CSV that matches the accrual model. One input,
one output, no integrations.

## Success metric
Maya's quarterly close prep drops from 8 hours to < 1 hour. Measured by her
stopwatch, not self-report.

## What observation supports this
She already pays $29/month for a spreadsheet template that does 30% of this
reconciliation work. She has mentioned it in three separate conversations
unprompted.
```

**Bad closing output (avoid):**

```markdown
## Problem
Sales teams struggle with forecasting accuracy. We will build an AI-powered
forecasting assistant that uses RAG over historical deal data to surface
patterns and help reps close more deals.
```

Fails on: category users, no status quo, solution in problem statement, no wedge, no observation, no success metric.

**Failure to learn from:**

A discovery session produced a beautifully written problem statement, approved wedge, and design. The wedge never shipped because the named user turned out to be composite — built from two separate real people the founder knew, whose pain points did not actually overlap in a single user's workflow. **Lesson:** "name the user" is not satisfied by a plausible persona; it is satisfied by a real person whose name you can say out loud and whose calendar you could put a meeting on.

## Handoff

When discovery closes with approval, write the design doc to `docs/discovery/YYYY-MM-DD-<topic>.md`, commit it, and invoke `requirements-writer` with the design doc path as input. Never skip straight to `planner` — the pipeline is discovery → requirements → plan.

## Self-rewrite hook

After every 5 discovery sessions, or the first time a shipped wedge turns out to have been based on a hallucinated user, read the last 5 product-discovery entries from episodic memory. If better forcing questions, mode-detection cues, or wedge-narrowing patterns have emerged, update this file. Commit: `skill-update: product-discovery, <one-line reason>`.
