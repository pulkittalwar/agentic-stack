# Personal Preferences

> **This file is yours.** It's the one file every new user should customize.
> Preferences are context, not procedure — tell the agent who you are, not
> how to write code.

## Code style

### Python (primary language)
- **Type hints:** always. Treat `mypy --strict` errors as bugs to fix, not warnings to silence.
- **Formatter + linter:** `ruff` (both format and lint). No `black`.
- **DataFrames:** pandas for small/medium, polars when performance matters, PySpark for big data. When data size is unclear, inspect shape/row-count first and pick based on findings — don't default blindly.
- **Docstrings:** Google style (`Args:` / `Returns:` / `Raises:` blocks). Renders cleanly in mkdocs, parses well for LLMs.
- **F-strings:** use where they keep log lines and messages readable and parameterized. Avoid string concatenation.
- **Validation boundaries:** Pydantic v2 for anything crossing an I/O edge (API payloads, config files, LLM structured outputs, CLI args). Plain `@dataclass` for internal domain objects where validation is wasted cycles.

### TypeScript / frontend (rarely touched — agent applies sane defaults)
- `tsconfig` strict mode on.
- React: function components + hooks only. No class components.
- Edge functions: target Supabase Edge Functions or Cloudflare Workers, not Vercel.

### SQL
- Uppercase keywords (`SELECT`, `FROM`, `WHERE`, `JOIN`).
- Prefer CTEs (`WITH foo AS (...)`) over nested subqueries for readability.

## Workflow

- **Artifact cadence:** during iterative drafting + approval work, write to disk on each approval; commit+push at logical milestones. Default to per-approval commits once the user has established the flow in a session. _(See auto-memory: `artifact-and-git-cadence`.)_
- **Commit style:** HEREDOC body + `Co-Authored-By` footer; match the repo's existing prefix (`docs:`, `chore:`, `feat:`, `fix:`).
- **Style conflicts:** match the file's existing convention over linter preferences when the two disagree.
- **Tests:** TDD where feasible — write the test, watch it fail, make it pass.
- **Missing-test policy:** a missing test is a deferred PR comment, not a merge blocker. Ship and log the gap rather than holding the change.
- **Branching:** branch-per-feature on personal projects; merge to `master`/`main` once the feature works. Direct commits to trunk only for docs, memory updates, or scaffold-level work.
- **Deployment:** no standing host preference. When deploy becomes relevant, agent proposes options (Railway, Fly, Cloudflare, VPS, etc.) weighing client constraints and project shape before picking.

## Constraints

### Primary stack
- **Languages:** Python (primary), SQL (frequent). Rarely TypeScript.
- **Database/backend default:** Supabase for personal projects unless a client dictates otherwise.
- **Big-data fallback:** PySpark, but only after an agent has inspected the data and confirmed pandas/polars can't handle it.

### BCG-specific invariants
- **Client data + LLMs:** client data may be pasted into BCG-approved enterprise LLMs. The enterprise agreement prohibits training on inputs, so paste is safe within that boundary. Never paste into consumer or free-tier LLMs.
- **GenAI policy:** no BCG-wide policy currently overrides these defaults. Revisit if policy changes.
- **Client overrides:** when on a client engagement, client-specific constraints (infrastructure, tooling, branching, security) take precedence over every default in this file. On ambiguous cases, ask first.

## Communication

- Direct, terse. Skip pleasantries.
- No trailing summaries of what was just done — the diff is sufficient.
- Surface tradeoffs explicitly; don't hide them behind a single recommendation.
- Socratic / teaching mode welcome when the goal is mental-model building (not when executing). Concrete examples beat abstract principles.
