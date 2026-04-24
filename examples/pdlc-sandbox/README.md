# pdlc-sandbox

Throwaway install target for verifying the `agentic-stack` → `claude-code`
adapter end-to-end. Not for real work.

## Purpose

After any non-trivial change to `.agent/`, the `adapters/claude-code/`
payload, or `install.sh`, run:

```bash
./install.sh claude-code examples/pdlc-sandbox --yes
```

from the fork root. This populates `examples/pdlc-sandbox/` with a fresh
copy of the brain (`.agent/`), the Claude Code adapter payload (`CLAUDE.md`
+ `.claude/settings.json` + `.claude/agents/`), and runs the onboarding
wizard. Inspect the result, smoke-test by dispatching the PDLC→SDLC
pipeline against a trivial task, then discard the install artifacts.

## What's tracked vs. ignored

- **Tracked in git:** this `README.md` only — documents intent.
- **Gitignored:** `.agent/`, `.claude/`, `CLAUDE.md`, `memory/`, and any
  other install artifacts. These regenerate on every `./install.sh`;
  tracking them would make the sandbox drift from the fork's source of
  truth.

See `examples/pdlc-sandbox/.gitignore` for the exact exclusions.

## Not the "real working project"

Real BCG case-team work lives in a separate install target (e.g.
`~/code/case-agent/`), not here. This directory exists **only** to verify
that `install.sh` produces a working brain on a clean slate. Real-world
testing happens in the dedicated working project after Step 8.2.
