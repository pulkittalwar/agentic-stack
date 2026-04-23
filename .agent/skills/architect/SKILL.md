---
name: architect
version: 2026-04-23
description: Use whenever a spec is approved and the next artifact needed is a system design — component boundaries, data flow, error paths, dependency graph, and test seams. Produces an ASCII component diagram, typed interfaces between modules, a data-flow diagram with failure branches, an edge-case matrix, and an explicit test-seam list. Triggers on "design the system", "architecture for this", "how should this be structured", or when a spec moves to planning without a structural design.
triggers: ["design the system", "architecture for this", "how should this be structured", "component diagram", "data flow"]
tools: [recall, git, bash]
sources:
  gstack: plan-eng-review (architecture + data flow + edge cases + test matrix sections)
preconditions: ["spec is approved (spec-reviewer verdict: APPROVED or APPROVED WITH GAPS)"]
constraints:
  - ASCII component diagram with named interfaces, not free-form boxes
  - data flow diagram includes failure branches, not just happy path
  - every component has a named test seam
  - assumptions are enumerated, not left implicit
category: sdlc
---

# Architect

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "architecture for <feature>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated, STOP and explain.

## What an architect is

The architect is the translator between what the system should do (spec) and how it will be structured (design). The design is a map the implementer reads before touching code. Bad architecture is recognizable a week after implementation starts — tests are hard to write, modules grow faster than capabilities, every new story requires touching five files. Good architecture is recognizable a year later — modules still have the same boundaries the diagram showed on day one. The diagram is a promise; honor it by making the promise specific enough to hold.

## Destinations — what a completed architecture achieves

- **An ASCII component diagram.** Boxes are modules; arrows are typed calls. Every arrow has a name — a function signature, a message-queue topic, an HTTP endpoint. "Component A calls Component B" is not an arrow; "`A.parse(csv: bytes) -> list[Deal]` called by B" is.
- **A data-flow diagram with failure branches.** Data enters, transforms, persists, exits. At each hop, name what happens when the hop fails. Silent failures are the worst architecture bug.
- **An edge-case matrix.** For each component, what happens on: empty input, malformed input, partial input, concurrent input, duplicated input, out-of-order input. Not every row applies; filling in "N/A" is legitimate and signals the architect considered it.
- **Test seams.** For every component, name the interface at which a test can inject inputs and observe outputs without spinning up the full system. If there is no test seam, the component will be untestable — redesign until every component has one.
- **An assumption ledger.** Everything the design depends on that is not enforced by the codebase — third-party SLAs, data shapes, version constraints, permission contexts. Assumptions that turn out false are the incident post-mortem's first bullet.
- **Blast-radius annotation.** For every component, name the files/modules that import it or are imported by it. Blast radius is the unit of change; a design with unclear blast radius hides future pain.

## Fences — what the architecture must not contain

- **UML for UML's sake.** Diagrams that do not lead to a code-level decision are ceremony. Every diagram earns its space by changing an implementation bet.
- **`TBD: infra`** or any "we'll figure it out". If the infrastructure boundary is unresolved, the design is not finished; say so and ask.
- **Untested happy-path-only flows.** If the data-flow diagram has no failure branches, the architect did not yet think about failure.
- **Single-component designs.** A one-box diagram is a file, not a system. Either the scope is too small for this skill, or the design is too shallow.
- **Implicit assumptions.** Anything you would have said "obviously…" about belongs in the assumption ledger. "Obvious" is where incidents come from.

## The five-section structure (from gstack /plan-eng-review)

Produce these in order — earlier sections constrain later ones.

### 1. Component diagram
Boxes = modules. Arrows = typed calls with named signatures. Group by responsibility, not by layer. Keep under 10 boxes per diagram; if more are needed, nest.

### 2. Data flow
Trace one concrete input end-to-end. For each hop: input type, transformation, output type, failure mode. Use the "blast radius" lens — files touched at each hop.

### 3. Edge-case matrix
Table: rows = components, columns = edge conditions (empty, malformed, partial, concurrent, duplicate, out-of-order). Every cell answers what happens.

### 4. Test-seam list
For each component: at what interface can a test inject + observe? If a component has no seam, redesign — do not paper over with end-to-end tests.

### 5. Assumption ledger
Bullets. Each: the assumption, why it matters, what happens if violated, how it can be verified.

