# Workspace (live task state)

> Live "where are we right now" file. Updated when we move between steps,
> hit a blocker, or change direction. For the durable history of *why* we
> did things, see `.agent/memory/semantic/DECISIONS.md`.

## Current step

**Step 8.2.5 — sync fork to upstream `codejunkie99/agentic-stack` (v0.8.0 → v0.11.2)**

Inserted before Step 8.3 (real-case dry-run) because dry-running on a
6-version-stale base is not meaningful. Identified 2026-04-27 when user
asked about the previously-discussed weekly upstream sync — discovered
the cadence was scoped in `DOMAIN_KNOWLEDGE.md` (loop #6) but never
operationalized. Now operationalized: weekly cron + auto-memory entry.

## Why now

- 59 commits behind upstream, last common ancestor `a397568` (v0.8.0)
- 6 new tags upstream: v0.9.0, v0.9.1, v0.10.0, v0.11.0, v0.11.1, v0.11.2
- Major upstream additions worth absorbing: `harness_manager/` Python
  package (replaces bash install), data-layer monitor + dashboard,
  data-flywheel trainer, DESIGN.md skill, codex adapter, pi rewrite,
  Windows path-traversal security fix, Python 3.9 compat
- Step 8.3 dry-run + any further BCG adapter work should land on a
  current base, not a stale fork

## Stage plan (draft — confirm before executing)

- **8.2.5.1** — review-only: per-tag walkthrough (v0.9.0 → v0.11.2),
  classify each upstream change as (a) take as-is, (b) take with
  adaptation, (c) skip / our-version-wins. No code changes; produces a
  classification doc.
- **8.2.5.2** — merge mechanics decision: rebase 8.x work onto upstream,
  vs. merge upstream into master, vs. cherry-pick selected upstream
  commits. Likely **merge** given the divergence size and the fact that
  our 8.x history is a series of dated decisions we don't want to rewrite.
- **8.2.5.3** — execute the merge. Highest-risk file: `install.sh` —
  upstream gutted it to a thin Python dispatcher (`harness_manager/`),
  we extended it for BCG-conditional propagation in 8.2.1 + 8.2.3
  agent-memory copy-if-missing loop. Resolution: port our BCG block into
  `harness_manager/install.py` rather than keeping the bash logic.
- **8.2.5.4** — smoke-test both adapter states (disabled/enabled) on
  fresh installs into `/tmp/claude/825-{disabled,enabled}/`, same
  pattern as 8.2.1 / 8.2.4.
- **8.2.5.5** — log + DECISIONS.md entry + episodic learning.

## Open questions

- [ ] Merge vs. rebase strategy — recommend merge, awaiting confirm
- [ ] Take the `harness_manager/` Python package wholesale (yes likely)
      and port our install.sh BCG logic into it?
- [ ] Take `data-layer` and `data-flywheel` skills as-is, or treat as
      out-of-scope for now and gitignore the new examples?
- [ ] Any upstream commits to explicitly *not* take? (e.g., if their
      `.agent/skills/` restructure conflicts with our knowledge-work
      skill imports from 8.1)

## Next step

Get user confirm on stage plan + merge-vs-rebase, then start 8.2.5.1
(per-tag walkthrough).

## Recurring cadence

- Weekly upstream sync check: every Monday morning. Mechanism:
  `CronCreate` (durable, 7-day TTL, ID `ba87d58c`, fires Mon 9:13 local)
  re-armed each fire, plus auto-memory entry
  `upstream_sync_cadence.md` so the cadence survives session restarts
  beyond the cron's lifetime.

## Recent upstream-sync checks

- 2026-04-27 — base at v0.8.0 (`a397568`); 59 commits behind across 6
  tags through v0.11.2; merge work scoped as Step 8.2.5 (this step).
