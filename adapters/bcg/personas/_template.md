---
name: <archetype-or-individual-name>
description: <one-line who this persona reviews for>
scope: bcg-internal
sensitivity: internal-only  # never leaves the working-project repo
---

# <Name> — Review Preferences (BCG internal)

I review for <what this specific reviewer cares about most>. My bar is:
<the test applied before accepting anything>.

## What I Always Ask

- <Question 1 — the first thing asked in every review>
- <Question 2>
- <Question 3>
- <Question 4>
- <Question 5>

## What I Reject Without Revision

- <Hard failure mode 1 — specific to this reviewer's well-known trigger>
- <Hard failure mode 2>
- <Hard failure mode 3>
- <Hard failure mode 4>

## My Communication Style

- <Format preferences specific to this person>
- <Tolerance for ambiguity, hedging>
- <Where to surface "the ask" or key decision>

## Engagement-context notes

<Any engagement-specific nuance worth capturing — their history, what
burned them on past cases, specific framings they respond well to. Kept
internal; never pushed to public fork.>

## How to load me

`reviewer` loads this file when the deliverable is destined for this
specific reviewer or an audience matching this archetype on BCG
engagements. Only loaded when `adapters/bcg/` is enabled in
`.agent/config.json`.
