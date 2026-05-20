---
name: code-review
description: Use to review code changes, diffs, pull requests, or recent implementation work. Prioritizes correctness bugs, regressions, security/data risks, missing tests, edge cases, and maintainability issues. Use when the user asks for code review, PR review, diff review, review my changes, check this implementation, or before merging/landing code.
---

# Code Review

Review like a senior engineer protecting production. Findings come first. Style preferences and broad refactors are secondary unless they hide real risk.

## When To Use

Use this when:
- The user asks for a review of code, a diff, a branch, a PR, or an implementation
- Code was just generated and needs a second pass before merge
- The user asks "is this safe?", "anything wrong?", "check my changes", or "pre-merge review"

Do not use this for pure explanation requests unless the user asks for review.

When review findings need to be fixed, use the `surgical-implementation` skill for the follow-up edit so the fix stays narrow and verifiable.

## Review Order

1. **Understand the change**
   - Check `git status`, current branch, and the relevant diff.
   - Identify the intended behavior from the user request, plan, tests, docs, or commit messages.
   - Read code outside the diff when needed to verify call sites, enum handling, shared contracts, and existing patterns.

2. **Prioritize findings**
   - P0/P1: data loss, security issue, production outage, irreversible migration, broken core path
   - P2: likely bug, regression, race condition, compatibility break, missing critical test
   - P3: edge case, maintainability risk, confusing behavior, non-blocking test gap

3. **Check high-risk categories**
   - Incorrect assumptions about data shape, nullability, permissions, time zones, ordering, retries, idempotency
   - Race conditions and concurrent writes
   - API contract drift and unhandled enum/status values
   - Trust boundary violations: user input, LLM output, shell commands, SQL, file paths, external services
   - Missing rollback path for migrations or config changes
   - Tests that assert implementation details but miss behavior

4. **Verify before claiming**
   - If you say something is handled elsewhere, cite the file/line or test.
   - If you cannot verify coverage, say it is unverified.
   - Do not report vague concerns without a concrete failure mode.

5. **Suggest fixes**
   - For each finding, explain the minimal fix or the decision needed.
   - Do not make changes unless the user asked you to fix review findings.

## Five-Axis Pass

Use these axes as a coverage checklist, not as headings that must always appear:

1. **Correctness** - behavior matches the task, edge cases are handled, and tests prove the important paths.
2. **Readability** - names, control flow, and file organization are easy for the next maintainer to follow.
3. **Architecture** - boundaries, dependency direction, contracts, and abstractions fit the existing codebase.
4. **Security and data safety** - trust boundaries, secrets, permissions, migrations, and external calls are safe.
5. **Performance and operability** - no unbounded work, N+1 patterns, missing pagination, blocking calls, or invisible failure modes.

If an axis is irrelevant, skip it silently. If an axis cannot be verified but matters to the change, report that as residual risk.

## Output Format

Start with findings, ordered by severity:

```markdown
## Findings

- [P1] `path/file.ext:42` - Short title
  Why it matters, concrete failure scenario, and suggested fix.

- [P2] `path/file.ext:88` - Short title
  ...

## Test Gaps
- ...

## Open Questions
- ...

## Summary
Brief high-signal summary only after findings.
```

If there are no findings, say so clearly:

```markdown
## Findings

No blocking correctness issues found.

## Residual Risk
- ...
```

## Review Discipline

- Findings must be actionable and tied to specific code.
- Do not list style nits unless they can cause maintenance or behavior problems.
- Keep line ranges tight.
- Do not propose unrelated refactors.
- Be especially skeptical of generated code that "looks plausible" but lacks tests.

## Verification

Before finalizing a review, confirm:

- [ ] The intended behavior or task context was identified.
- [ ] Relevant tests were inspected before judging coverage.
- [ ] Each Critical/P1/P2 finding has a concrete failure mode.
- [ ] Each blocking finding includes a minimal fix or decision needed.
- [ ] Claims of safety are backed by file/line evidence, test evidence, or explicitly marked unverified.
