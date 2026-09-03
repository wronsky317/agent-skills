---
name: verification-before-completion
description: Requires fresh command or artifact evidence before claiming that work is complete, fixed, passing, or ready. Use immediately before success claims, commits, pull requests, releases, task completion, or handoff when the current work changed code, configuration, documents, or generated artifacts.
---

# Verification Before Completion

Evidence must describe the current artifact, not an earlier version or an agent's unverified report.

## Workflow

1. **Identify the claim**
   - Translate “done”, “fixed”, “passes”, “ready”, or “looks correct” into an observable condition.

2. **Choose direct evidence**
   - Code: focused test plus broader checks proportional to risk.
   - Build/config: parser, compiler, linter, dry run, or documented validation command.
   - Documents/media: render and visually inspect the final artifact.
   - Delegated work: inspect the actual diff/files and rerun the relevant check.

3. **Run verification fresh**
   - Execute against the exact current tree/artifact.
   - Capture exit status and the meaningful summary; do not infer success from partial output.

4. **Inspect scope**
   - Review status/diff or artifact inventory for missing, unrelated, temporary, secret, or generated files.
   - Confirm the requested acceptance criteria, not merely tool success.

5. **State the result precisely**
   - Say what passed and cite the evidence.
   - If a check could not run, say what is unverified and why.
   - If verification fails, report the failure and continue investigation or ask for direction; do not use completion language.

## Evidence Rules

- A prior run proves only the prior state.
- “The subagent said it passed” is a lead, not evidence.
- A linter does not prove runtime behavior; a unit test does not prove visual layout.
- Warnings must be explained or reported, not silently treated as clean.

## Verification

- [ ] The evidence was generated after the last relevant edit.
- [ ] It tested the exact claim being made.
- [ ] Exit status/output or visual inspection was checked directly.
- [ ] The final scope/diff was inspected.
- [ ] Residual risk is explicit and success language matches the evidence.
