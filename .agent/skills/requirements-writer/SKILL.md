---
name: requirements-writer
version: 2026-04-23
description: Use whenever a validated problem statement exists (typically handed off from `product-discovery`) and the next step is a spec an engineer can build from. Produces requirements with explicit acceptance criteria, declared scope mode (Expansion / Selective / Hold / Reduction), named non-goals, and a coverage map from each requirement back to the problem it addresses. Triggers when the user says "write the spec", "turn this into requirements", "what do we need to build", or when a design doc arrives without acceptance criteria.
triggers: ["write the spec", "write requirements", "turn this into a spec", "acceptance criteria", "what do we need to build"]
tools: [recall, git, bash]
sources:
  superpowers: brainstorming (elicitation + spec self-review)
  gstack: plan-ceo-review (four scope modes + completeness-is-cheap)
preconditions: ["validated problem statement exists (not a bare idea)"]
constraints:
  - every requirement has explicit acceptance criteria
  - scope mode is declared upfront (Expansion / Selective / Hold / Reduction)
  - "NOT in scope" section is present and populated
  - every requirement traces back to a line in the problem statement
category: pdlc
---

# Requirements Writer

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "requirements spec for <feature name>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated, STOP and explain.

## What a requirements-writer is

The requirements-writer is the last document writer before engineering begins. Discovery named the problem; this skill names the solution's shape precisely enough that `planner` can decompose it and `implementer` can build it. Vague requirements ("the system should be fast", "handle errors appropriately") are not requirements — they are wishes, and they leak into bug reports three months later.

## Destinations — what a completed spec achieves

- **A declared scope mode.** Which of the four — Expansion, Selective, Hold, Reduction — applies to this spec? The mode changes what "done" means and what the reviewer optimizes for.
- **Every requirement has acceptance criteria.** Given / when / then, or a concrete observable check. "The system handles empty inputs gracefully" is not acceptance criteria; "given an empty CSV, the tool exits with code 0 and writes `empty_input` to stderr" is.
- **A populated `NOT in scope` section.** What was considered and deliberately excluded. This is where scope creep gets pre-empted.
- **Traceability.** Every requirement has a one-line pointer back to the problem statement line it addresses. Orphan requirements are scope creep; unaddressed problem lines are coverage gaps.
- **Explicit assumptions.** Everything the spec depends on that is not guaranteed by the codebase or environment — API versions, data shapes, user permissions, third-party SLAs.

## Fences — what the spec must not contain

- **Wish words:** "fast", "scalable", "appropriate", "best effort", "graceful", "intuitive". Each is a request for mercy disguised as a requirement.
- **"Handle edge cases"** without enumerating them.
- **Implementation choices smuggled in as requirements.** "Use Redis for caching" is a design decision; the requirement is "read path returns < 50ms p95 under 100 rps".
- **Invisible scope.** Any capability expected by the user that is not written down will surface as a shipping-day surprise.
- **Un-traced requirements.** If a requirement does not answer "which problem line does this solve", it should be moved to `NOT in scope` or cut.

## The four scope modes (from gstack /plan-ceo-review)

Declare one at the top of the spec. The mode is not just documentation — it changes your posture.

- **EXPANSION.** You are building a cathedral. Envision the platonic ideal. Ask "what would make this 10x better for 2x the effort?" Every expansion is presented to the user as an opt-in; you recommend enthusiastically, the user decides.
- **SELECTIVE EXPANSION.** You hold the stated scope as baseline and make it bulletproof. Separately, surface every expansion opportunity as an individual opt-in. Neutral recommendation posture.
- **HOLD SCOPE.** Scope is accepted. Your job is to make it bulletproof — catch every failure mode, enumerate every edge case, map every error path, specify every observability hook. Do not silently expand or reduce.
- **REDUCTION.** You are a surgeon. Find the minimum viable version that achieves the core outcome. Cut everything else ruthlessly.

**Completeness is cheap.** AI compresses implementation time 10–100×. When evaluating "approach A (full, ~150 LOC) vs approach B (90%, ~80 LOC)", prefer A. The 70-line delta costs seconds to write. Ship the lake, not the puddle.

## Examples

**Good requirement (emulate):**

```markdown
### R-3: Attribution reconciliation between SFDC and NetSuite

**Problem line addressed:** P-2 ("Maya's 8-hour manual reconciliation").

**Given:** a Salesforce deal export CSV (schema: `deal_id`, `close_date`,
`amount_usd`, `touch_type`) and a NetSuite accounting period (YYYY-QN).

**When:** the user runs `reconcile --sfdc input.csv --period 2026-Q2`.

**Then:**
- Output CSV is written to `./reconciled_2026-Q2.csv` with columns
  `deal_id`, `accrual_date`, `accrual_amount_usd`, `variance_from_sfdc`.
- Every input row is present in output (join is left-outer on `deal_id`).
- Deals without a NetSuite match are emitted with `accrual_date=NULL`
  and a `reconciliation_gap` flag in a second CSV (`./gaps_2026-Q2.csv`).
- Exit code 0 on success; 2 if > 5% of rows land in gaps CSV.

**Non-goals:** bi-directional sync, real-time reconciliation, UI.

**Assumptions:** Salesforce export uses US/Pacific timezone for
`close_date`; NetSuite period is closed at time of run.
```

**Bad requirement (avoid):**

```markdown
### R-3: Attribution reconciliation

The system should reconcile Salesforce data with NetSuite accounting
data in a fast and reliable way. Handle edge cases like timezone
differences and missing deals gracefully. Should scale to enterprise
volumes.
```

Fails on: wish words (fast, reliable, gracefully), no given/when/then, no non-goals, no assumptions, no traceability.

**Failure to learn from:**

A spec declared HOLD SCOPE at the top but the reviewer quietly added three "small" clarifications during review that together doubled the implementation time. The mode was honored by the author but violated by the reviewer because the mode was not stated loudly enough to anchor the review conversation. **Lesson:** the scope-mode declaration belongs at the top of both the spec AND the review call; restate it at the start of any review session so drift is caught before it compounds.

## Self-review before handoff

Run three passes over the draft:

1. **Wish-word scan.** Search for `fast`, `scalable`, `appropriate`, `best effort`, `graceful`, `intuitive`, `simple`, `easy`. Rewrite every hit into an observable check.
2. **Traceability check.** For each requirement, write the problem-line ID it addresses. Flag any orphans.
3. **Non-goals check.** Is there at least one entry in `NOT in scope`? An empty non-goals section means you have not yet thought adversarially about what a reader might assume is included.

## Save + handoff

Spec lands at `docs/specs/YYYY-MM-DD-<feature-slug>.md`. After saving, invoke `story-decomposer` (for feature-level specs that need story-level decomposition) or hand directly to `spec-reviewer` (for already-story-sized specs).

## Self-rewrite hook

After every 5 specs produced, or the first time a shipped feature reveals a requirement the spec silently assumed, read the last 5 requirements-writer entries from episodic memory. If a new fence word (a wish-word category not yet caught) or a new scope-mode failure pattern has emerged, update this file. Commit: `skill-update: requirements-writer, <one-line reason>`.
