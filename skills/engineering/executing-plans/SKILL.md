---
name: executing-plans
description: Executes an existing written implementation plan step by step while maintaining progress, review checkpoints, and verification evidence. Use when the user asks to execute, continue, or resume a plan and the plan is already concrete enough to implement.
---

# Executing Plans

Turn an approved written plan into verified changes. This skill owns execution; `implementation-plan` owns creating the plan and `plan-tracker` owns the durable progress file.

## Workflow

1. **Load the plan and local rules**
   - Read the complete plan, linked design/spec, repository instructions, and current worktree status.
   - If `plan-tracker` is available, treat its plan file as the progress ledger.

2. **Review before editing**
   - Check that paths, interfaces, dependencies, and test commands match the current repository.
   - Resolve critical gaps before starting. Correct stale mechanical details in the plan and record the change.

3. **Choose execution mode**
   - Execute inline by default.
   - Use `subagent-driven-development` only when subagents are authorized and tasks have non-overlapping ownership.
   - Use an isolated worktree only when requested or justified by repository/workflow constraints.

4. **Execute one plan task at a time**
   - Mark the task in progress.
   - Follow the task's required test/change sequence.
   - Keep the diff within the planned edit surface; pause if the required scope expands materially.
   - Run the task-level verification and record evidence before marking it complete.

5. **Reconcile the plan continuously**
   - Update paths, decisions, discovered risks, completed steps, and blockers in the plan file.
   - Do not mark future work complete based on expected results.

6. **Complete the whole change**
   - Run broader verification proportional to risk.
   - Inspect the final diff and compare it with every plan requirement.
   - If branch integration is requested, follow `finishing-a-development-branch`; otherwise leave branch state unchanged.

## Stop Conditions

Pause for direction when the plan has an unresolved product decision, verification repeatedly fails without a diagnosed cause, the required change becomes materially broader, or a destructive/external action needs new authority.

Do not stop merely because a plan detail is stale when the correct local fact is discoverable and the intent remains clear.

## Verification

- [ ] Every completed task has recorded evidence.
- [ ] The plan reflects actual status and any deviations.
- [ ] The final diff maps to the plan and excludes unrelated edits.
- [ ] Relevant focused and broader tests were run.
- [ ] Remaining risks or skipped checks are explicit.
