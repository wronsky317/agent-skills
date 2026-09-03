---
name: receiving-code-review
description: Evaluates incoming code-review feedback against the actual codebase before applying it, including clarification, technical pushback, prioritized fixes, and regression checks. Use when the user provides reviewer comments, PR feedback, requested changes, or asks to address review findings.
---

# Receiving Code Review

Treat feedback as a technical claim to understand and verify, not as an instruction to apply blindly.

## Workflow

1. **Read the complete review**
   - Group duplicate or related comments.
   - Separate blocking correctness issues, non-blocking improvements, questions, and preferences.

2. **Translate each item into a requirement**
   - State the expected behavior or invariant in concrete terms.
   - Clarify any item whose intended outcome is ambiguous before implementing interdependent feedback.

3. **Verify against the repository**
   - Inspect the cited code, call sites, tests, compatibility constraints, and reason for the current implementation.
   - Check whether the suggestion would break existing behavior or add unused scope.

4. **Adjudicate**
   - Accept feedback supported by evidence.
   - Push back with file/test evidence when a suggestion is incorrect, incomplete, or conflicts with an approved decision.
   - Escalate architectural conflicts or unverifiable assumptions to the user.

5. **Implement in risk order**
   - Fix security/data-loss and correctness issues first, then simple changes, then larger refactors.
   - Apply one coherent group at a time and run the nearest relevant check after each group.
   - Use `surgical-implementation` for edits and `investigate` when the review exposes an uncertain root cause.

6. **Report disposition**
   - For every review item, mark fixed, rejected with reason, needs clarification, or deferred with owner.
   - Include the verification evidence for fixed items.

## Response Style

Lead with the technical disposition or completed change. Avoid performative agreement. When correcting an earlier disagreement, state the new evidence and decision plainly.

## Verification

- [ ] Every review item has a disposition.
- [ ] Accepted suggestions were verified against code and tests before implementation.
- [ ] Rejected or deferred suggestions include concrete reasoning.
- [ ] Fixes were tested individually and together where interactions exist.
- [ ] No unrelated reviewer preference became unapproved scope.
