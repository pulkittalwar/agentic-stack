---
name: story-decomposer
version: 2026-04-23
description: Use whenever a feature-level spec exists and needs to be split into stories each team can ship independently in under a week. Produces a story list where every story is independently valuable, sized, estimable, and vertically sliced (not horizontally layered). Triggers when the user says "break this into stories", "decompose this", "split this feature", "user stories", or when a spec is too large for a single plan.
triggers: ["break this into stories", "decompose this feature", "user stories", "story decomposition", "split this feature"]
tools: [recall, git, bash]
sources:
  superpowers: writing-plans (partial — bite-sized discipline)
  gstack: autoplan (decomposition + blast-radius analysis)
preconditions: ["feature-level spec exists with requirements + acceptance criteria"]
constraints:
  - each story is independently shippable (delivers user value alone)
  - each story fits in < 1 week for one engineer
  - dependencies between stories are named explicitly
  - vertical slices preferred over horizontal layers
category: pdlc
---

# Story Decomposer

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "story decomposition for <feature>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated, STOP and explain.

## What a story-decomposer is

The story-decomposer turns a feature into a sequence of stories each of which is a complete increment of user value. The difference between a story and a "technical task" is that you can demo a story to the user and they nod; you cannot demo "set up the database schema" because nothing visible happened. When in doubt: if the story does not change what a user can observe, do, or avoid, it is not a story — it is scaffolding, and scaffolding belongs inside a story, not as its own story.

## Destinations — what a completed decomposition achieves

- **Every story delivers user-observable value.** A user (or operator, or developer) can point at the story and say "after this, I can do X that I could not do before."
- **Every story fits in under a week** for one engineer. Stories over a week are features in disguise; split them.
- **Stories are vertical slices.** Each one cuts through all layers (data → API → UI) for a narrow capability, rather than "the backend for all capabilities" followed by "the frontend for all capabilities". Vertical keeps every story shippable; horizontal leaves you with half a feature for weeks.
- **Dependencies are explicit.** If Story B needs Story A done first, say so and explain why. No hidden ordering.
- **Each story has acceptance criteria carried forward** from the spec — not rewritten, not paraphrased, copied. Rewording drifts meaning.
- **Blast radius is noted per story.** Which files/modules get touched, which direct importers are affected.

## Fences — what decomposition must not contain

- **Technical tasks disguised as stories.** "Set up the database", "refactor the auth module", "write the API layer" — these are scaffolding, not stories.
- **Horizontal layer splits.** "Story 1: all the backend. Story 2: all the frontend." You shipped nothing until Story 2 is done. Wrong.
- **Stories over a week.** A > 1-week story is a feature you have not yet decomposed. Split it.
- **Silent ordering.** If the stories must be done in a specific order, write the order down. "Implicit" ordering collapses when the team parallelizes.
- **Stories without acceptance criteria.** If you moved acceptance criteria to "we'll figure it out during implementation", you regressed to a wish.

## INVEST as the shape check (superpowers discipline)

A story that fails any of these is not a story yet:

- **I — Independent.** Can ship without waiting on another story in the same batch (or dependencies are named and narrow).
- **N — Negotiable.** The details can still be discussed; the story captures intent, not an implementation contract.
- **V — Valuable.** A user, operator, or developer sees value after this alone.
- **E — Estimable.** You can put a confidence range on effort (e.g. 1–3 days) without doing the whole design.
- **S — Small.** Under a week for one engineer. Ideally 2–4 days.
- **T — Testable.** The acceptance criteria are specific enough that a test (manual or automated) can verify them.

## The blast-radius discipline (from gstack /autoplan)

For each story, name the files modified + their direct importers. Expansions inside the blast radius and < 1 day of effort fold into the story; larger ones get flagged as a separate story or deferred. This prevents the "while I'm in there, I'll also fix…" creep that turns a 3-day story into a 10-day story.

## Examples

**Good decomposition (emulate):**

A spec for "CSV reconciliation tool" decomposes into:

```markdown
## Story 1: Single-file reconciliation happy path
**Value:** Maya can run `reconcile --sfdc input.csv --period 2026-Q2` and get
a correctly-reconciled output CSV for a clean input file.
**Acceptance:** (copied from spec R-3 clauses 1-3)
**Size:** 2-3 days. **Depends on:** none.
**Blast radius:** new package `reconcile/`, touches nothing existing.

## Story 2: Gap CSV for unmatched deals
**Value:** Maya sees which deals did not match NetSuite in a separate gaps
CSV she can triage.
**Acceptance:** (copied from spec R-3 clause 4)
**Size:** 1 day. **Depends on:** Story 1 (extends the join path).
**Blast radius:** `reconcile/core.py` + new `reconcile/gaps.py`.

## Story 3: Exit-code discipline and stderr reporting
**Value:** Maya's downstream cron job can tell a run succeeded vs ran with
warnings vs failed, without parsing stdout.
**Acceptance:** (copied from spec R-3 clause 5)
**Size:** < 1 day. **Depends on:** Story 2 (exit code uses gap fraction).
**Blast radius:** `reconcile/cli.py` only.
```

Each story is shippable on its own. Story 1 alone is a useful tool.

**Bad decomposition (avoid):**

```markdown
## Story 1: Build the CSV parser
## Story 2: Build the NetSuite join logic
## Story 3: Build the gap detection
## Story 4: Wire up the CLI
## Story 5: Add tests
```

Fails on: horizontal layers (nothing ships until Story 4), Story 5 is scaffolding, no acceptance criteria, no sizes, no blast radius, implicit hard ordering.

**Failure to learn from:**

A decomposition declared "independent" for two stories that touched the same transactional boundary in the database. They were built in parallel; both shipped; one silently corrupted the other's state under concurrent load. **Lesson:** independence claims must be verified at the data/transactional boundary, not just at the code-file boundary. When two stories write to the same table or message bus, name the dependency explicitly even if the file paths do not overlap.

## Self-review before handoff

1. **INVEST pass.** Check every story against the six letters. Fail any letter → fix or split.
2. **Horizontal-layer scan.** If two consecutive stories look like "build the X layer" and "build the Y layer", you sliced horizontally. Re-cut vertically.
3. **Blast-radius overlap.** For any two "independent" stories, list the files they both touch. Any overlap → re-evaluate independence.

## Save + handoff

Stories land in the spec doc as a new section, or in `docs/stories/YYYY-MM-DD-<feature>.md`. Hand off to `spec-reviewer` for a go/no-go on the decomposition before invoking `planner` on each story individually.

## Self-rewrite hook

After every 5 decompositions, or the first time a declared-independent story-pair corrupts each other in production, read the last 5 story-decomposer entries from episodic memory. Update fences or independence-check patterns if new failure modes have emerged. Commit: `skill-update: story-decomposer, <one-line reason>`.
