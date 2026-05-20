# Skill Anatomy

Use this reference when creating or substantially rewriting a skill.

## Required Files

Every skill needs:

```text
skill-name/
  SKILL.md
```

Optional resources:

```text
skill-name/
  references/   # Detailed docs loaded only when needed
  scripts/      # Deterministic reusable helpers
  assets/       # Templates, fonts, images, boilerplate, fixtures
  agents/       # UI metadata when supported by the runtime
```

Do not add empty optional directories.

## Frontmatter

Use at least:

```yaml
---
name: skill-name
description: Does the task. Use when the user asks for concrete trigger contexts.
---
```

Rules:

- `name` is lowercase hyphen-case and matches the folder name.
- `description` is the primary trigger surface.
- `description` includes both capability and when-to-use language.
- Keep `description` under 1024 characters.
- Avoid process summaries in `description`; put process in the body.

## Recommended Body Shape

```markdown
# Skill Title

## Overview
One short paragraph explaining the purpose and boundary.

## Workflow
Numbered steps the agent follows.

## Decision Rules
When to choose one path over another.

## Resources
References or scripts and when to load or execute them.

## Verification
Checklist of evidence required before reporting success.
```

Equivalent headings are fine if they serve the same purpose.

## Progressive Disclosure

Keep `SKILL.md` small and operational.

Move these into `references/`:

- Long examples
- Detailed checklists
- Style guides
- Domain schemas
- Platform-specific variants

Move these into `scripts/`:

- Repeated parsing, validation, conversion, or scaffolding code
- Operations that should behave deterministically
- Logic that would otherwise be rewritten often

## Quality Review

Before finalizing, ask:

- Would the skill trigger from the description alone?
- Can another agent follow the workflow without guessing?
- Is there a clear stop condition?
- Is verification evidence named explicitly?
- Is this new skill meaningfully different from existing skills?
- Did we avoid copying large reference material into the body?
