---
name: ipso-iff
description: Investigate a piece of news for information manipulation. Runs a pipeline — detective (evidence gathering) → annotator (Master Dataset JSON) — and returns a Detective Report with DISARM-tagged findings. Use when the user asks to investigate, fact-check, or check a news item/article/post for manipulation or disinformation.
argument-hint: "News text and/or URL to investigate (date optional)"
user-invocable: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding.

## What this skill does

Orchestrates a full information-manipulation investigation of a single piece of news
supplied above, in order, ending with a machine-readable Master Dataset JSON row per
excerpt. No database is involved anywhere in this flow — everything is scoped to this run,
written only to the session folder (`artifacts/<session_id>/`) as Markdown reports plus one
`dataset.json`.

## Step 1 — Normalize the input

From `$ARGUMENTS`, extract:
- `text` — the news content itself. **Required.** If the argument contains no analyzable
  news text and no URL you can treat as the subject, STOP here and respond only with:

  > No analyzable content was provided. Please include the news text and/or a URL to
  > investigate.

  Do not proceed to Step 2 in that case.
- `title` — if evident, otherwise omit.
- `url` — if provided, otherwise omit. Its absence never blocks the investigation.
- `date` — if provided, otherwise omit. Its absence never blocks the investigation.
- `source` — the channel/outlet name, if provided or self-evident (e.g. from the URL's
  domain), otherwise omit. Its absence never blocks the investigation.

## Step 1.5 — Load actor configs

Before dispatching to the detective phase, run `.claude/skills/ipso-iff/scripts/load_actors.py`
to load enabled actor configurations from `.env`. This produces a JSON object containing only
the enabled media sources (web_search, twitter, reddit, instagram, threads, telegram).
Pass this config dict to the detective agents when they start working.

## Step 1.6 — Generate session ID and session folder

Run `.claude/skills/ipso-iff/scripts/generate_session_id.py` to generate a fresh `session_id`
(one UUID per news investigated — one news, one session, never reused across runs, even for
re-investigations of the same news).

Create the folder `artifacts/<session_id>/` (relative to the project root). This is the
**session folder** for this run.

Pass the session folder path (e.g. `artifacts/<session_id>/`) to **every** agent dispatched
from this point on (`ipso-detective-head` and, transitively via it, `ipso-reader`,
`ipso-analyst`, `ipso-source`; then `ipso-annotator`). Every one of these agents **must**
write its own report to that folder as a file (see each agent's own spec for its exact
filename) in addition to returning the report inline to its caller.

## Step 2 — Detective phase

Dispatch the `ipso-detective-head` sub-agent with the normalized Piece of News (text
required; title/url/date passed through if present), **the enabled actor configs** from
Step 1.5, and **the session folder path** from Step 1.6. Wait for it to return the Detective
Report (Markdown, see `.claude/agents/ipso-detective-head.md` for its exact shape).

If this dispatch fails outright, stop and tell the user the investigation could not
proceed past the evidence-gathering phase — do not fabricate a Detective Report yourself.

## Step 3 — Annotator phase

Dispatch `ipso-annotator` with: `news_id` (the `session_id` from Step 1.6), `full_text`
(the normalized news text from Step 1), `url`/`source`/`date` from Step 1 if present, the
Detective Report from Step 2, and the session folder path from Step 1.6. Wait for it to
return the Master Dataset JSON row(s) for this news item (see
`.claude/agents/ipso-annotator.md` for the exact schema and shape).

If this dispatch fails outright, do not fail the whole investigation — proceed to Step 4
anyway; the detective report is still valid without the dataset JSON.

## Step 4 — Respond to the user

Return, in this order, and nothing else besides this section:

```markdown
## Detective Report

<the full detective report from Step 2, verbatim>
```

Do not additionally print the raw dataset JSON as top-level output — it is a
machine-readable artifact, not a separate user-facing deliverable (point the user to
`artifacts/<session_id>/dataset.json` if they need it directly). Do not mention
`ipso-detective-head`, `ipso-reader`, `ipso-analyst`, `ipso-source`, `ipso-annotator`, or
this skill's own name anywhere in the response text you add around that section.
