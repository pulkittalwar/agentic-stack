# Workflows

Generic, shareable workflow definitions. A workflow is a canonical pattern
for producing a named deliverable — it declares the deliverable's contents,
the team composition (which agents/skills collaborate), review lenses,
quality gates, and output format.

Distinct from `.agent/skills/`: skills are reusable capabilities (analyze,
review, assemble); workflows compose skills + agents into a deliverable
recipe (situation-assessment, mid-case-findings-deck, …).

## Current set

Bootstrapped in Step 8.1 from Kenneth Leung's `harness-starter-kit` (BCG).
Each file has frontmatter with `workflow_id`, `name`, `team_structure`,
and `description`. The `sample-` prefix from the source was dropped —
in this repo these are canonical patterns, not samples.

| Workflow | Purpose |
|---|---|
| `situation-assessment.md` | Initial structured client-context + hypothesis + approach doc |
| `issue-tree-hypothesis.md` | MECE decomposition of the case question with supporting hypotheses |
| `mid-case-findings-deck.md` | Mid-engagement synthesis and insight surfacing |
| `final-recommendations-deck.md` | Culminating deliverable — recommendations + value + roadmap |
| `post-meeting-update.md` | Transcript → updates to tracker / RAID / workstream pages |
| `daily-task-tracking.md` | Daily transcript → Jira task pipeline with QA gates |

## Status

As of Step 8.2.2, every role reference in every workflow resolves to a
real agent in either `adapters/claude-code/agents/` (SDLC roster, always
installed) or `adapters/bcg/agents/` (BCG consulting roster, installed
only when `.agent/config.json` has `bcg_adapter: "enabled"`).

The reconciliation was hybrid:
- Three reviewer-lens roles were genuine distinct lenses and were authored
  as new BCG agents: `partner-strategy`, `partner-analytics`,
  `principal-delivery`.
- Six other orphan role labels from the starter-kit workflows were
  relabeled to canonical roster names: `framework-lead`, `case-analyst`,
  `transcript-analyst`, `jira-tracker-analyst` → `analyst`;
  `delivery-lead` → `program-manager`; `io-qa-auditor` → `test-lead`.

See `adapters/bcg/README.md` for the full BCG agent roster and
`.agent/memory/semantic/DECISIONS.md` for the reconciliation rationale.

## Conventions

- Filenames use kebab-case. The `workflow_id` in frontmatter matches the
  filename stem.
- `team_structure` is one of: `flat`, `coordinated`, `full`.
- Workflow definitions are read-only contracts; instantiating a workflow
  for a specific engagement produces artifacts under
  `.agent/memory/working/` or `context/project/`, not here.
