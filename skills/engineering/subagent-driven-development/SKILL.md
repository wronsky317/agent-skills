---
name: subagent-driven-development
description: Executes a written implementation plan through authorized, task-scoped implementer and reviewer agents with durable briefs, evidence, and bounded fix loops. Use when the user explicitly asks for subagent-driven development or an active execution workflow authorizes subagents for independent plan tasks.
---

# Subagent-Driven Development

Coordinate implementation without delegating away accountability. The controller owns the plan, task boundaries, integration, and final verification; agents own only their assigned task or review.

Resolve every `scripts/` and `references/` path relative to the directory containing this `SKILL.md`. Run helper scripts with the target project's root as the working directory.

## Preconditions

- A written, approved implementation plan exists.
- Subagent delegation is authorized by the user, system instructions, or the active workflow.
- Each task has a bounded edit surface and acceptance criteria.
- Concurrent tasks do not edit the same files or shared mutable resources.

If these conditions are not met, use `executing-plans` inline.

## Workflow

1. **Prepare the execution ledger**
   - Read the full plan and linked spec.
   - Record current branch/status and a stable base revision.
   - Resolve a plan-scoped scratch directory with `bash <skill-dir>/scripts/sdd-workspace PLAN_FILE`.
   - Keep briefs, reports, and review packages in that ignored scratch directory.

2. **Select a task**
   - Respect dependencies and choose the next unblocked task.
   - Extract it with `bash <skill-dir>/scripts/task-brief PLAN_FILE TASK_NUMBER`.
   - Record the task base revision before implementation.

3. **Dispatch one implementer**
   - Use [references/implementer-prompt.md](references/implementer-prompt.md) as a template, adapting tool/model language to the current runtime.
   - Give exact file ownership, worktree path, brief path, report path, tests, and shared-workspace constraints.
   - An implementer does not dispatch nested agents or review its own work beyond self-review.

4. **Verify the implementer report**
   - Check status, commits/diff, changed files, test output, and any TDD evidence required by the task.
   - Treat the report as a claim until the controller inspects the actual repository state.
   - If the agent is blocked, decide whether to provide context, revise the plan, or take the task inline.

5. **Run a task-scoped review**
   - Generate a packet with `bash <skill-dir>/scripts/review-package PLAN_FILE BASE HEAD`.
   - Dispatch a read-only reviewer using [references/task-reviewer-prompt.md](references/task-reviewer-prompt.md).
   - Require separate spec-compliance and code-quality verdicts with concrete evidence.

6. **Apply a bounded fix loop**
   - Send confirmed blocking findings back to the implementer.
   - After each fix, capture tests and generate a diff from the previously reviewed head.
   - Use [references/re-review-prompt.md](references/re-review-prompt.md) for a scoped re-review.
   - Stop after repeated unsuccessful rounds; adjudicate or escalate instead of looping indefinitely.

7. **Advance only after the gate passes**
   - Update the durable plan/ledger with task result, commits, tests, findings, and deferred risks.
   - Then select the next dependency-ready task.

8. **Integrate and verify**
   - Run one whole-change review using `requesting-code-review`.
   - Run the relevant full verification on the integrated current tree.
   - Use `finishing-a-development-branch` only when the user asks to integrate or publish the branch.

## Concurrency Rules

Use `dispatching-parallel-agents` only for truly independent tasks with disjoint file ownership. All agents share the workspace unless the runtime explicitly isolates them. Never assume concurrent commits or branch changes are safe in one checkout.

## Verification

- [ ] Delegation was authorized and every agent had bounded ownership.
- [ ] Each completed task has an inspected diff and test evidence.
- [ ] Blocking findings were fixed, adjudicated, or explicitly deferred.
- [ ] Plan/ledger state matches repository state.
- [ ] The combined current tree passed final review and verification.
