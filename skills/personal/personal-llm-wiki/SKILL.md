---
name: personal-llm-wiki
description: Consult and maintain the user's personal LLM wiki at `/Users/wronsky/Documents/Agent技能`. Use when the user asks to use their personal wiki, long-term memory, knowledge base, Obsidian-style wiki, ingest sources into the wiki, preserve or沉淀 durable insights, answer from the wiki, link another project to the wiki, or lint/health-check the wiki.
---

# Personal LLM Wiki

## Overview

Use this skill to connect current work to the user's long-term markdown wiki.
The wiki root is `/Users/wronsky/Documents/Agent技能`.

## Quick Start

Run `scripts/wiki_status.py` when you need a compact map of the wiki paths,
recent log entries, and index headings.

Always read these files before writing wiki updates:

- `/Users/wronsky/Documents/Agent技能/AGENTS.md`
- `/Users/wronsky/Documents/Agent技能/wiki/index.md`

Treat `/Users/wronsky/Documents/Agent技能/raw/` as source material and
`/Users/wronsky/Documents/Agent技能/wiki/` as the maintained knowledge layer.

## Decision Rules

- If the user asks to consult, use, or answer from the wiki: read `wiki/index.md`,
  then open the relevant pages before answering.
- If the user asks to ingest a source: read the source, create or update a source
  page, update related pages, update `wiki/index.md`, and append `wiki/log.md`.
- If the user asks to preserve, file, remember, or沉淀 something: create or update
  a durable page under `wiki/questions/`, `wiki/concepts/`, or `wiki/syntheses/`.
- If working from another project: read from the wiki when relevant, but write to
  the wiki only when the user explicitly asks to preserve or ingest something.
- If the user asks for lint, health check, cleanup, or consistency review: inspect
  links, stale claims, orphan pages, missing source support, and underdeveloped
  concepts.

## Write Workflow

When changing the wiki:

1. Read `AGENTS.md` and `wiki/index.md`.
2. Inspect existing pages that might overlap with the new information.
3. Prefer updating an existing page over creating a near-duplicate.
4. Use Obsidian-style links such as `[[concepts/llm-maintained-wiki]]`.
5. Add or update YAML frontmatter with `created`, `updated`, `status`, and
   `sources` when useful.
6. Update `wiki/index.md` for any created page or meaningful page change.
7. Append a dated entry to `wiki/log.md`.
8. Summarize the changed files and any open questions.

## Page Placement

- `wiki/sources/`: one page per ingested source.
- `wiki/entities/`: people, organizations, projects, products, places, and named
  objects.
- `wiki/concepts/`: reusable ideas, frameworks, terms, and themes.
- `wiki/questions/`: durable answers from conversations.
- `wiki/syntheses/`: higher-level analysis, comparisons, maps, and evolving
  theses.

## Safety

Do not rewrite files under `raw/` unless the user explicitly asks. Do not add
private project details to the personal wiki unless the user asks to preserve
them there. Preserve uncertainty and source support instead of making claims
look more settled than they are.
