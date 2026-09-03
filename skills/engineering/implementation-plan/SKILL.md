---
name: implementation-plan
description: Use after a design or requirement is clear but before coding. Turns a feature, bug fix, refactor, or technical change into a concrete implementation plan: files to inspect or edit, ordered steps, risks, tests, rollout/rollback notes, and stopping points. Use when the user asks for an implementation plan, execution plan, coding plan, task breakdown, or says to plan before implementing.
---

# Implementation Plan

Turn an approved idea into a practical coding plan. The plan should reduce ambiguity before edits begin, not become a second design doc.

## When To Use

Use this when:
- The user has approved a design or described a clear coding goal
- The change touches multiple files, modules, APIs, data flow, tests, migrations, or user-visible behavior
- The user asks to "make a plan", "break this down", "plan implementation", or "think before coding"

Do not use this for trivial edits where the implementation is obvious and the user asked for direct action. For those, state the intended change briefly and proceed.

When the plan is approved and coding begins, use the `surgical-implementation` skill to keep the actual diff scoped, assumption-aware, and verified.

## Workflow

1. **Read context first**
   - Check README/docs, package scripts, existing tests, nearby code, and recent relevant commits when available.
   - Search for existing helpers, patterns, feature flags, data models, routes, and tests before proposing new structures.

2. **Restate the goal**
   - Write the smallest clear statement of what will change.
   - Name what is intentionally out of scope.

3. **Map the current system**
   - Identify existing code that already solves part of the problem.
   - Identify ownership boundaries: UI, API, service, storage, background jobs, config, tests.

4. **List the edit surface**
   - Name files/modules likely to be changed.
   - Distinguish confirmed edits from files that only need inspection.

5. **Plan ordered steps**
   - Put dependency work first.
   - Keep structural changes separate from behavior changes when possible.
   - Prefer the smallest diff that cleanly expresses the change.
   - Make each task an independently reviewable, testable outcome rather than a bucket of unrelated setup work.
   - Record interfaces produced for later tasks and dependencies consumed from earlier tasks when multiple implementers could execute the plan.

6. **Risk review**
   - Call out data loss, security, concurrency, migration, compatibility, performance, and UX risks.
   - If the plan touches more than 8 files or introduces more than 2 new abstractions, challenge the scope and propose a smaller path.

7. **Verification plan**
   - List exact commands/tests to run.
   - Include manual QA steps for user-facing behavior.
   - Add regression tests for bug fixes and edge cases.

8. **Self-review the written plan**
   - Check every spec requirement maps to a task.
   - Search for placeholders such as `TBD`, `TODO`, “handle edge cases”, or “add tests” without concrete detail.
   - Verify paths, interfaces, types, and names are consistent between tasks.
   - For high-risk plans, use [references/plan-document-reviewer-prompt.md](references/plan-document-reviewer-prompt.md) when an independent plan review is authorized.

9. **Proceed or pause**
   - If the user asked only for a plan, stop after the plan.
   - If the user asked you to implement and there are no unresolved decisions, proceed after presenting the plan.
   - If key decisions remain, ask one focused question before coding.

## Output Format

Use this structure:

```markdown
## Goal

## Out Of Scope

## Current System Notes

## Edit Surface
- Confirmed edits:
- Inspect only:

## Implementation Steps
1. ...

## Risks And Mitigations
- ...

## Verification
- Automated:
- Manual:

## Open Questions
- None / ...
```

## Quality Bar

- Reuse existing patterns before inventing new ones.
- Avoid broad refactors unless they are required for the change.
- Include tests proportional to risk.
- Make rollback obvious for migrations, config changes, and releases.
- Do not hide uncertainty. Mark uncertain files/steps as "inspect first".

## Verification

- [ ] Every requirement has an implementation and verification step.
- [ ] Task boundaries are independently testable and ordered by dependency.
- [ ] Paths, interfaces, and names are internally consistent.
- [ ] No vague placeholders remain.
- [ ] Risks, rollout/rollback, and open decisions are explicit.
