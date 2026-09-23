---
name: ipso-iff
description: Investigate a piece of news for information manipulation. Runs a pipeline — detective (evidence gathering) → annotator (Master Dataset JSON) — writing all output to disk and returning only the dataset.json path, to keep the caller's context small. Use when the user asks to investigate, fact-check, or check a news item/article/post for manipulation or disinformation.
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

## Step 1.5 — Generate session ID and session folder

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
required; title/url/date passed through if present) and **the session folder path** from
Step 1.5. This agent writes the full Detective Report to `<session folder>/detective_report.md`
itself and returns you only a
short one-line confirmation — do **not** ask for or accept the full Markdown body inline;
if it comes back anyway, discard it from your working context and keep only the
confirmation line. You never need to hold the report's content yourself — Step 3's agent
reads the file directly.

If this dispatch fails outright, stop and tell the user the investigation could not
proceed past the evidence-gathering phase — do not fabricate a Detective Report yourself.

## Step 3 — Annotator phase

Dispatch `ipso-annotator` with: `news_id` (the `session_id` from Step 1.5), `full_text`
(the normalized news text from Step 1), `url`/`source`/`date` from Step 1 if present, and
the session folder path from Step 1.5. Do **not** paste the Detective Report's content into
this dispatch — the annotator reads `<session folder>/detective_report.md` itself. Wait for
it to confirm the Master Dataset JSON row(s) were written to
`<session folder>/dataset.json` (see `.claude/agents/ipso-annotator.md` for the schema).

If this dispatch fails outright, do not fail the whole investigation — proceed to Step 4
anyway; note that `dataset.json` was not produced.

## Step 4 — Respond to the user

Return **only** this, nothing else:

```markdown
Dataset written to `artifacts/<session_id>/dataset.json`.
```

(Or, if Step 3 failed: say plainly that the detective phase completed but the dataset JSON
could not be produced, and give the detective report's path instead.)

Do not print the Detective Report's Markdown body, the dataset JSON's contents, or any
per-excerpt findings as top-level output — this skill's only deliverable is the file path.
Do not mention `ipso-detective-head`, `ipso-reader`, `ipso-analyst`, `ipso-source`,
`ipso-annotator`, or this skill's own name anywhere in the response text.
