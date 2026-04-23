---
name: release-notes
version: 2026-04-23
description: Use whenever a set of merged changes needs to be translated into user-facing communication — before a tag, before a deploy, before a changelog entry, or whenever the user asks "what changed". Produces release notes sectioned by audience (users / operators / developers), surfaces breaking changes with explicit upgrade paths, proposes a version bump grounded in semver, and updates CHANGELOG + docs in one pass. Triggers on "write release notes", "update the changelog", "what changed in this release", "document the release", or after a batch of commits is ready to tag.
triggers: ["write release notes", "update the changelog", "what changed", "document the release", "release notes", "changelog entry"]
tools: [recall, git, bash]
sources:
  gstack: document-release (per-file audit + cross-doc consistency + version-bump decision)
preconditions: ["at least one merged commit since the last release tag"]
constraints:
  - sections are by audience (users / operators / developers) — never just a commit dump
  - breaking changes have an explicit upgrade path, not "see commit history"
  - version bump is proposed with rationale tied to semver rules
  - every entry traces back to the commit or PR that introduced it
category: sdlc
---

# Release Notes

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "release notes for <version or tag>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated (e.g. a prior release shipped a silent breaking change because the writer missed it), STOP and explain.

## What a release-notes skill is

Release notes are the contract between engineering and everyone else. A user reads them to decide whether to upgrade; an operator reads them to know what will change in their stack; a developer reads them to know what APIs moved. A release note that reads like a git log is a failure of translation — the reader came for "what changed for me", not "what changed in the repo".

## Destinations — what completed release notes achieve

- **Sectioned by audience.** Three passes over the same diff, each answering a different question:
  - **Users:** what can I do now that I could not do before? What looks different?
  - **Operators:** what changes about deploying, monitoring, or running this? What new config exists? What alerts might fire?
  - **Developers:** what APIs, types, or contracts changed? What imports broke?
- **Breaking changes surfaced at the top.** Every breaking change has a one-line upgrade path: the exact edit, flag, or config the user makes.
- **Grouped by semantic category.** Added / Changed / Deprecated / Removed / Fixed / Security. The Keep-a-Changelog categories — proven for both humans and tools.
- **Traceable.** Every entry carries a PR or commit reference. `docs: add timezone handling (#412, 5f3a9b)`. Future debug sessions thank you.
- **A version-bump proposal.** Patch / Minor / Major, with one-line rationale citing the semver rule that applies.
- **Cross-doc consistency.** README, docs/, and CHANGELOG all agree on what changed. If a new feature is announced in release notes but missing from README, the release is half-done.

## Fences — what release notes must not contain

- **"Misc fixes"** or "various improvements" buckets that hide breaking changes or security fixes. Every change is categorized or it does not ship.
- **Copy-pasted commit messages.** "feat(auth): wire up JWT rotation — part 2" is an engineering artifact, not a release note. Translate it.
- **Breaking changes without an upgrade path.** "This breaks X. Please update your config." is hostile; write the exact config edit.
- **Release notes that contradict the diff.** Every claim in the notes must be verifiable against the diff in under a minute.
- **Silent version bumps.** A major bump without an explicit "why major" paragraph is a minefield for downstream consumers.

## The semver decision (grounded in the spec)

Propose the version bump by applying, in order:

1. **Breaking change in a public contract?** → MAJOR. Public contract = anything a consumer (user, API caller, importing package) depends on. Internal refactors do not count unless they are visible.
2. **New functionality added in a backwards-compatible way?** → MINOR.
3. **Bugfixes, docs, internal-only changes?** → PATCH.

State the rule that applied. "MAJOR because `reconcile()` signature changed from `(deals, period)` to `(deals, period, *, strict=False)`, which breaks callers that used positional args."

## The nine steps (from gstack /document-release)

Run in order — earlier steps constrain later ones.

