---
name: requesting-code-review
description: Prepares and requests an independent, evidence-focused review of a bounded implementation diff. Use when the user asks to request review, when an authorized multi-agent workflow reaches a review checkpoint, or before integrating a high-risk or multi-file change.
---

# Requesting Code Review

Give the reviewer the requirement, exact diff range, and evidence needed to find real defects without rediscovering the whole project.

## Workflow

1. **Confirm review readiness**
   - The implementation is coherent, relevant checks have run, and temporary/debug artifacts are removed.
   - Record the exact base and head or the explicit working-tree diff to review.

2. **Assemble the review packet**
   - Goal and acceptance criteria.
   - Design/plan paths when applicable.
   - Base/head revisions and changed-file summary.
   - Test commands and results.
   - Known trade-offs, risks, and intentionally out-of-scope areas.

3. **Choose the reviewer**
   - Use a subagent only when delegation is authorized; otherwise perform or request the review through the available workflow.
   - The reviewer must be read-only and should not inherit implementation ownership.

4. **Set review priorities**
   - Ask first for correctness, regressions, security/data safety, compatibility, and missing behavioral tests.
   - Require file/line evidence, a concrete failure mode, severity, and a minimal remediation for blocking findings.

5. **Process the result**
   - Verify findings rather than accepting them automatically.
   - Use `receiving-code-review` for adjudication and fixes.
   - Re-review only the fix diff for addressed findings; run one broad final review if risk warrants it.

## Reviewer Packet Template

Use [references/code-reviewer.md](references/code-reviewer.md) when dispatching an independent reviewer.

## Verification

- [ ] The reviewer saw the intended behavior and exact change range.
- [ ] Test evidence and known risks were included.
- [ ] The review stayed read-only and findings cite concrete evidence.
- [ ] Each blocking finding was adjudicated before completion.
