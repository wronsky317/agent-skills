---
name: investigate
description: Use when debugging bugs, failing tests, errors, stack traces, regressions, unexpected behavior, flaky behavior, production incidents, or "why is this broken" requests. Requires root-cause investigation before fixes: reproduce, trace, form hypotheses, test evidence, then apply the smallest verified fix with regression coverage.
---

# Investigate

Debug systematically. Do not guess-fix. A fix without a confirmed root cause is just a new experiment hidden in the codebase.

## Iron Law

No implementation fix before root cause evidence.

You may add temporary logging, run commands, inspect code, and write small repro tests while investigating. Remove temporary instrumentation before finishing unless it is intentionally part of the fix.

After the root cause is confirmed and the fix is straightforward, use the `surgical-implementation` skill for the actual code change.

## Workflow

1. **Capture the symptom**
   - Restate what is failing.
   - Collect error messages, stack traces, failing test names, affected route/command, expected vs actual behavior.
   - If the report is too vague to reproduce, ask one focused question.

2. **Reproduce or narrow**
   - Run the failing test or command when possible.
   - If full reproduction is impossible, find the smallest observable signal: log line, stack frame, bad response, state mismatch, or code path.

3. **Trace the path**
   - Follow the data/control flow from symptom backward.
   - Search references and call sites.
   - Check recent changes to affected files.
   - Look for known bug families: null propagation, race, stale cache, config drift, time zone, serialization, permission mismatch, dependency/API change.

4. **Form hypotheses**
   - List up to 3 concrete hypotheses.
   - Each hypothesis must predict observable evidence.
   - Test the most likely hypothesis first.

5. **Confirm root cause**
   - Prove the cause with a failing test, targeted logging, debugger output, or code-path evidence.
   - If a hypothesis fails, record why and move to the next.
   - After 3 failed hypotheses, stop and report what was ruled out before continuing.

6. **Fix narrowly**
   - Apply the smallest change that addresses the root cause.
   - Avoid unrelated cleanup.
   - If the fix touches more than 5 files, pause and explain why the blast radius is necessary.

7. **Add regression coverage**
   - For bug fixes, add or update a test that fails without the fix and passes with it.
   - If a regression test is impossible, explain why and provide another verification signal.

8. **Verify**
   - Re-run the original reproduction.
   - Run relevant tests.
   - Check that no temporary instrumentation remains.

## Focused References

Load only the reference that matches the observed failure:

- [references/root-cause-tracing.md](references/root-cause-tracing.md) when the symptom is far from the original bad input or caller.
- [references/defense-in-depth.md](references/defense-in-depth.md) when invalid data crosses several trust or ownership boundaries.
- [references/condition-based-waiting.md](references/condition-based-waiting.md) for flaky asynchronous tests that rely on arbitrary sleeps; the companion implementation is [references/condition-based-waiting-example.ts](references/condition-based-waiting-example.ts).
- In npm projects, run `bash <investigate-skill-dir>/scripts/find-polluter.sh <artifact> <test-glob>` when a test creates persistent state and the polluting test is unknown. Resolve `<investigate-skill-dir>` from this `SKILL.md`.

When adding a regression test before the fix, use `test-driven-development`. Before making a success claim, use `verification-before-completion`.

## Output Format

Use this for the final report:

```markdown
## Debug Report

Symptom:

Root Cause:

Evidence:

Fix:

Regression Coverage:

Verification:

Residual Risk:
```

## Stop Conditions

Stop and ask before continuing when:
- The bug cannot be reproduced and there is no reliable signal to inspect
- 3 hypotheses have failed
- The fix requires a broad rewrite or touches unrelated modules
- The suspected root cause conflicts with the user's stated constraints

## Anti-Patterns

- "This should fix it" without verification
- Changing multiple layers before confirming which layer is broken
- Silencing an error instead of understanding why it occurred
- Adding retries for deterministic failures
- Treating flaky behavior as random before checking shared state, time, ordering, and isolation

## Verification

- [ ] The original symptom or a reliable proxy was reproduced.
- [ ] The root cause is supported by test, log, debugger, or code-path evidence.
- [ ] The fix targets the cause rather than suppressing the symptom.
- [ ] Regression coverage fails without the fix and passes with it when practical.
- [ ] The original reproduction and relevant surrounding checks pass after the fix.