## Principles

- **Boil lakes.** Fix everything in the design's blast radius (files it changes + direct importers) if inside < 1-day scope. Flag larger expansions; do not silently absorb.
- **Explicit over clever.** A 10-line obvious design reads in 30 seconds for a new contributor. A 200-line abstraction reads in an hour. Prefer the 10-line design unless the abstraction buys verified reuse.
- **Design for testability first.** If a component is hard to test, it is hard to change. Architecture that optimizes for testability is architecture that stays honest over time.
- **Types at boundaries.** Every arrow in the diagram has a type signature. Types are documentation that cannot rot.

## Examples

**Good architecture output (emulate):**

```markdown
# Architecture: reconcile-v1

## Components
```
  ┌──────────────┐    parse(csv_bytes) -> list[Deal]     ┌──────────────┐
  │  cli         │ ──────────────────────────────────▶  │  sfdc_parser │
  │              │                                       │              │
  │              │    load(period) -> NetSuitePeriod     ┌──────────────┐
  │              │ ──────────────────────────────────▶  │  ns_loader   │
  │              │                                       │              │
  │              │    reconcile(deals, period) -> Result ┌──────────────┐
  │              │ ──────────────────────────────────▶  │  reconciler  │
  └──────────────┘                                       └──────────────┘
                                                               │
                                                 write_csv(path, rows)
                                                               ▼
                                                       ┌──────────────┐
                                                       │  output      │
                                                       └──────────────┘
```

## Data flow (happy + failure)

```
  stdin CSV ──▶ sfdc_parser ──▶ list[Deal]
                     │
                     └─ parse failure ──▶ exit 2, stderr "malformed: row N"

  --period ──▶ ns_loader ──▶ NetSuitePeriod
                     │
                     └─ period closed ──▶ exit 2, stderr "period not found"

  (Deals, Period) ──▶ reconciler ──▶ Result
                           │
                           └─ > 5% gaps ──▶ exit 2 but still write output + gap CSV
```

## Edge-case matrix

| Component     | empty | malformed | partial  | concurrent |
|---------------|-------|-----------|----------|------------|
| sfdc_parser   | exit 0, empty Deal list | exit 2 with row N | N/A | N/A (single file) |
| ns_loader     | N/A | N/A | warn + proceed | N/A (read-only) |
| reconciler    | empty Result | N/A | partial Result + gap CSV | N/A |

## Test seams

- `sfdc_parser.parse(bytes) -> list[Deal]` — unit test with fixture bytes.
- `ns_loader.load(str) -> NetSuitePeriod` — unit test with mock HTTP layer.
- `reconciler.reconcile(deals, period) -> Result` — unit test with in-memory inputs.
- `cli.main(argv) -> int` — integration test with tmpdir.

## Assumptions

- Salesforce export uses US/Pacific timezone for `close_date`. If violated:
  off-by-one-day reconciliation errors at quarter boundaries. Verify by
  inspecting three exports from three different Salesforce orgs.
- NetSuite period is closed at run time. If violated: numbers change
  between runs. Verify via the "is closed" API call before proceeding.
```

**Bad architecture output (avoid):**

```markdown
# Architecture

The system has a backend and a frontend. The backend talks to a database
and exposes APIs. The frontend calls the APIs. We'll use Redis for caching
and figure out deployment later.
```

Fails on: no typed interfaces, no data flow, no edge cases, no test seams, TBD infra, implementation choice (Redis) not tied to a requirement.

**Failure to learn from:**

An architecture diagram had clean module boundaries on paper but one component held a shared mutable state that both neighbors read and wrote. The diagram was structurally clean but the hidden shared state meant every test had to spin up both neighbors. The refactor took three weeks. **Lesson:** the test-seam section is the architecture's honesty check. If you cannot name a test seam per component without needing neighbors, the boundary is fictional. Redesign before it ships.

## Save + handoff

Architecture docs land at `docs/architecture/YYYY-MM-DD-<feature-slug>.md`. After saving, hand to `planner` with the architecture doc path as input. The plan will reference the architecture doc when naming files per task.

## Self-rewrite hook

After every 5 architectures produced, or the first time a shipped design has its test-seam promise broken by hidden shared state, read the last 5 architect entries from episodic memory. Tighten the test-seam and assumption-ledger fences. Commit: `skill-update: architect, <one-line reason>`.
