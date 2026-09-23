# ipso-iff-agentic-suite

Multi-agent Claude Code suite that investigates a single piece of news for information
manipulation / disinformation. Orchestrated by the `/ipso-iff` skill, a pipeline of
specialist sub-agents gathers evidence, argues both sides, and returns one decisive verdict.

## Requirements

- Claude Code CLI
- Any MCP tools you want the Analyst/Source specialists to use for tool-backed
  fact-checking and source lookup (e.g. web search, WebFetch) — configured in `.mcp.json`.
  Without them, those specialists fall back to text-only analysis.

## Setup

`.mcp.json` registers the MCP servers available to the agents (e.g. `searxng` for web
search). Add or swap servers there as needed — no other setup is required.

## Usage

Invoke the skill with the news you want investigated:

```
/ipso-iff <news text and/or URL, date optional>
```

Example:

```
/ipso-iff "https://example.com/some-article" published 2026-07-28
```

`$ARGUMENTS` just needs enough to identify the news: raw text, a URL, a title, or a
combination. If nothing analyzable is found, the skill stops and asks you for content
instead of guessing.

### What you get back

Exactly two sections, in this order:

```markdown
## Verdict
**Manipulation present.** / **Manipulation not established.**
<plain-language conclusion, ~250 words>

## Detective Report
<full evidence report: text analysis, detected manipulations, distribution
sources, related coverage, patterns, open evidence gaps>
```

Every agent's raw report is still saved to disk (see below).

## Pipeline

One investigation run = one **session**, one session ID, one output folder. The skill:

1. Normalizes your input (text/title/url/date).
2. Generates a fresh session ID (`.claude/skills/ipso-iff/scripts/generate_session_id.py`,
   a UUID4) and creates `artifacts/<session_id>/` — the session folder for this run only.
3. Runs three phases, passing the session folder to every agent so each one saves its own
   report there in addition to returning it to its caller:

```
                    ┌─────────────────┐
                    │ ipso-detective-  │
                    │      head        │
                    └───────┬─────────┘
                            │ dispatches
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ipso-reader   ipso-analyst   ipso-source
        (text only)  (MCP tools)    (MCP tools)
              └─────────────┴─────────────┘
                            │ merged into
                    Detective Report
```

- **Detective phase** (`ipso-detective-head`): dispatches three specialists in parallel —
  `ipso-reader` (surface-level rhetoric/wording signals, text only, no tools),
  `ipso-analyst` (fact-checking via whichever MCP tools are available), `ipso-source`
  (outlet/channel/syndicator discovery via whichever MCP tools are available) — then merges
  their findings into one Detective Report, using only facts the specialists actually
  returned.

## Session artifacts

Every agent writes its own report to the session folder, in addition to returning it to
whoever dispatched it:

```
artifacts/<session_id>/
├── reader_report.md       # ipso-reader
├── analyst_report.md      # ipso-analyst
├── source_report.md       # ipso-source
└── detective_report.md    # ipso-detective-head (merged)
```

One news item → one session → one folder. Re-investigating the same news later starts a
new session with a new UUID and a new folder — nothing is overwritten or reused across runs.
No database is involved anywhere in this flow; everything is scoped to the session folder.

## Repo layout

```
.claude/
├── agents/           # the 4 specialist agent specs (ipso-reader, ipso-analyst, ipso-source,
│                      #  ipso-detective-head)
└── skills/ipso-iff/
    ├── SKILL.md       # orchestration: normalize input → session → 3 phases → respond
    └── scripts/
        └── generate_session_id.py   # emits one UUID4 per run
artifacts/             # session output folders, one per investigation (gitignored)
.mcp.json               # MCP server registration (web search, etc.)
```
