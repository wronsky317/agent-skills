---
name: surgical-implementation
description: Use frequently when implementing, fixing, or refactoring code after the goal is reasonably clear. Enforces explicit assumptions, minimal diffs, existing patterns, scoped edits, success criteria, and verification. Use for coding changes where overengineering, hidden assumptions, or unrelated edits are risks.
---

# Surgical Implementation

Implement code changes with a small, intentional diff. The goal is to solve the requested problem without inventing extra scope, changing unrelated behavior, or hiding uncertainty.

## When To Use

Use this for ordinary coding work, including:
- Implementing a requested feature or behavior change
- Fixing a bug when the root cause is already known
- Refactoring code after the desired end state is clear
- Editing generated code before it lands
- Tightening an implementation after a plan has been approved

Prefer adjacent skills when the task is not yet ready for implementation:
- Use `investigate` first when the failure mode or root cause is unclear.
- Use `implementation-plan` first when the design, edit surface, or rollout risk is unclear.
- Use `code-review` after changes when the user asks for review or pre-merge risk assessment.
- Use `qa` after implementation when user-visible behavior needs acceptance testing.

## Workflow

1. **Restate the goal**
   - Say what will change in one sentence.
   - Name anything intentionally out of scope.
   - If there are multiple plausible interpretations, ask one focused question before editing.

2. **Expose assumptions**
   - State assumptions that affect API shape, data model, permissions, behavior, or tests.
   - Push back if a simpler implementation would satisfy the same goal.
   - Stop if the request requires guessing about product behavior, safety, or data ownership.

3. **Find existing patterns**
   - Search nearby code, tests, docs, helpers, and recent conventions before creating new structure.
   - Reuse local APIs and style even when a different pattern would be personally preferable.
   - Add a new abstraction only when it removes real duplication or matches an established local pattern.

4. **Define success criteria**
   - For a bug: identify the repro and the regression signal.
   - For a feature: identify the user-visible behavior and nearest automated check.
   - For a refactor: identify the invariant that must remain unchanged.

5. **Edit narrowly**
   - Change only files required by the goal.
   - Do not perform drive-by cleanup, formatting, comment rewrites, dependency changes, or broad refactors.
   - Remove only unused imports, variables, functions, or files made obsolete by your own change.
   - If the diff expands beyond the expected edit surface, pause and explain why.

6. **Verify**
   - Run the smallest relevant test first, then broader checks proportional to risk.
   - Inspect the diff before reporting completion.
   - Report any important path that could not be tested.

## Lightweight Mode

For trivial edits, keep the workflow compact:

```markdown
Goal: ...
Edit: ...
Verify: ...
```

Still avoid unrelated changes.

## Stop Conditions

Pause before editing when:
- The requested behavior is ambiguous in a way that affects the implementation.
- A safer or much simpler approach conflicts with the requested approach.
- The change would require broad rewrites, migrations, permissions changes, or irreversible data changes.
- The target files contain user changes that materially conflict with the requested edit.

## Verification

Before finishing, confirm:

- [ ] The final diff maps directly to the request.
- [ ] Assumptions and tradeoffs were surfaced when they mattered.
- [ ] Existing project patterns were reused where available.
- [ ] The nearest relevant verification was run, or the untested risk is stated.
- [ ] No unrelated cleanup or pre-existing dead code was removed.

## Reference

For the source inspiration and the distilled principle mapping, read [references/karpathy-principles.md](references/karpathy-principles.md) only when attribution or deeper rationale is useful.
