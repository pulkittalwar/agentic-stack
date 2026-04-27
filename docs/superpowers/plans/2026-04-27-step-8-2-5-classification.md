# Step 8.2.5 — Per-tag Classification (v0.9.0 → v0.11.2)

Classification of each upstream tag's changes for the fork sync.
Categories: TAKE-AS-IS / TAKE-WITH-ADAPTATION / SKIP-OURS-WIN.

Base: `a397568` (v0.8.0 baseline, merge-base with our master).
Target: `8ba0293` (v0.11.2, latest upstream).
Total: 59 commits across 6 tags.

## v0.9.0 — harness_manager Python backend (architectural shift)

**TAKE-WITH-ADAPTATION.** Replaces `install.sh` + `install.ps1` with a thin Python dispatcher pointing at a new `harness_manager/` package. Manifest-driven adapter installation: each adapter has its own `adapter.json` describing files (with merge_policy), optional `skills_link`, and optional `post_install` named built-in actions. Rejects DSL creep — codex review of v1.0 vision plan flagged generalized `run_command` so post_install actions are constrained to a registry of named functions.

**Adaptation needed:** our `install.sh` had a 61-line BCG-conditional propagation block (added in Step 8.2.1, extended in 8.2.3 with copy-if-missing agent-memory loop) that doesn't survive the dispatcher refactor. **Port:** new named `post_install` action `bcg_conditional_propagate` in `harness_manager/post_install.py`, registered in `harness_manager/schema.py` `VALID_POST_INSTALL_ACTIONS`, wired into `adapters/claude-code/adapter.json`. Extends `post_install.run()` signature to pass `stack_root` via kwargs (existing `openclaw_register_workspace` swallows extras via `**_kwargs` — non-breaking).

**Notable commits:**
- `de06531` feat(harness-manager): Python backend (install/doctor/remove/status/cli)
- `eafba1d` feat(harness-manager): adapter.json manifests for all 10 adapters
- `2bbb873` feat(harness-manager): adapter.json schema + stdlib validator
- `80a00ac` feat(install.sh): refactor to thin Python dispatcher
- `e46c838` feat(install.ps1): refactor to thin Python dispatcher (Windows parity)
- `d150f5b` feat(harness-manager): add `manage` TUI menu loop
- `db4e6b0` fix(schema)!: reject Windows-style path traversal (security)
- `90d77d9` harden episodic writes: fcntl lock + fix pi skills orphan sync
- `b64b80c` feat: add pi tool-result hook and windows installer
- `fb7b898` feat: add codex adapter
- `192341e` fix(openclaw): auto-wire AGENTS.md and register project-scoped agent

## v0.9.1 — pi adapter rewrite + image optimization

**TAKE-AS-IS.** Pi memory-hook rewrite (`0d64e23`) addresses three bugs: formula crash, decay timezone bug, inline TS hook. We don't customize pi.

**Notable commits:**
- `0d64e23` fix(pi): rewrite adapter — inline TS hook, formula crash, decay tz bug (#24)
- `f1c362d` chore: untrack tests/ (keeps local-only, out of release bottle)
- `bfbd00a` [ImgBot] Optimize images
- `49bd5e0` docs(diagram): refresh legacy architecture diagram for 10 adapters

Note on `f1c362d`: upstream removed `tests/` from tracking. We re-add `tests/test_bcg_conditional_propagate.py` for our smoke test in Stage 4 of the plan; that is intentional and not a regression of upstream's intent (which was to keep upstream's own e2e tests local-only, not to forbid downstream tests).

## v0.10.0 — DESIGN.md skill + data-layer + data-flywheel

**TAKE-AS-IS.** Three new skills (`data-flywheel`, `data-layer`, `design-md`), new top-level `schemas/` and `examples/` directories, two top-level test files (`test_data_flywheel_export.py`, `test_data_layer_export.py`), `harness_manager/` Python 3.9 compat.

**No collision** with our 13 knowledge-work + SDLC skill imports from Step 8.1 — the three new skill names are disjoint from ours.

**Notable commits:**
- `8985eb5` [codex] Add DESIGN.md skill support (#21)
- `62f4e6b` feat: add cross-harness data layer dashboard
- `56e0939` feat: add data flywheel trainer artifacts
- `f0cd73b` fix(harness_manager): support Python 3.9 (closes #27)

## v0.11.0 → v0.11.2 — data-dashboard polish

**TAKE-AS-IS.** Terminal dashboard shown by default in v0.11.0; natural-language dashboard in v0.11.2; brew formula bumps. No conflicts.

**Notable commits:**
- `f041370` feat: show data layer terminal dashboard by default (v0.11.0)
- `df806ab` feat: make data dashboard natural language (v0.11.2)
- chore(formula) bumps for v0.11.0/v0.11.1/v0.11.2

## Files we kept (no upstream collision — 92 files)

- `adapters/bcg/**` — entire BCG adapter (16 agents, 16 agent-memory templates, scripts, commands, protocols, context, templates, skills) from Step 8.0/8.2.x
- `.agent/context/**` — 4 generic-consulting files (frameworks, glossary, quality-standards, README) from Step 8.2.4
- `.agent/personas/**` — 4 firm-generic persona files (executive-sponsor, program-director, _template, README) from Step 8.2.3
- `.agent/skills/**` — all 13 knowledge-work + SDLC skill dirs imported in Steps 4–8 (analysis, architect, code-reviewer, context-search, document-assembly, draft-status-update, implementer, planner, product-discovery, release-notes, requirements-writer, review, spec-reviewer)

## Conflicts (resolution per main plan)

| File | Strategy |
|---|---|
| `install.sh` | Take theirs (38-line dispatcher); port BCG block to `harness_manager/post_install.bcg_conditional_propagate` |
| `.agent/skills/_index.md` | Mechanical merge — disjoint skill names |
| `.agent/skills/_manifest.jsonl` | Mechanical merge — 20 ours + 3 theirs, no overlap |
| `.agent/memory/semantic/DECISIONS.md` | Ours-wins (project history) |
| `.agent/AGENTS.md` | Auto-merge (no conflict) |
| `.gitignore` | Auto-merge (no conflict) |
