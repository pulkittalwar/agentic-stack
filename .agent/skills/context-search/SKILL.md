---
name: context-search
version: 2026-04-24
bootstrapped_from: "harness-starter-kit (Kenneth Leung, BCG) — 2026-04-24 import, Step 8.1"
description: Use before any analysis or drafting to retrieve relevant context from the project knowledge base — client facts, decisions, constraints, transcripts, frameworks, glossary. Distinct from memory recall — this skill searches structured project context, not episodic/semantic agent memory. Always cite sources and flag gaps explicitly. Path conventions below reference starter-kit layout and will be adapted to agent-stack paths in Step 8.2.
triggers: ["find context on", "search context", "what do we know about", "pull the background", "what's in the project data"]
tools: [bash]
preconditions: ["context directory exists for the engagement"]
constraints:
  - context is read-only — never modify context files
  - prefer specific citations over paraphrases
  - flag gaps as [CONTEXT GAP: <what is missing>]
  - surface contradictions rather than picking one version silently
category: knowledge-work
---

# Context Search Skill

Use this skill to retrieve relevant context from the project's knowledge base before performing analysis or drafting.

## Search Protocol

### Step 1: Identify What You Need
Before searching, list:
- What specific information is required?
- What would change your analysis if it were different?
- Is this global context or case-specific?

### Step 2: Search Locations

| Information Type | Where to Look |
|---|---|
| Engagement background, client facts | `context/projects/{project}/background/` |
| Data and analysis inputs | `context/projects/{project}/data/` |
| Decisions already made | `context/projects/{project}/decisions/` |
| Constraints and boundaries | `context/projects/{project}/constraints/` |
| Transcripts and interviews | `context/projects/{project}/transcripts/` |
| BCG frameworks and templates | `context/account/frameworks/` |
| Consulting glossary | `context/account/glossary/` |
| Engagement process norms | `context/account/case-engagement-process.md` |
| Team roster and assignments | Confluence — use `confluence-access` skill protocol |
| Action items and RAID log | Confluence — use `confluence-access` skill protocol |

### Step 3: Cite What You Find
Always cite:
- Source file or Confluence page
- Section heading if applicable
- Date of the content if time-sensitive

### Step 4: Flag Gaps
If required context is not found:
- Note explicitly: [CONTEXT GAP: <what is missing>]
- Propose what alternative data could substitute, or what assumption to make

## Rules
- Context is read-only — never modify context files
- Prefer specific citations over paraphrases
- If context is contradictory, flag both versions and ask for clarification
