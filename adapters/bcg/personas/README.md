# BCG personas (adapter layer)

**Private, gitignored.** BCG-specific partner/principal review styles.
This directory holds actual colleague review dynamics — names, demands,
rejection patterns, voice — that are engagement-sensitive and must never
ship to the public fork.

See `../../.agent/personas/README.md` for the generic-archetype pattern
and when to load personas at all.

## What goes here

Personas that identify or characterize specific BCG individuals. A
persona whose demands match a known partner's review style, named
accordingly:

- `partner-<firstname>-<last-initial>.md`
- `principal-<firstname>-<last-initial>.md`
- `xo-review-style.md` (XO-specific review dynamics)

Or archetypes specific to BCG's internal culture:

- `mcg-partner-strategy.md` (Marketing, Sales & Pricing practice)
- `bcg-x-ds-reviewer.md` (BCG X data-science reviewer norms)
- `partner-pitch-reviewer.md` (pitch-deck-specific review bar)

If the archetype is firm-generic (any consulting partner), it belongs in
`.agent/personas/`, not here.

## Git behavior

`.gitignore` in this directory tracks **only** `README.md` and
`_template.md`. Every `*.md` with an actual persona is ignored, same
pattern as `.agent/memory/client/` — track the shape, never the content.

To add a new persona:

1. Copy `_template.md` to `<new-name>.md`.
2. Fill it in. File is local-only; will not appear in `git status`.
3. Reference it from the `reviewer` subagent's dispatch when that
   reviewer's audience matches.

## Status

Scaffold as of Step 8.0 (2026-04-24). Real personas populate during Phase
2 case work when specific review dynamics surface.