1. **Detect platform + base branch.** What deploy target, what version-tagging convention, what CHANGELOG format.
2. **Diff analysis.** `git log <last-tag>..HEAD` gives the commit range. Read each commit's diff, not just its message — messages lie, diffs do not.
3. **Per-file documentation audit.** For each changed file, check whether README, docstrings, type hints, or public-facing docs need updates.
4. **Apply auto-updates.** Mechanical doc updates (e.g. version strings, updated imports in examples) apply without asking.
5. **Ask about risky / questionable changes.** Anything where intent is unclear from the diff — ask the user before writing it into release notes as a claim.
6. **CHANGELOG voice polish.** Match the project's existing tone (formal vs casual, user-focused vs developer-focused). If no CHANGELOG exists, propose one in Keep-a-Changelog format.
7. **Cross-doc consistency check.** Scan README, docs/, API reference. Any mention of old behavior that contradicts the new behavior gets flagged.
8. **TODOS cleanup.** Any TODO that was resolved by this release → remove. Any still-open → mark in the notes as "Known limitations".
9. **Version bump + commit.** Propose the version, state the rule, get confirmation, then commit the notes + CHANGELOG + version-file bump in one commit.

## Examples

**Good release notes (emulate):**

```markdown
# reconcile v0.3.0 — 2026-04-23

## Breaking changes

- **`reconcile()` now requires a keyword `strict` argument** (#412).
  Upgrade: callers using positional args must pass `strict=False` (old
  behavior) or `strict=True` (new, stricter validation).
  Before: `reconcile(deals, period)` — now fails with TypeError.
  After:  `reconcile(deals, period, strict=False)`.

## Added (users)

- **Gap CSV output** (#412). When deals in the SFDC export cannot be
  matched to a NetSuite period, a second CSV is written alongside the
  reconciled one listing each gap with a reason code. See
  `docs/usage.md#gap-handling`.
- **Exit-code discipline** (#418). The CLI now exits 0 on clean runs,
  2 on warnings (> 5% of rows in gaps), 1 on hard failures. Useful for
  cron-driven pipelines.

## Changed (operators)

- **Log volume reduced ~40%** (#420). Per-row trace logs moved from
  INFO to DEBUG. Set `RECONCILE_LOG_LEVEL=DEBUG` to restore prior verbosity.

## Fixed

- Timezone-boundary deals straddling quarter-end no longer get assigned
  to the wrong period (#408). Previously off-by-one for US/Pacific inputs.

## Security

- No security-relevant changes.

## Version rationale

**MINOR bump (0.2.1 → 0.3.0).** New `strict` parameter is a breaking
change in the strict semver reading, but the default value preserves
prior behavior for non-positional callers, and the project is pre-1.0,
where the convention is to bump MINOR for feature-additions. A post-1.0
version of this same change would be MAJOR.
```

**Bad release notes (avoid):**

```markdown
# v0.3.0

- Various improvements and fixes
- Updated reconcile function
- Added gap handling
- Bumped version
```

Fails on: misc-fixes bucket, no audience sections, no breaking-change callout, no PR/commit refs, no upgrade path, no version rationale.

**Failure to learn from:**

A release note said "Added gap CSV output" but the feature was behind a feature flag that defaulted to off. Users upgraded, did not see gap CSVs, and filed bugs assuming the feature was broken. **Lesson:** the release note must distinguish "available" from "enabled by default". If a feature is flagged, say so in the note with the exact flag name. If it is enabled by default, say that too — readers should never guess.

## Save + handoff

Release notes live in two places: (1) `CHANGELOG.md` entry per Keep-a-Changelog format; (2) a standalone announcement at `docs/releases/YYYY-MM-DD-v<version>.md` for richer commentary. After writing, propose the version bump, get confirmation, then make one commit covering CHANGELOG + release doc + version-file update. Push, tag, hand off to whoever drives the actual deploy.

## Self-rewrite hook

After every 5 releases documented, or the first time a released feature causes confusion the release notes should have prevented, read the last 5 release-notes entries from episodic memory. Tighten fences or add new audience sections (e.g. "security" if security-relevant changes become frequent). Commit: `skill-update: release-notes, <one-line reason>`.
