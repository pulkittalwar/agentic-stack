# Workspace (live task state)

> Live "where are we right now" file. Updated when we move between steps,
> hit a blocker, or change direction. For the durable history of *why* we
> did things, see `.agent/memory/semantic/DECISIONS.md`.

## Current step

**Step 8.3 — real-case dry-run (next)**

Step 8.2.5 (fork sync v0.8.0 → v0.11.2) completed 2026-04-27. Base now
at upstream v0.11.2 plus our 8.x BCG/SDLC work plus the harness_manager
BCG port. Plan + classification: `docs/superpowers/plans/2026-04-27-step-8-2-5-*`.

## Why now

The roster is complete (5 SDLC + 16 BCG agents, 17 skills + 3 new from
upstream, 6 workflows, generic context, BCG adapter content) and the
install path is current and Python-driven. 8.3 exercises the stack
against a real consulting workflow to surface gaps the unit-level
smoke tests can't.

## Stage plan (TBD)

To be scoped at start of 8.3.

## Recurring cadence

- Weekly upstream sync check: every Monday morning. Mechanism:
  `CronCreate` (durable, 7-day TTL, ID `ba87d58c`, fires Mon 9:13 local)
  re-armed each fire, plus auto-memory entry `upstream_sync_cadence.md`
  so the cadence survives session restarts beyond the cron's lifetime.

## Recent upstream-sync checks

- 2026-04-27 — base WAS v0.8.0 (`a397568`); 59 commits behind across 6
  tags through v0.11.2. Merged via Step 8.2.5. Base now v0.11.2 + 8.x
  + BCG harness_manager port. Two upstream regressions discovered &
  fixed locally (cli.py future import, claude-code adapter.json SDLC
  agent entries) — candidates to upstream as PRs to codejunkie99.
