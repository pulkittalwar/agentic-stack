---
description: Safety rules for all Atlassian operations (Confluence and Jira)
globs: "*"
---

# Atlassian Safety Rules

Read `config.yaml` for Confluence space key, space ID, Jira project key, and site URLs.

## IP Allowlist Workaround

The Atlassian org enforces an IP allowlist that **blocks all REST API v2/v1 endpoints** from environments not on the list. This includes `getConfluenceSpaces`, `getPagesInConfluenceSpace`, `getConfluencePage`, `searchConfluenceUsingCql` (CQL), `searchJiraIssuesUsingJql` (JQL), `createConfluencePage`, and `updateConfluencePage`.

**Two tools bypass the IP allowlist** (they use Atlassian Graph Gateway, not REST API):

| Tool | Use For | Key Rule |
|---|---|---|
| `searchAtlassian` (Rovo Search) | Discovering pages, searching content | Do NOT pass `cloudId` — it is auto-derived from token |
| `fetchAtlassian` (ARI Fetch) | Reading full page content | Do NOT pass `cloudId` — it is extracted from the ARI |

**Default behavior:** Always try `searchAtlassian` + `fetchAtlassian` first. Only fall back to REST API tools if those fail (which would indicate Rovo is down, not an IP issue).

See `.claude/skills/confluence-access/SKILL.md` for the full access protocol.

## Confluence API ID Rules (for REST API fallback only)

These rules apply when the IP allowlist is lifted or when running from an allowlisted network:

- **`cloudId`** — Always use the `site_url` value (e.g. `bcgx.atlassian.net`). Never use a UUID unless explicitly provided.
- **`spaceId`** — Always use the **numeric** `space_id` from `config.yaml` (e.g. `2938077250`). Do NOT pass the text `space_key` (e.g. `BCTAH`) — the API expects a long integer and will reject string keys.
- **`pageId`** — Always a numeric string. The homepage ID is stored as `homepage_id` in `config.yaml`.

### Auto-Resolve Missing IDs

Before any Confluence operation, read `config.yaml`. If `space_id` or `homepage_id` are missing but `space_key` and `site_url` are present, resolve them automatically:

1. Use `searchAtlassian` to find pages in the space and extract `cloudId` from result metadata
2. If REST API is accessible, call `getConfluenceSpaces` with `cloudId: <site_url>` and `keys: <space_key>`
3. Extract `id` → `space_id` and `homepageId` → `homepage_id` from the response
4. Write them back to `config.yaml` under the `confluence:` section (preserving existing fields)
5. Confirm to the user what was resolved

## Scope

- **Configured space/project only.** Confluence ops scoped to the configured `space_key` / `space_id`. Jira ops scoped to the configured `project_key`. Never touch other spaces or projects.
- If a user provides a URL outside the configured scope, confirm before proceeding.

## Read/Write

- **Read before write.** Fetch current state before any update. Never write blind.
- **Merge, don't overwrite.** Add to existing content. Never replace an entire page body or issue description.
- **Preserve structure.** Keep existing headings, tables, formatting. Add rows — don't rebuild tables.

## Failure Handling

- **No auto-retry.** If an API call fails, report the error and ask the user.
- **No bulk deletes.** Never remove multiple entries without explicit per-item confirmation.

## Audit

- **Log operations.** After batch updates, summarize what changed and where.

## Practical Tips

- **Use `searchAtlassian` + `fetchAtlassian` as the primary access path** — they bypass the IP allowlist
- Rovo Search has indexing lag on newly created pages (hours/days). If a page is not found, construct the ARI manually: `ari:cloud:confluence:<cloudId>:page/<pageId>`
- The `cloudId` UUID is available in the `metadata.cloudId` field of any Rovo Search result
- Numeric `space_id` is not in the Confluence UI — use `getConfluenceSpaces` API with space key to retrieve it (when on allowlisted IP); store in `config.yaml`
- When MCP tool results are saved to file due to size, parse as JSON immediately — don't guess formats with grep/regex
- During sync, always create local files for Confluence pages even if page content is empty
- `scripts/sync-confluence.py` uses REST API directly and **requires an allowlisted IP or VPN**. When blocked, use the MCP-based fallback in the sync-harness command instead.
