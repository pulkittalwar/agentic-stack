# Personas

**Reviewer style overlays.** A persona is not an agent; it is a set of
demands, rejection criteria, and voice that an agent loads on top of its
base behavior when the reviewer's identity matters.

Pattern adopted from `harness-starter-kit` (Kenneth Leung, BCG) in Step
8.1. See `_template.md` for the shape.

## When to load a persona

The `reviewer` subagent loads a persona when the deliverable will be
consumed by a specific audience whose demands shape the review bar. The
generic "review against LESSONS.md" pass happens first; the persona
layers on top and may reject items the generic pass missed.

Examples of when a persona changes the output:
- A `board-ready-reviewer` demands pyramid-principle framing; a
  `detail-oriented-pm` demands every acceptance criterion be explicitly
  checked.
- A `skeptical-exec` rejects three-page memos; a `methodology-rigorous`
  partner rejects unmarked assumptions.

## Generic vs. BCG-specific

- **Generic personas** live in this directory. Shareable archetypes that
  don't identify specific individuals: `skeptical-exec`,
  `board-ready-reviewer`, `detail-oriented-pm`, `friendly-cto`, etc.
- **BCG-specific personas** live in `adapters/bcg/personas/` and are
  gitignored. Real partner/principal review styles, possibly names —
  engagement-sensitive, never on public fork.

## Shape of a persona file

Each persona is a single markdown file named after the archetype
(`skeptical-exec.md`, not `partner-someone-specific.md` — that belongs in
the BCG adapter). Structure per `_template.md`:

1. One-sentence opening: what I review for, my bar.
2. **What I Always Ask** — the five-ish standing questions.
3. **What I Reject Without Revision** — hard failure modes.
4. **My Communication Style** — voice + length + format preferences.

Keep each persona under 40 lines. A persona that needs more is probably
two personas.

## Status

Directory is scaffold as of Step 8.0 (2026-04-24). Content is added as
real reviewer archetypes surface during Phase 2/3 case work. Seed with
generic archetypes only; BCG-specific partners go in the adapter.
