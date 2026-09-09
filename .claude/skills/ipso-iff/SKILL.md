---
name: ipso-iff
description: Investigate a piece of news for information manipulation. Runs a pipeline — detective (evidence gathering) → court (attorney/prosecutor) → judge (final verdict) → annotator (Master Dataset JSON) — and returns a Detective Report plus a decisive, non-technical verdict. Use when the user asks to investigate, fact-check, or check a news item/article/post for manipulation or disinformation.
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
`ipso-analyst`, `ipso-source`; then `ipso-attorney`, `ipso-prosecutor`, `ipso-judge`; then
`ipso-annotator`). Every one of these agents **must** write its own report to that folder as
a file (see each agent's own spec for its exact filename) in addition to returning the
report inline to its caller.

## Step 2 — Detective phase

Dispatch the `ipso-detective-head` sub-agent with the normalized Piece of News (text
required; title/url/date passed through if present), **the enabled actor configs** from
Step 1.5, and **the session folder path** from Step 1.6. Wait for it to return the Detective
Report (Markdown, see `.claude/agents/ipso-detective-head.md` for its exact shape).

If this dispatch fails outright, stop and tell the user the investigation could not
proceed past the evidence-gathering phase — do not fabricate a Detective Report yourself.

## Step 3 — Court phase (parallel)

Dispatch `ipso-attorney` and `ipso-prosecutor` independently — each gets the Piece of News,
the Detective Report from Step 2, and the session folder path from Step 1.6. They do not see
each other's output and do not need to run in strict lock-step; just ensure both complete
before Step 4. Collect both Court Reports.

If one of the two fails, proceed to Step 4 with whichever report succeeded plus a note that
the other side's argument could not be produced — do not block the whole investigation on
a single court-phase failure.

## Step 4 — Judge phase

Dispatch `ipso-judge` with: the Piece of News, the Detective Report, both Court Reports
(or the one that succeeded, per the fallback above), and the session folder path from
Step 1.6. Wait for the Final Verdict Report (exactly one of "Manipulation present." /
"Manipulation not established." plus a standalone conclusion).

## Step 5 — Annotator phase

Dispatch `ipso-annotator` with: `news_id` (the `session_id` from Step 1.6), `full_text`
(the normalized news text from Step 1), `url`/`source`/`date` from Step 1 if present, the
Detective Report from Step 2, and the session folder path from Step 1.6. Wait for it to
return the Master Dataset JSON row(s) for this news item (see
`.claude/agents/ipso-annotator.md` for the exact schema and shape).

If this dispatch fails outright, do not fail the whole investigation — proceed to Step 6
anyway; the verdict and detective report are still valid without the dataset JSON.

## Step 6 — Respond to the user

Return, in this order, and nothing else besides these two sections:

```markdown
## Verdict

<the judge's verdict and conclusion, verbatim>

## Detective Report

<the full detective report from Step 2, verbatim>
```

Do not additionally print the raw Attorney/Prosecutor reports or the dataset JSON as
top-level output — they are working evidence and a machine-readable artifact, not a
separate user-facing deliverable. Do not mention `ipso-detective-head`, `ipso-reader`,
`ipso-analyst`, `ipso-source`, `ipso-attorney`, `ipso-prosecutor`, `ipso-judge`,
`ipso-annotator`, or this skill's own name anywhere in the response text you add around
those two sections.
