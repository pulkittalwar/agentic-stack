# Permissions

The pre_tool_call hook reads this file and enforces it before any tool
invocation. Humans edit this file; the agent does not.

## Always allowed (no approval)
- Read any file in the project directory.
- Run tests.
- Create branches.
- Write to `memory/` and `skills/` directories.
- Create draft pull requests.
- Read public HTTP APIs in the approved domains list.

## Requires approval
- Merge pull requests.
- Deploy to any environment (staging, production).
- Delete files outside of `memory/working/`.
- Install new dependencies or upgrade pinned versions.
- Modify CI/CD configuration.
- Run database migrations.

## Never allowed
- Force push to `main`, `production`, or `staging`.
- Access secrets or credentials directly (use env vars through the shell only).
- Send HTTP requests to domains not on the approved list.
- Modify `permissions.md` (only humans edit this file).
- Disable or bypass `pre_tool_call` hooks.
- Delete entries from episodic or semantic memory (archive, don't delete).

## Approved external domains
- `api.github.com`
- `registry.npmjs.org`
- `pypi.org`
- `api.anthropic.com`
- `api.openai.com`

## BCG engagement rules

These layer on top of the generic tiers above when working on BCG
engagements or in repositories handling client data. Remove or edit when
leaving BCG.

### Never allowed
- Push from a BCG-client repo (remote URL contains `client-`, `bcg-`, or a
  BCG-hosted git host) to a personal remote (e.g. `github.com/pulkittalwar/*`),
  or vice versa. If the correct remote is ambiguous, stop and ask.
- Write into `memory/client/<X>/` where `<X>` does not match the current
  active client. Active client resolves in this order: (1) `AGENT_CLIENT`
  env var, (2) nearest parent directory matching `client-*`, (3) first
  `memory/client/<X>/` path referenced in the session.

### Requires approval
- `git push` to any remote URL not seen previously in the current session.
  Prevents silent mistakes after `git remote add` or branch-tracking changes.
