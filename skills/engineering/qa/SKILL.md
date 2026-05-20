---
name: qa
description: Use after implementation to verify behavior from the user's perspective. Applies to web UI, CLI tools, APIs, workflows, and integrations. Creates a test plan, runs realistic checks, records bugs with reproduction steps and evidence, fixes only when asked or when the task includes fixing, then re-verifies.
---

# QA

Validate that the work actually behaves correctly for a user or caller. QA is not just "tests pass"; it checks the intended workflow end to end.

## When To Use

Use this when:
- The user asks to QA, test, verify, dogfood, smoke test, check if it works, or validate a feature
- A feature implementation is complete and needs acceptance testing
- A fix needs reproduction and re-verification
- A frontend, CLI, API, integration, or generated artifact has user-visible behavior

Use report-only mode unless the user asked you to fix issues too.

When QA finds an issue and the user wants it fixed, use the `surgical-implementation` skill for the code change, then return to QA to re-verify the same path.

## Workflow

1. **Define scope**
   - Identify the target: URL, command, API endpoint, file, workflow, or feature.
   - Identify mode: report-only or test-and-fix.
   - Identify auth/data needs and any unsafe actions to avoid.

2. **Create a test matrix**
   - Happy path
   - Empty/loading/error states
   - Permission/auth boundaries
   - Invalid input
   - Regression path for the changed behavior
   - Responsive/browser/device checks for UI work

3. **Prepare environment**
   - Start or identify the dev server if needed.
   - Run build/typecheck/unit tests when relevant.
   - For web UI, use browser tooling if available; otherwise document manual checks clearly.

4. **Execute realistic checks**
   - Follow user-visible steps, not only internal function calls.
   - Capture evidence: command output, screenshots, response bodies, console errors, logs, or exact repro steps.
   - Record expected vs actual behavior.

5. **Triage**
   - Critical: blocks core workflow, data loss, security/privacy, crash
   - High: common workflow broken or misleading
   - Medium: edge case or degraded experience
   - Low: cosmetic or minor polish

6. **Fix loop, only if in test-and-fix mode**
   - Fix one issue at a time.
   - Keep each fix minimal and tied to the repro.
   - Add regression coverage when practical.
   - Re-run the specific repro and relevant automated tests.

7. **Final report**
   - State pass/fail for each tested path.
   - Include unresolved issues and residual risk.
   - Include exact verification commands.

## Prove-It Pattern

Use this pattern for bug fixes and regression verification:

1. Reproduce the issue before trusting the fix.
2. Capture the failing evidence: command, input, request, screenshot, log, or exact user steps.
3. Apply or inspect the fix.
4. Re-run the same repro and show it now passes.
5. Run the nearest relevant regression check.

If the original failure cannot be reproduced, say so and lower confidence. Do not mark the bug fixed only because the code looks plausible.

## Output Format

```markdown
## QA Scope

## Test Matrix
- [ ] ...

## Results
- PASS/FAIL - path tested - evidence

## Issues
- [High] Title
  Repro:
  Expected:
  Actual:
  Evidence:
  Suggested fix:

## Fixes Applied
- None / ...

## Verification Commands
- ...

## Ship Readiness
Ready / Not ready / Ready with caveats
```

## Quality Bar

- Always test the primary user path.
- For UI, check console errors and at least one narrow/mobile viewport when possible.
- For CLI/API, check success and failure exits/statuses.
- Never mark ready if the core path was not actually exercised.
- Do not hide environmental blockers; report them as blockers with the next required action.

## Verification

Before reporting QA complete, confirm:

- [ ] The primary user or caller path was exercised.
- [ ] Evidence was captured for each PASS/FAIL result.
- [ ] At least one failure or edge path was checked when applicable.
- [ ] Bugs include repro steps, expected behavior, actual behavior, and evidence.
- [ ] Any untested important path is listed as residual risk.
